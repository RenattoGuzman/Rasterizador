import pygame
from pygame.locals import *
import glm
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


obj1 = rend.loadModel(filename = "pinguin.obj", texture = "animals.bmp", position = (0,-0.72,-2))

rend.target = obj1.position

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
            elif event.key == pygame.K_SPACE:
                rend.toggleFilledMode()
                
            elif event.key == pygame.K_1:
                rend.setShaders(vertex_shader, fragment_shader)
                print("                                    Shader original")
            elif event.key == pygame.K_2:
                rend.setShaders(vertex_shader, platinum_shader)
                print("                                    Platinum Shader")
            elif event.key == pygame.K_3:
                rend.setShaders(vertex_shader, disco_shader)
                print("                                    Disco Shader")
            elif event.key == pygame.K_4:
                rend.setShaders(vertex_shader, semaforo_shader)
                print("                                    Semaforo Shader")
            elif event.key == pygame.K_5:
                rend.setShaders(vertex_shader, candle_shader) 
                print("                                    Candle Shader")           

    #5 unidades por segundo
    if keys[K_d]:
        rend.camPosition.x -= 5 * deltaTime 
         
    elif keys[K_a]:
        rend.camPosition.x += 5 * deltaTime
    
    if keys[K_w]:
        rend.camPosition.y -= 5 * deltaTime
         
    elif keys[K_s]:
        rend.camPosition.y += 5 * deltaTime
            
    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
        
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime
        
    obj1.rotation.y += 45 * deltaTime
    
    if keys[K_RIGHT]:
        obj1.rotation.y += 45 * deltaTime 
         
    elif keys[K_LEFT]:
        obj1.rotation.y -= 135 * deltaTime 
        
    elif keys[K_UP]:
        obj1.rotation.y -= 45* deltaTime        
        
    rend.elapsedTime += deltaTime
        
    rend.update()
    rend.render()
    
    pygame.display.flip()

pygame.quit()