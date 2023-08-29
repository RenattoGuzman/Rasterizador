from gl import Renderer
import shaders

width = 800
height = 711

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader

rend.glClearColor(0.5,0.5,0.5)
rend.glBackgroundTexture("textures/grafitireal.bmp")
rend.glClearBackground()

print("background terminado")

rend.glLookAt(camPos = (0,0,3), eyePos= (0,0,-5))
rend.vertexShader = shaders.vertexShader
rend.glDirectionalLight((1,0,1))


################# TELEVISION ##################
rend.fragmentShader = shaders.deepFryShader
rend.glLoadModel(filename = "models/tv.obj",
                 textureName = "textures/tv.bmp",
                 translate = (-1,-2,-2),
                 rotate = (0, 60, 0),
                 scale = (1.5,1.5,1.5))
print("tv terminado")

rend.glRender()
print("tv renderizada")
##################### BASURA #####################

rend.fragmentShader = shaders.trashShader
rend.glLoadModel(filename = "models/bolsas.obj",
                 textureName = "textures/bolsas.bmp",
                 translate = (1,-2.5,-5),
                 rotate = (0, 140, 0),
                 scale = (1.3,1.3,1.3))
print("basura terminada")

rend.glRender()
print("ya renderizo")

################## BASURERO ##################

rend.fragmentShader = shaders.inverseShader
rend.glLoadModel(filename = "models/TrashCan.obj",
                 textureName = "textures/TrashCan.bmp",
                 translate = (2.2,-2.7,-9),
                 rotate = (10, 10, 0),
                 scale = (0.012,0.012,0.012))
print("basurero terminado")

rend.glRender()
print("ya renderizo")

################# PINGUINO ##################
rend.fragmentShader = shaders.waterShader
rend.glLoadModel(filename = "models/pinguin_001.obj",
                 textureName = "textures/animals-texture.bmp",
                 translate = (5,-1,-8),
                 rotate = (0, 150, 0),
                 scale = (1.5,1.5,1.5))
print("pinguino terminado")

rend.glRender()
print("pinguino renderizado")
rend.glFinish("output/con-shaders.bmp")

print("Revisar output/con-shaders.bmp")