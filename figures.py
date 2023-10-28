import mathLibrary as ml
from math import tan, pi, atan2, acos, sqrt

class Intercept(object):
    def __init__(self, distance, point, texcoords, normal, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape(object):
    def __init__(self,position,material):
        self.position = position
        self.material = material

    def ray_intersect(self,orig,dir):
        return None

class Sphere(Shape):
    def __init__(self,position,radius,material):
        self.radius = radius
        super().__init__(position,material)
        
    def ray_intersect(self, orig, dir):
        l = ml.twoVecSubstraction(self.position, orig)
        lengthL = ml.vecMag(l)
        tca = ml.twoVecDot(l,dir)
        
        #if radius < d: no hay contacto (False)
        #if radius > d: si hay contacto (True)
        d = (lengthL**2 - tca**2)**0.5
        if d > self.radius:
            return None
        
        thc = (self.radius**2 - d**2)**0.5
        t0 = tca - thc
        t1 = tca + thc
        
        if t0<0:
            t0 = t1
        if t0<0:
            return None
        
        #P = O+D*t0
        p = ml.twoVecSum(orig,ml.vecMultEsc(dir, t0))
        normal = ml.twoVecSubstraction(p,self.position)
        normal = ml.vecNorm(normal)
        
        u = (atan2(normal[2], normal[0]) / (2*pi)) + 0.5
        v = acos(normal[1]) / pi
        
        return Intercept(distance = t0,
                         point = p,
                         normal = normal,
                         texcoords= (u,v),
                         obj = self)

class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = ml.vecNorm(normal)
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        
        denom = ml.twoVecDot(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = ml.twoVecDot(ml.twoVecSubstraction(self.position, orig), self.normal)
        t = num/denom
        
        if t<0:
            return None
        
        #P = O+D*t0
        p = ml.twoVecSum(orig, ml.vecMultEsc(dir,t))
        
        return Intercept(distance = t,
                         point = p,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)
    
    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)
        
        if planeIntersect is None:
            return None
        
        contactDistance = ml.twoVecSubstraction(planeIntersect.point, self.position)
        contactDistance = ml.vecMag(contactDistance)
        
        if contactDistance > self.radius:
            return None
        
        return Intercept(distance = planeIntersect.distance,
                         point = planeIntersect.point,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class Box(Shape):

    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes=[]
        
        self.size = size
        
        #Sides
        leftPlane = Plane(ml.twoVecSum(self.position, (-self.size[0]/2,0,0)), (-1,0,0), material)
        rightPlane = Plane(ml.twoVecSum(self.position, (self.size[0]/2,0,0)), (1,0,0), material)
        
        bottomPlane = Plane(ml.twoVecSum(self.position, (0,-self.size[1]/2,0)), (0,-1,0), material)
        topPlane = Plane(ml.twoVecSum(self.position, (0,self.size[1]/2,0)), (0,1,0), material)
        
        backPlane = Plane(ml.twoVecSum(self.position, (0,0,-self.size[2]/2)), (0,0,-1), material)
        frontPlane = Plane(ml.twoVecSum(self.position, (0,0,self.size[2]/2)), (0,0,1), material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)
        
        #Bounding Box (agregar limites a los planos infinitos creados)
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
        
        bias = 0.001
        
        for i in range (3):
            self.boundsMin[i] = self.position[i]-(bias+size[i]/2)
            self.boundsMax[i] = self.position[i]+(bias+size[i]/2)
    
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        
        u = 0
        v = 0
        
        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig,dir)
            
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                
                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect
                                
                                #Generar uv's
                                if abs(plane.normal[0]) > 0:
                                    #Este es un plano izquierdo o derecho
                                    #Usar Y y Z para crear uv's, estando en X.
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1]+0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2]+0.002)
                                elif abs(plane.normal[1]) > 0:
                                    #Usar X y Z para crear uv's, estando en Y.
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0]+0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2]+0.002)
                                elif abs(plane.normal[2]) > 0:
                                    #Usar X y Y para crear uv's, estando en Z.
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0]+0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1]+0.002)
                                            
        if intersect is None:
            return None
        
        return Intercept(distance = t,
                         point = intersect.point,
                         normal = intersect.normal,
                         texcoords= (u,v),
                         obj = self)
        
        
class Ellipsoid(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        
        l = ml.twoVecSubstraction(orig,self.position)
        l = ml.divV(l,self.radius)
        dir = ml.divV(dir,self.radius)
        
        a = ml.twoVecDot(dir, dir)
        b = 2.0 * ml.twoVecDot(dir, l)
        c = ml.twoVecDot(l, l) - 1.0
        
        dis = (b**2) - (4*a*c)
    
        if dis < 0:
            return None
        
        t1 = (-b + sqrt(dis)) / (2 * a)
        t2 = (-b - sqrt(dis)) / (2 * a)
        
        if t1 < 0 and t2 <0:
            return None
        
        if t1 < t2:
            t = t1
        else:
            t = t2
            
        p = ml.twoVecSum(orig, ml.vecMultEsc(dir, t))
        
        normal = ml.twoVecSubstraction(p, self.position)
        normal = ml.divV(normal, self.radius)
        normal = ml.vecNorm(normal)
        
        u = 1-((atan2(normal[2], normal[0])+pi)/(2*pi))
        v = ((acos(normal[1])+pi)/2)/pi
        
        return Intercept(distance = t,
                         point = p,
                         normal = normal,
                         texcoords= (u,v),
                         obj = self)
        
