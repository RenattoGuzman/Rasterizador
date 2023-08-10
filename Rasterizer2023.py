from gl import Renderer
import shaders

width = 1000
height = 1000

rend = Renderer(width,height)

rend.glClearColor(0, 0, 0)
rend.glClear()

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

#rend.glLoadModel(filename= "pinguin_001.obj", textureName="animals-texture.bmp", translate = (0, 0,0),rotate=(0,0,0), scale = (300,300,300))


rend.glRender()

rend.glFinish("output1.bmp")
print("Revisar el archivo output1.bmp")