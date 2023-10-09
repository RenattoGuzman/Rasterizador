import pygame
from pygame.locals import * 
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 512
height = 512

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)

raytracer.rtClearColor(0.25,0.25,0.25)

#  TEXTURAS
derretido2 = pygame.image.load("images/derretido2.jpg")
starwars = pygame.image.load("images/starwars.jpg")

#  MATERIALES
derretido2Tex = Material(texture = derretido2, spec = 100, ks = 0.01)
starwarsTex = Material(texture = starwars, spec = 100, ks = 0.01)
c0 = Material(diffuse=(0.33,0.23,0.44))
c1 = Material(diffuse=(0.92,0.87,0.65))
c2 = Material(diffuse=(0.87,0.42, 0.51))
c3 = Material(diffuse=(0.12,0.13,0.1))
c4 = Material(diffuse=(0.35,0.48,0.5))

# PAREDES
raytracer.scene.append(Plane(position=(0,-2,0), normal = (0,1,-0.02), material = c1)) # piso
raytracer.scene.append(Plane(position=(0,5,0), normal = (0,1,0.2), material = c2)) # arriba
raytracer.scene.append(Plane(position=(4,0,0), normal = (1,0,0.2), material = c3)) # derecha
raytracer.scene.append(Plane(position=(-4,0,0), normal = (1,0,-0.2), material = c4)) # izquierda
raytracer.scene.append(Plane(position=(0,0,-20), normal = (0,0,0.2), material = starwarsTex)) # fondo

# CUBOS
raytracer.scene.append(Box(position=(1.5,-0.5,-5), size = (1.5,1.5,1.5), material = starwarsTex)) # Derecha
raytracer.scene.append(Box(position=(-1.5,-0.5,-5), size = (1.25,1.25,1.25), material = derretido2Tex)) # Izquierda

# DISCO
raytracer.scene.append(Disk(position=(0,1,-5), normal = (0,1,0), radius= 1.5, material= c0))

raytracer.lights.append(AmbientLight(intensity=1))
raytracer.lights.append(DirectionalLight(direction=(1,1,-2), intensity=0.95))
raytracer.lights.append(PointLight(point=(0,0,-5), intensity=150, color= (1,1,1)))

raytracer.rtClear()
raytracer.rtRender()

print("\nTiempo de renderizado:", pygame.time.get_ticks() / 1000, "segundos")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False

rect = pygame.Rect(0,0,width,height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "resultado.jpg")
                
pygame.quit()