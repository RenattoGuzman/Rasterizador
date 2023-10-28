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

raytracer.envMap = pygame.image.load("images/fondo.png")

raytracer.rtClearColor(0.25, 0.25, 0.25)
raytracer.rtColor(1, 1, 1)


#  TEXTURAS
linesTex = pygame.image.load("images/lines.jpg")
derretido = pygame.image.load("images/derretido1.jpg")
starwars = pygame.image.load("images/starwars.jpg")
matTex = pygame.image.load("images/mat.png")
cuboTex = pygame.image.load("images/cubo.png")

feliksCamisaTex = pygame.image.load("images/felikscamisa.png")
matsCamisaTex = pygame.image.load("images/matscamisa.png")

feliksTex = pygame.image.load("images/feliks.png")
matsTex = pygame.image.load("images/mats.png")


#  MATERIALES
lines = Material(texture = linesTex, spec = 100, ks = 0.01)
trans = Material(texture=derretido, spec=64, ks=0.15, ior=3, matType=TRANSPARENT)
refl = Material(diffuse=(0.1, 0.1, 0.1), spec = 64, ks = 0.1, matType= REFLECTIVE)
mat = Material(texture = matTex, spec = 100, ks = 0.01) 
cubo = Material(texture = cuboTex, spec = 100, ks = 0.01)
cuboRefra = Material(texture = cuboTex, spec = 128, ks = 0.01, ior=2, matType= TRANSPARENT)

feliksCamisa = Material(texture = feliksCamisaTex, spec = 100, ks = 0.01)
matsCamisa = Material(texture = matsCamisaTex, spec = 100, ks = 0.01)
feliks = Material(texture = feliksTex, spec = 100, ks = 0.01)
mats = Material(texture = matsTex, spec = 100, ks = 0.01)


# Cubo Main
raytracer.scene.append(Box(position=(0.1,-0.7,-3), size = (0.4,0.4,0.4), material = cubo)) 

# Cubo Izquierda Refractivo
raytracer.scene.append(Box(position=(-2,-0.5,-3.2), size = (0.4,0.4,0.4), material = cuboRefra)) 


# # Mesa Reflectiva
raytracer.scene.append(Box(position=(0.1,-1.3,-3.5), size = (7.5,0.5,3), material = refl)) 

# Mat del cubo
raytracer.scene.append(Box(position=(0.1,-1.2,-3.2), size = (3,0.5,2.7), material = mat)) 

# Feliks Zemdegs
#    Cuerpo
raytracer.scene.append(Ellipsoid(position=(0,-0.5,-5), radius=(0.8,1.3,0.8), material=feliksCamisa))
#   Cabeza 
raytracer.scene.append(Ellipsoid(position=(0,1,-5), radius=(0.5,0.7,0.8), material=feliks))

# Mats Valk
#   Cuerpo
raytracer.scene.append(Ellipsoid(position=(3,-0.5,-6), radius=(0.6,1.1,0.8), material=matsCamisa))
#   Cabeza 
raytracer.scene.append(Ellipsoid(position=(3,1,-6), radius=(0.3,0.5,0.8), material=mats))

# Luces
raytracer.lights.append(AmbientLight(intensity=1))
raytracer.lights.append(DirectionalLight(direction=(-0.3,-0.5,-1), intensity=0.95, color=(1, 1, 1)))

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