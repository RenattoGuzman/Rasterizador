import struct
from collections import namedtuple

from obj import Obj

V2= namedtuple('V2', ['x', 'y'])
V3= namedtuple('V3', ['x', 'y','z'])

POINTS = 0
LINES = 1
TRIANGLES = 2
SQUARES = 3

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b*255), 
                  int(g*255),
                  int(r*255)])

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

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
    # def glTriangle(self, A, B, C, clr = None):
        
    #     if A[1] < B[1]:
    #         A, B = B, A
    #     if A[1] < C[1]:
    #         A, C = C, A            
    #     if B[1] < C[1]:
    #         B,C = C, B
            
    #     self.glLine(A,B,clr or self.currColor)
    #     self.glLine(B,C,clr or self.currColor)
    #     self.glLine(C,A,clr or self.currColor)
        
    #     def flatbottom(A, B, C):
    #         try:
    #             mBA = (B[0]-A[0])/(B[1]-A[1])
    #             mCA = (C[0]-A[1])/(C[1]-A[1])    
    #         except :
    #             pass
    #         else:
    #             x0= B[0]
    #             x1= C[0] 
                
    #             for i in range (B[1], A[1]):
    #                 self.glLine((x0,y), (x1,y))
    #                 x0+= mBA
    #                 x1+= mCA 
                     
    #     if B[1] == C[1]:
    #         flatbottom()
    #         pass
        
    #     elif A[1]==B[1]:
    #         pass
        
    #     else:
    #         #Dibujar ambos casos con un nuevo vertice D
    #         pass
            
        
            
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y]=clr or self.currColor

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

        if x0 == x1 and y1 == y0: #Si los vertices son el mismo, dibuja un punto
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

        if x0 > x1: #Si la linea va de derecha a izquierda, se intercambian valores para dibujarlos de izquierda a derecha
            x0, x1= x1, x0
            y0, y1= y1, y0

        dx= abs(x1 - x0)
        dy= abs(y1 - y0)


        offset= 0
        limit= 0.5

        m = dy / dx
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep: #Dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)

            else: #Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1: #Dibujando de abajo para arriba
                    y += 1
                
                else: #Dibujando de arriba para abajo
                    y -= 1

                limit += 1

                    
                    
    def glLoadModel(self, filename, translate = (0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        self.objects.append( Model(filename, translate, rotate, scale))

    def glScanlineFill(self, vertices, clr=None):
        # Triangulate the polygon into multiple triangles
        triangles = []
        for i in range(1, len(vertices) - 1):
            triangles.append((vertices[0], vertices[i], vertices[i + 1]))

        # Fill each triangle using the existing scanline fill algorithm with reversed winding
        for triangle in triangles:
            self._fillTriangle(triangle[::-1], clr or self.currColor)


    def _fillTriangle(self, vertices, clr):
        # Sorting the vertices by their y-coordinate to get the top, middle, and bottom vertices
        vertices = sorted(vertices, key=lambda v: v.y)

        print(vertices)
        
        print(vertices[0])
        if len(vertices) < 3:
            return

        v0, v1, v2 = vertices

        # Calculate the slopes of the two edges of the triangle
        if v2.y - v0.y != 0:
            slope_0_2 = (v2.x - v0.x) / (v2.y - v0.y)
        else:
            slope_0_2 = 0

        if v1.y - v0.y != 0:
            slope_0_1 = (v1.x - v0.x) / (v1.y - v0.y)
        else:
            slope_0_1 = 0

        # Fill the triangle from top to bottom
        for y in range(int(v0.y), int(v2.y) + 1):
            if y < v1.y:
                x_start = v0.x + (y - v0.y) * slope_0_2
                x_end = v0.x + (y - v0.y) * slope_0_1
            else:
                x_start = v1.x + (y - v1.y) * slope_0_2
                x_end = v0.x + (y - v0.y) * slope_0_1

            if x_start > x_end:
                x_start, x_end = x_end, x_start

            for x in range(int(x_start), int(x_end) + 1):
                self.glPoint(x, y, clr)



    def glPoligono(self, vertices, clr=None):
        # Dibuja las líneas que conectan los vértices del polígono
        for i in range(len(vertices)):
            self.glLine(vertices[i], vertices[(i + 1) % len(vertices)], clr or self.currColor)

        # Rellena el polígono
        self.glFill(vertices, clr or self.currColor)


    
    def glFill(self, vertices,clr=None):
        
        # Encuentra las coordenadas mínimas y máximas en el eje x
        minX=min(vertices, key=lambda v: v[0])[0]
        maxX= max(vertices, key=lambda v: v[0])[0]
        
        # Encuentra las coordenadas mínimas y máximas en el eje y
        minY = min(vertices, key=lambda v: v[1])[1]
        maxY = max(vertices, key=lambda v: v[1])[1]
        
        # Itera sobre los puntos dentro del área delimitada por el polígono
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # Comprueba si el punto (x, y) está dentro del polígono y pinta el punto
                if self.esPunto(x, y, vertices):
                    self.glPoint(x, y,clr)


    def esPunto(self, x, y, vertices):
        n = len(vertices)
        adentro = False
        vertices[0]
        
        # Punto inicial del segmento
        p1x, p1y = vertices[0]
        for i in range(n + 1):
            # Punto final del segmento
            p2x, p2y = vertices[i % n]
            
            #Mira si el punto está encima del segmento
            if y > min(p1y, p2y):
                #Si el punto está debajo o en el segmento
                if y <= max(p1y, p2y):
                    #Si el punto está a la izquierda del segmento
                    if x <= max(p1x, p2x):
                        #Mira que el segmento no sea vertical
                        if p1y != p2y:
                            # Calcula la intersección en el eje x entre la línea horizontal y el segmento
                            xinters = (y-p1y) * (p2x-p1x) / (p2y -p1y) + p1x
                        #Mira si el punto esta a la izquierda o al nivel de la intersección
                        if p1x == p2x or x<= xinters:
                            #Cambia el estado
                            adentro = not adentro
            #Actualiza para la otra iteración (siguiente punto)
            p1x, p1y = p2x, p2y 
            
        #Regresa  si está adentro del poligono    
        return adentro              

    def glRender(self):
        
        transformedVerts = []
        for model in self.objects:
            modelMatrix = self.glModelMatrix(model.translate, model.scale)
            
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
            
#                 
        primitives = self.glPrimitiveAssembly(transformedVerts)
        
        if self.fragmentShader:
            primsColor = self.fragmentShader()
            
            primColor = color(primsColor[0], primsColor[1], primsColor[2])
        else:
            primColor = self.currColor
        
        for primitive in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(primitive[0], primitive[1], primitive[2],primColor)
        
        
    def glAddVertices(self,vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)
            
    def glPrimitiveAssembly(self, tVerts):
        
        primitives = [ ]
        
        if self.primitiveType == TRIANGLES:
            for i in range(0,len(tVerts),3):
                triangle = [ ]
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2])
                primitives.append(triangle)            
               
        return primitives
    
    # def glModelMatrix(self, translate = (0,0,0), scale = (1,1,1)):
    #     translation = np.matrix([[1,0,0,translate[0]],
    #                              [0,1,0,translate[1]],
    #                              [0,0,1,translate[2]],
    #                              [0,0,0,1]])
    #     scale = np.matrix([[scale[0],0,0,0],
    #                       [0,scale[1],0,0],
    #                       [0,0,scale[2],0],
    #                       [0,0,0,1]])
        
    #     self.modelMatrix =  translation * scale
    #     return self.modelMatrix
    
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height * 3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height * 3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #ColorTable
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
