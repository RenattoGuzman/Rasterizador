import mathLibrary as Multi

class Light(object):
  def __init__(self, intensity = 1, color = (1,1,1), ligthType = "None"):
    self.intensity = intensity
    self.color = color
    self.ligthType = ligthType

  def getColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

  def getDiffuseColor(self, intercept):
      return None

  def getSpecularColor(self, intercept, viewPosition):
      return None

class AmbientLight(Light):
  def __init__(self, intensity = 1, color = (1,1,1)):
    super().__init__(intensity, color, "Ambient")

def reflect(normal, direction):
    reflectValue = [2 * Multi.twoVecDot(normal, direction) * n - d for n, d in zip(normal, direction)]
    return Multi.vecNorm(reflectValue)

class DirectionalLight(Light):
    def __init__(self, direction=(0, 1, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Directional")
        self.direction = Multi.vecNorm(direction)

    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = Multi.twoVecDot(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.Ks

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = [i * -1 for i in self.direction]

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = Multi.twoVecSubstraction(viewPosition, intercept.point)
        viewDirection = Multi.vecNorm(viewDirection)

        intensity = max(0, min(1, Multi.twoVecDot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.Ks

        return [i * intensity for i in self.color]
    
class PointLight(Light):
    def __init__(self, position=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Point")
        self.position = position

    def getDiffuseColor(self, intercept):
        direction = Multi.twoVecSubstraction(self.position, intercept.point)
        radius = Multi.vecNormSimple(direction)
        direction = Multi.vecNorm(direction)

        intensity = Multi.twoVecDot(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = Multi.twoVecSubstraction(self.position, intercept.point)
        radius = Multi.vecNormSimple(direction)
        direction = Multi.vecNorm(direction)

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = Multi.twoVecSubstraction(viewPosition, intercept.point)
        viewDirection = Multi.vecNorm(viewDirection)

        intensity = max(0, min(1, Multi.twoVecDot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.Ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]