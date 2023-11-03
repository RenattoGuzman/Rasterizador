import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader)

""" #               POSITIONS           COLOR
triangleData = [-0.5, -0.5, 0.0,    1.0,0.0,0.0,
                0, 0.5, 0.0,        0.0,1.0,0.0,
                0.5, -0.5, 0.0,     0.0,0.0,1.0,
                
                -0.5, -0.5, 0.0,    1.0,0.0,0.0,
                0, 0.5, 0.0,        0.0,1.0,0.0,
                0.5, -0.5, 0.0,     0.0,0.0,1.0] """

# #               POSITIONS           UVs         NORMALS
# triangleData = [-0.5, -0.5, 0.0,    0.0,0.0,    1.0,0.0,0.0,
#                 -0.5, 0.5, 0.0,     0.0,1.0,    1.0,0.0,0.0,
#                 0.5, -0.5, 0.0,     1.0,0.0,    1.0,0.0,0.0,
                
#                 -0.5, 0.5, 0.0,     0.0,1.0,    1.0,0.0,0.0,
#                 0.5, 0.5, 0.0,      1.0,1.0,    1.0,0.0,0.0,
#                 0.5, -0.5, 0.0,     1.0,0.0,    1.0,0.0,0.0]

obj1 = rend.loadModel(filename = "pinguin.obj", texture = "animals.bmp", position = (0,-2,-5))

isRunning = True
while isRunning:
    
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    #5 unidades por segundo
    if keys[K_d]:
        rend.camPosition.x -= 5 * deltaTime 
         
    elif keys[K_a]:
        rend.camPosition.x += 5 * deltaTime
    
    if keys[K_w]:
        rend.camPosition.y -= 5 * deltaTime
         
    elif keys[K_s]:
        rend.camPosition.y+= 5 * deltaTime
            
    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
        
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime
        
    obj1.rotation.y += 45 * deltaTime
    
    if keys[K_RIGHT]:
        obj1.rotation.y += 45 * deltaTime 
         
    elif keys[K_LEFT]:
        obj1.rotation.y -= 45 * deltaTime
            
    rend.elapsedTime += deltaTime
        
    rend.render()
    
    pygame.display.flip()

pygame.quit()