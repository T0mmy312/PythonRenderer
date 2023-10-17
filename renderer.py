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
        return (self.r, self.g, self.b)
    
    def __sub__(self, other):
        return color(self.r - other.r, self.g - other.g, self.b - other.b)
    
    def __mul__(self, other):
        return color(clamp(0, self.r * other, 255), clamp(0, self.g * other, 255), clamp(0, self.b * other, 255))

class light:
    def __init__(self, pos, color, intensity):
        self.pos = pos
        self.color = color
        self.intensity = intensity

class renderer:
    def __init__(self, c, f, ref, screenX, screenY, sensX, polys, lights, maxAngleOffset, maxBounces):
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
        self.mAO = maxAngleOffset
        self.maxBounces = maxBounces
    
    def render(self, surface):
        fy = vector3(0, 1, 0)
        if self.f != fy:
            fr = crossProd(self.f, fy).unitVec() * self.mdPix
        else:
            fr = vector3(1, 0, 0)
        fo = crossProd(self.f, fr).unitVec() * self.mdPix
        oo = self.c + self.f
        hsx = self.screenX / 2
        hsy = self.screenY / 2
        polys = []
        pixls = [[None] * self.screenX] * self.screenY
        for y in range(self.screenY + 1):
            row = []
            for x in range(self.screenX + 1):
                polys = self.polys
                op = oo + (x - hsx + 0.5) * fr + (y + hsy + 0.5) * fo
                points = [(op, color(255, 255, 255), 0)]
                cop = self.c - op
                a = op + self.f + ((self.f.amount()/cos(angl(cop, self.f))) * cop.unitVec() - self.f) * self.ref
                g1 = gP(op, a)
                tempPoint = None
                noLight = True
                bounces = 0
                while noLight and bounces <= self.maxBounces:
                    for light in self.lights:
                        eq = g1.element(light.pos)
                        if eq[0] and eq[1] >= 0:
                            points.append((light.pos, light.color, light.intensity))
                            noLight = False
                            break
                        alpha = degrees(angl(light.pos - g1.op, g1.a))
                        if alpha < self.mAO:
                            points.append((light.pos, light.color, light.intensity * (1 - alpha/self.mAO)))
                            noLight = False
                            break
                    if not noLight:
                        break
                    for i,pol in enumerate(polys):
                        if tempPoint != None:
                            if i == tempPoint[4]:
                                continue
                        e = pol.plane()
                        n = e.n()
                        if n * g1.a == 0:
                            continue
                        dk = det3x3([
                            [e.a.x, e.b.x, -g1.a.x],
                            [e.a.y, e.b.y, -g1.a.y],
                            [e.a.z, e.b.z, -g1.a.z]
                        ])
                        dt = det3x3([
                            [g1.op.x - e.p.x, e.b.x, -g1.a.x],
                            [g1.op.y - e.p.y, e.b.y, -g1.a.y],
                            [g1.op.z - e.p.z, e.b.z, -g1.a.z]
                        ])
                        ds = det3x3([
                            [e.a.x, g1.op.x - e.p.x, -g1.a.x],
                            [e.a.y, g1.op.y - e.p.y, -g1.a.y],
                            [e.a.z, g1.op.z - e.p.z, -g1.a.z]
                        ])
                        dp = det3x3([
                            [e.a.x, e.b.x, g1.op.x - e.p.x],
                            [e.a.y, e.b.y, g1.op.y - e.p.y],
                            [e.a.z, e.b.z, g1.op.z - e.p.z]
                        ])
                        if dk == 0:
                            continue
                        t = dt/dk
                        s = ds/dk
                        g1t = dp/dk
                        if t > 1 or s > 1 or t < 0 or s < 0 or g1t <= 0:
                            continue
                        sp = e.calc(t, s)
                        l = (sp - g1.op).amount()
                        if tempPoint != None:
                            if l < tempPoint[2]:
                                tempPoint = (sp, pol.rgb, l, e, i)
                        else:
                            tempPoint = (sp, pol.rgb, l, e, i)
                    if tempPoint != None:
                        nea = g1.a * -1
                        n = tempPoint[3].n()
                        gam = angl(n, nea)
                        nea = nea.unitVec() * (n.amount()/cos(gam))
                        newa = n + (n - nea)
                        g1 = gP(tempPoint[0], newa)
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
                print(f"Pixel ({x}, {y}) was rendered with color {totalColor.tup()}! {int(y/self.screenY * 100)}% Complete!")
            pixls.append(row)
        return pixls