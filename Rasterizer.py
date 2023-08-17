from gl import Renderer
import shaders


width = 1000
height = 1000

rend = Renderer(width, height)

################################
# inverseShader
# deepFryShader
# waterShader
################################


rend.vertexShader = shaders.vertexShader

rend.fragmentShader = shaders.waterShader

rend.glLookAt(camPos = (0,0,3), eyePos= (0,0,-5))

rend.glLoadModel(filename = "pinguin_001.obj",
                 textureName = "animals-texture.bmp",
                 translate = (0,-2,-5),
                 rotate = (0, 140, 0),
                 scale = (3,3,3))



rend.glRender()

rend.glFinish("waterShader.bmp")

print("Revisar waterShader.bmp")