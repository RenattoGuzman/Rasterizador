from gl import Renderer,V2,color
import shaders

width = 1000
height = 1000

rend = Renderer(width,height)

rend.glClearColor(0, 0, 0)
rend.glClear()

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel(filename= "pinguin_001.obj", textureName="animals-texture.bmp", translate = (200, 550,200),rotate=(0,0,0), scale = (300,300,300))

rend.glLoadModel(filename= "pinguin_001.obj", textureName="animals-texture.bmp", translate = (800, 550,200),rotate=(0,180,0), scale = (300,300,300))

rend.glLoadModel(filename= "pinguin_001.obj", textureName="animals-texture.bmp", translate = (800, 100,200),rotate=(-25,20,0), scale = (300,300,300))

rend.glLoadModel(filename= "pinguin_001.obj", textureName="animals-texture.bmp", translate = (200, 100,200),rotate=(30,20,0), scale = (300,300,300))


rend.glRender()

rend.glFinish("output.bmp")
print("Revisar el archivo output.bmp")