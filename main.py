import time
import pygame
from vectors import *
from renderer import *

startTime = time.time()
pygame.init()

polis = []
with open("polygons.txt", "r") as file:
    con = file.read().replace(" ", "").replace("(", "").replace(")", "").split("\n")
    con.pop(0)
    for pol in con:
        spl = pol.split(";")
        a = spl[0].split(",")
        b = spl[1].split(",")
        c = spl[2].split(",")
        rgb = spl[3].split(",")
        polis.append(poly(vector3(float(a[0]), float(a[1]), float(a[2])), vector3(float(b[0]), float(b[1]), float(b[2])), vector3(float(c[0]), float(c[1]), float(c[2])), color(float(rgb[0]), float(rgb[1]), float(rgb[2]))))
    file.close()

with open("cubes.txt", "r") as file:
    con = file.read().replace(" ", "").replace("(", "").replace(")", "").split("\n")
    con.pop(0)
    for line in con:
        spl = line.split(";")
        posL = spl[0].split(",")
        pos = vector3(float(posL[0]), float(posL[1]), float(posL[2]))
        of = vector3(float(spl[1])/2, float(spl[2])/2, float(spl[3])/2)
        lColor = spl[4].split(",")
        col = color(int(lColor[0]), int(lColor[1]), int(lColor[2]))
        if int(spl[5]) == 1:
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), col))
        else:
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y + of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x - of.x, pos.y + of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x + of.x, pos.y + of.y, pos.z + of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y - of.y, pos.z - of.z), vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), col))
            polis.append(poly(vector3(pos.x + of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z + of.z), vector3(pos.x - of.x, pos.y - of.y, pos.z - of.z), col))
    file.close()

lights = []
with open("lights.txt", "r") as file:
    con = file.read().replace(" ", "").replace("(", "").replace(")", "").split("\n")
    con.pop(0)
    for line in con:
        spl = line.split(";")
        pos = spl[0].split(",")
        rgb = spl[1].split(",")
        intens = float(spl[2])
        lights.append(light(vector3(float(pos[0]), float(pos[1]), float(pos[2])), color(float(rgb[0]), float(rgb[1]), float(rgb[2])), intens, float(spl[3])))
    file.close()

window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Renderer")

running = True

#one time renderer
screen.fill((255, 255, 255))
pygame.display.flip()
ren = renderer(vector3(3, 0, 0), vector3(-0.08, 0, 0), 0.8, window_width, window_height, window_width/1000, polis, lights, 4)
pixs = ren.render()

with open("screen.txt", "w") as file:
    con = ""
    for y, row in enumerate(pixs):
        for x, pix in enumerate(row):
            con += f"({pix[0]}, {pix[1]}, {pix[2]}) "
        con += "\n"
    file.write(con)
    file.close()
for y, row in enumerate(pixs):
    for x, colo in enumerate(row):
        screen.set_at((x, y), (colo[0], colo[1], colo[2]))

pygame.display.flip()

dur = time.time()- startTime
if dur > 60:
    m = int(dur/60)
    s = dur - m*60
    print(f"Render Complete in {m} min and {s} sec")
else:
    print(f"ender Complete in {dur} sec")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                running = False

pygame.quit()