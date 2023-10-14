import pygame
from pygame.locals import * 
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 650
height = 500

pygame.init()


screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)

raytracer.envMap = pygame.image.load("images/starwars.jpg")

raytracer.rtClearColor(0.25, 0.25, 0.25)
raytracer.rtColor(1, 1, 1)


#  TEXTURAS
linesTex = pygame.image.load("images/lines.jpg")
derretido = pygame.image.load("images/derretido1.jpg")
starwars = pygame.image.load("images/starwars.jpg")

#  MATERIALES
lines = Material(texture = linesTex, spec = 100, ks = 0.01)
trans = Material(texture=derretido, spec=64, ks=0.15, ior=3, matType=TRANSPARENT)
refl = Material(diffuse=(0.9, 0.1, 0.1), spec = 64, ks = 0.1, matType= REFLECTIVE)

# Opaco
raytracer.scene.append(Ellipsoid(position=(0,0,-5), radius=(1,1.8,1), material=lines))
# Transparente
raytracer.scene.append(Ellipsoid(position=(-2,0,-5), radius=(0.8,0.4,0.7), material=trans))
# Reflectivo
raytracer.scene.append(Ellipsoid(position=(3,0,-10), radius=(3,2.2,1), material=refl))


raytracer.lights.append(AmbientLight(intensity=1))
raytracer.lights.append(DirectionalLight(direction=(1,1,-2), intensity=0.95))

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