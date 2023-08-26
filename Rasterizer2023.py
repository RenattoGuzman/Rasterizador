from gl import Renderer
import shaders


width = 1000
height = 1000

rend = Renderer(width, height)


rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

## Medium Angle
#rend.glLookAt(camPos = (0,1,1), eyePos= (0,0,-5))

## High Angle
# rend.glLookAt(camPos = (0,5,-1), eyePos= (0,0,-5))

## Low Angle
#rend.glLookAt(camPos = (0,-5,1), eyePos= (0,0,-5))

## Dutch Angle
rend.glLookAt(camPos = (-5,-5,-1), eyePos= (0,0,-5))

rend.glLoadModel(filename = "pinguin_001.obj",
                 textureName = "animals-texture.bmp",
                 translate = (0,-3,-5),
                 rotate = (0, 180, 0),
                 scale = (4,4,4))

rend.glRender()

rend.glFinish("angles/dutch_angle.bmp")

