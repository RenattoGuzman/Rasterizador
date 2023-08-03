import struct
from matrix import  Multi
from math import pi, sin, cos
from collections import namedtuple
from obj import Obj
from texture import Texture


V2= namedtuple('V2', ['x', 'y'])
V3= namedtuple('V3', ['x', 'y','z'])

POINTS = 0
LINES = 1
TRIANGLES = 2
SQUARES = 3

def char(c):
    #1 byte
    return struct.pack('=c',c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h',w)

def dword(d):
    #4 bytes      
    return struct.pack('=l',d)

def color(r,g,b):
    return bytes([int(b*255),int(g*255),int(r*255)])

class Model(object):
    def __init__(self,filename, translate =(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        self.model = Obj(filename)
        self.vertices = self.model.vertices
        self.texcoords = self.model.texcoords
        self.normals = self.model.normals
        self.faces = self.model.faces
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        
    def LoadTexture(self, textureName):
        self.texture = Texture(textureName)


class Renderer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()
        self.glColor(1, 1, 1)
        self.primitiveType = TRIANGLES
        self.vertexBuffer = [ ]
        self.vertexShader = None
        self.fragmentShader = None
        self.objects = [ ]
        self.activeTexture = None
        
    def glClearColor(self,r,g,b):
        self.clearColor = color(r,g,b)

    def glColor(self,r,g,b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
        self.zbuffer = [[float('inf') for y in range(self.height)]
                       for x in range(self.width)]
        
    def glPoint(self,x,y,clr=None):
        if 0<=x<self.width and 0<=y<self.height:
            self.pixels[x][y] = clr or self.currColor
            
    def glTriangle_bc(self,A,B,C,vtA, vtB, vtC):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))
        
        colorA = (1, 0, 0)
        colorB = (0,1,0)
        colorC = (0,0,1)
        
        for x in range (minX, maxX +1):
            for y in range (minY, maxY +1):
                if (0 <= x < self.width) and (0 <= y < self.height):
                    P = (x,y)
                    u,v,w = Multi.barycentricCoords(A,B,C,P)
                    
                    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
                        
                        z = u * A[2] + v * B[2] + w * C[2]

                        if z < self.zbuffer[x][y]:

                            self.zbuffer[x][y] = z

                            uvs = (u*vtA[0] + v*vtB[0] + w*vtC[0],
                                    u*vtA[1] + v*vtB[1] + w*vtC[1])
                            

                            if self.fragmentShader != None:
                                colorP = self.fragmentShader(texCoords=uvs,  texture = self.activeTexture)
                                
                                self.glPoint(x,y,color(colorP[0],colorP[1],colorP[2]))
                            else:
                                self.glPoint(x,y,colorP)
                        


    def glTriangle(self,v0,v1,v2, clr=None):
        self.glLine(v0,v1, clr or self.currColor)
        self.glLine(v1,v2, clr or self.currColor)
        self.glLine(v2,v0, clr or self.currColor)

    def glLine(self, v0, v1, clr= None):
        #Bresenham line algorith
        #y= mx + b
        
        """ m= (v1.y - v0.y) / (v1.x - v0.x)
        y= v0.y

        for x in range(v0.x, v1.x + 1):
            self.glPoint(x, int(y))
            y += m """
            
        x0 = int(v0[0])
        x1 = int(v1[0])        
        y0 = int(v0[1])
        y1 = int(v1[1])

        #Si los vertices son el mismo, dibuja un punto
        if x0 == x1 and y1 == y0: 
            self.glPoint(x0, y0)

            return 
        
        dx= abs(x1 - x0)
        dy= abs(y1 - y0)

        steep= dy > dx    
        
        #Si la pendiente es mayor a 1 o menor a -1
        if steep: 
            #Intercambio de valores
            x0, y0 = y0, x0
            x1, y1= y1, x1

        #Si la linea va de derecha a izquierda, se intercambian valores para dibujarlos de izquierda a derecha
        if x0 > x1: 
            x0, x1= x1, x0
            y0, y1= y1, y0

        dx= abs(x1 - x0)
        dy= abs(y1 - y0)


        offset= 0
        limit= 0.5

        m = dy / dx
        y = y0
        
        for x in range(x0, x1 + 1):
            #Dibujar de manera vertical
            if steep: 
                self.glPoint(y, x, clr or self.currColor)
            
            #Dibujar de manera horizontal
            else: 
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                #Dibujando de abajo para arriba
                if y0 < y1: 
                    y += 1
                #Dibujando de arriba para abajo
                else: 
                    y -= 1

                limit += 1
                              
    def glLoadModel(self, filename, textureName, translate = (0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        
        model = Model(filename, translate, rotate, scale)
        model.LoadTexture(textureName)
        
        self.objects.append(model)

    def glRender(self):
        
        transformedVerts = []
        texCoords = []
        
        for model in self.objects:
            
            self.activeTexture = model.texture
            modelMatrix = self.glModelMatrix(model.translate,model.rotate, model.scale)
            
            for face in model.faces:
                vertCount = len(face)
                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                
                if  vertCount == 4:
                    v3 = model.vertices[ face[3][0] - 1]
                    
                if self.vertexShader:
                    v0 = self.vertexShader(v0,modelMatrix = modelMatrix)
                    v1 = self.vertexShader(v1,modelMatrix = modelMatrix)
                    v2 = self.vertexShader(v2,modelMatrix = modelMatrix)
                    if  vertCount == 4:
                        v3 = self.vertexShader(v3,modelMatrix = modelMatrix)
                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if  vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)
                vt0=model.texcoords[face[0][1] -1]
                vt1=model.texcoords[face[1][1] -1]
                vt2=model.texcoords[face[2][1] -1]
                if vertCount == 4:
                    vt3=model.texcoords[face[3][1] -1]

                texCoords.append(vt0)
                texCoords.append(vt1)
                texCoords.append(vt2)
                if vertCount == 4:
                    texCoords.append(vt0)
                    texCoords.append(vt2)
                    texCoords.append(vt3)

        primitives = self.glPrimitiveAssembly(transformedVerts, texCoords)
                
        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle_bc(prim[0], prim[1], prim[2], 
                                   prim[3], prim[4], prim[5])
        
    def glAddVertices(self,vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)
            
    def glPrimitiveAssembly(self, tVerts,tTexCoords):
        
        primitives = [ ]
        
        if self.primitiveType == TRIANGLES:
            for i in range(0,len(tVerts),3):
                triangle = [ ]
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2])
                
                triangle.append(tTexCoords[i])
                triangle.append(tTexCoords[i+1])
                triangle.append(tTexCoords[i+2])

                
                primitives.append(triangle)            
               
        return primitives
    
    def glModelMatrix(self, translate = (0,0,0), rotate= (0,0,0), scale = (1,1,1)):
        translation = ([[1,0,0,translate[0]],
                                 [0,1,0,translate[1]],
                                 [0,0,1,translate[2]],
                                 [0,0,0,1]])
        
        pitch = rotate[0] * pi/180
        yaw = rotate[1] * pi/180
        roll = rotate[2] * pi/180

        Rx = [[1,0,0,0],
            [0,cos(pitch),-sin(pitch),0 ],
            [0, sin(pitch), cos(pitch),0],
            [0,0,0,1]]
        
        Ry =[[cos(yaw),0,sin(yaw),0],
            [0,1,0,0],
            [-sin(yaw),0,cos(yaw),0],
            [0,0,0,1]]
        
        Rz =[[cos(roll),-sin(roll),0,0],
            [sin(roll),cos(roll),0,0],
            [0,0,1,0],
            [0,0,0,1]]
        
        rotMat = Multi.var_Mul_Matrix([Rx,Ry,Rz])
        
        scale = ([[scale[0],0,0,0],
                          [0,scale[1],0,0],
                          [0,0,scale[2],0],
                          [0,0,0,1]])
        
        self.modelMatrix =  Multi.var_Mul_Matrix([translation, rotMat, scale])
        return self.modelMatrix
    
    def glRotationMatrix(self, pitch = 0, yaw = 0,roll = 0):
        pitch = pi/180
        yaw *= pi/180
        roll *= pi/180
        
        pitchMat = ([[1,0,0,0],
                    [0,cos(pitch),-sin(pitch),0],
                    [0,sin(pitch),cos(pitch),0],
                    [0,0,0,1]])
        
        yawMat = ([[cos(yaw),0,sin(yaw),0],
                  [0,1,0,0],
                  [-sin(yaw),0,cos(yaw),0],
                  [0,0,0,1]])
        rollMat = ([[cos(roll),-sin(roll),0,0],
                   [sin(roll),cos(roll),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])

        return Multi.var_Mul_Matrix([pitchMat,yawMat,rollMat])

    def glFinish(self,filename):
        with open(filename,"wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])