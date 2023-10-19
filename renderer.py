import pygame
import time
from math import *
from vectors import *

def clamp(min, x, max):
    return min if x < min else max if x > max else x 

class poly:
    def __init__(self, a, b, c, rgb):
        self.a = a
        self.b = b
        self.c = c
        self.rgb = rgb
    
    def plane(self):
        return plane(self.a, self.b - self.a, self.c - self.a)

class color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def invert(self):
        return color(clamp(0, 255 - self.r, 255), clamp(0, 255 - self.g, 255), clamp(0, 255 - self.b, 255))
    
    def tup(self):
        return (int(self.r), int(self.g), int(self.b))
    
    def __sub__(self, other):
        return color(self.r - other.r, self.g - other.g, self.b - other.b)
    
    def __mul__(self, other):
        return color(clamp(0, self.r * other, 255), clamp(0, self.g * other, 255), clamp(0, self.b * other, 255))

class light:
    def __init__(self, pos, color, intensity, radius):
        self.pos = pos
        self.color = color
        self.intensity = intensity
        self.radius = radius

class renderer:
    def __init__(self, c, f, ref, screenX, screenY, sensX, polys, lights, maxBounces):
        self.c = c
        self.f = f
        self.ref = ref
        self.screenX = screenX
        self.screenY = screenY
        self.sensX = sensX
        self.sensY = (screenY/screenX) * sensX
        self.mdPix = sensX/screenX
        self.polys = polys
        self.lights = lights
        self.maxBounces = maxBounces
    
    def render(self):
        fy = vector3(0, 1, 0)
        if self.f != fy:
            fr = crossProd(self.f, fy).unitVec() * self.mdPix
        else:
            fr = vector3(1, 0, 0)
        fo = crossProd(self.f, fr).unitVec() * self.mdPix
        oo = self.c + self.f
        hsx = self.screenX / 2
        hsy = self.screenY / 2
        sxeven = self.screenX % 2 == 0
        syeven= self.screenY % 2 == 0
        pixls = []
        for y in range(self.screenY + 1):
            row = []
            for x in range(self.screenX + 1):
                op = oo + (x - hsx + (0.5 if sxeven else 0)) * fr + (hsy - y - (0.5 if syeven else 0)) * fo
                points = [(op, color(255, 255, 255), 0)]
                cop = op - self.c
                a = self.f + ((self.f.amount()/cos(angl(cop, self.f))) * cop.unitVec() - self.f) * self.ref
                g1 = gP(op, a)
                tempPoint = None
                noLight = True
                bounces = 0
                while noLight and bounces <= self.maxBounces:
                    for light in self.lights:
                        ang = angl(light.pos - g1.op, g1.a)
                        if ang < 1.57079633:
                            rad = sin(ang) * (light.pos - g1.op).amount()
                            if rad < light.radius:
                                points.append((light.pos, light.color, light.intensity * (1 - rad/light.radius)))
                                noLight = False
                                break
                    if not noLight:
                        break
                    for i,pol in enumerate(self.polys):
                        if tempPoint != None:
                            if i == tempPoint[4]:
                                continue
                        e = pol.plane()
                        sp = pIntersectG(e, g1, (0, 999), (0, 1), (0, 1))
                        if sp == None:
                            continue
                        l = (sp - g1.op).amount()
                        if tempPoint != None:
                            if l < tempPoint[2]:
                                tempPoint = (sp, pol.rgb, l, e, i)
                        else:
                            tempPoint = (sp, pol.rgb, l, e, i)
                    if tempPoint != None:
                        g1 = pReflectG(tempPoint[3], g1, tempPoint[0])
                        bounces += 1
                        points.append((tempPoint[0], tempPoint[1], 0)) 
                    else:
                        points.append((vector3(0, 0, 0), color(0, 0, 0), 0))
                        noLight = False
                totalLen = 0
                totalColor = color(255, 255, 255)
                for vp in range(1, len(points)):
                    totalLen += (points[vp][0] - points[vp - 1][0]).amount()
                    totalColor -= points[vp][1].invert()
                totalColor *= ((1/(totalLen**2)) * points[-1][2])
                row.append(totalColor.tup())
                print(f"{int(y/self.screenY * 100)}% Complete! Pixel ({x}, {y}) was rendered with color {totalColor.tup()}!")
            pixls.append(row)
        return pixls