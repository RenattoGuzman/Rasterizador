import numpy as np
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


obj1 = rend.loadModel(filename = "models/pinguin.obj", texture = "textures/animals.bmp",position=(0, -0.72, -2), scale=(1.2,1.2,1.2))

rend.target = obj1.position

current_model = "Pinguino"

isRunning = True
is_left_button_pressed = False
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

                rend.deleteModel(obj1)
                obj1 = rend.loadModel(filename="models/pinguin.obj", texture="textures/animals.bmp", position=(0, -0.72, -2), scale=(1.2,1.2,1.2))
                current_model = "Pinguino"
                
            elif event.key == pygame.K_2:
                rend.deleteModel(obj1)
                obj1 = rend.loadModel(filename = "models/Mjollnir Blender OBJ.obj", texture = "textures/Mjollnir_BaseColor.png", position = (0,0,-2), scale=(0.4,0.4,0.4))
                current_model = "Martillo"
                
            elif event.key == pygame.K_3:
                rend.deleteModel(obj1)
                obj1 = rend.loadModel(filename = "models/GLOCK 19 F T.obj", texture = "textures/GLOCK_TEXTURE.png", position = (0,0.5,-1), scale=(0.4,0.4,0.4))
                current_model = "Pistola"
                
            elif event.key == pygame.K_4:
                rend.deleteModel(obj1)
                obj1 = rend.loadModel(filename = "models/TrashCan.obj", texture = "textures/TrashCan.bmp", position = (0,-0.5,-2), scale=(0.004,0.004,0.004))
                current_model = "Basura"
                
            elif event.key == pygame.K_z:
                rend.setShaders(vertex_shader, fragment_shader) 

            elif event.key == pygame.K_x:
                rend.setShaders(vertex_shader, platinum_shader) 

            elif event.key == pygame.K_c:
                rend.setShaders(vertex_shader, disco_shader) 

            elif event.key == pygame.K_v:
                rend.setShaders(vertex_shader, semaforo_shader) 

            elif event.key == pygame.K_b:
                rend.setShaders(vertex_shader, candle_shader) 

             
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            is_left_button_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button
            is_left_button_pressed = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                speed = 5 * deltaTime
                
                if current_model == "Basura":
                    speed = 1500 * deltaTime
                
                translation_vector = glm.vec3(0, 0, speed)
                camera_translation = glm.translate(glm.mat4(), translation_vector)
                rend.camPosition += glm.vec3(camera_translation[3])

            elif event.button == 5:  # Scroll down
                speed = -5 * deltaTime

                if current_model == "Basura":
                    speed = - 1500 * deltaTime
                    
                translation_vector = glm.vec3(0, 0, speed)
                camera_translation = glm.translate(glm.mat4(), translation_vector)

                rend.camPosition += glm.vec3(camera_translation[3])

            
    rel_mouse_movement = pygame.mouse.get_rel()

    if is_left_button_pressed:
        sensitivity = 0.5  
        rend.camRotation.x += rel_mouse_movement[1] * sensitivity
        rend.camRotation.y += rel_mouse_movement[0] * sensitivity
        rend.camRotation.x = max(min(rend.camRotation.x, 90), -90)

    if current_model != "Basura":
        rend.camPosition.z = max(min(rend.camPosition.z,0.78), -0.78)
    else:
        rend.camPosition.z = max(min(rend.camPosition.z,500), -346)


    pygame.mouse.get_rel()
    if keys[K_RIGHT]:
        obj1.rotation.y += 45 * deltaTime 
         
    elif keys[K_LEFT]:
        obj1.rotation.y -= 135 * deltaTime 
        
    elif keys[K_UP]:
        obj1.rotation.y -= 45* deltaTime        

    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
        
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime
    
        
    rend.elapsedTime += deltaTime
        
    rend.update()
    rend.render()
    
    pygame.display.flip()

pygame.quit()