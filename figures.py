import mathLibrary as Multi

class Intercept(object):
  def __init__(self, distance, point, normal, obj):
    self.distance = distance
    self.point = point
    self.normal = normal
    self.obj = obj

class Shape(object):
  def __init__(self, position, material):
    self.position = position
    self.material = material

  def ray_intersect(self, orig, dir):
    return None
  
  def normal(self, point):
        raise NotImplementedError()

class Sphere(Shape):
  def __init__(self, position, radius, material):
    self.radius = radius
    super().__init__(position, material)
  
  def ray_intersect(self, origin, direction):
    L = Multi.twoVecSubstraction(self.position, origin)
    lengthL = Multi.vecNormSimple(L)
    tca = Multi.twoVecDot(L, direction)
    d = (lengthL**2 - tca**2)**0.5

    if d > self.radius:
      return None
    
    thc = (self.radius**2 - d**2)**0.5

    t0 = tca - thc
    t1 = tca + thc

    if t0 < 0:
      t0 = t1
    
    if t0 < 0:
      return None
    
    multi = Multi.valVecMultiply(t0, direction)
    #Multi.twoVecMultiply(t0, direction)
    P = Multi.twoVecSum(origin, multi)
    normal = Multi.twoVecSubstraction(P, self.position)
    normal = Multi.vecNorm(normal)

    return Intercept(distance = t0,
                     point = P,
                     normal=normal,
                     obj=self)
                     