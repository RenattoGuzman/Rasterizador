#En OpenGl, los shaders se escriben
#en un nuevo lenguaje llamado GLSL
#(Graphics Library Shaders Language)

vertex_shader = '''
#version 450 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoords;
layout(location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 outNormals;
out vec3 worldPos;
out vec3 outPosition;
out vec2 UVs;

void main()
{   
    outNormals = normalize(modelMatrix * vec4(normals, 1.0)).xyz;
    vec4 pos = viewMatrix * vec4(position, 1.0);
    worldPos = pos.xyz;
    outPosition = position;
    UVs = texCoords;
    gl_Position = projectionMatrix * modelMatrix * pos;
}
'''


fragment_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex, UVs);
}
'''

#vec4 newPos = vec4(position.x, position.y + sin(time + position.x)/2, position.z, 1.0);
""" layout(binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);
    intensity = min(1,intensity);
    intensity = max(0,intensity);
    fragColor = texture(tex, UVs) * intensity;
} """


candle_shader  = '''

#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    // Parámetros de la silueta
    float outlineWidth = 0.2;  // Ancho de la silueta
    vec3 outlineColor = vec3(1.0, 1.0, 1.0);  // Color de la silueta en RGB

    // Calcula el borde de la textura
    float texelWidth = 1.0 / textureSize(tex, 0).x;
    vec4 color = texture(tex, UVs);
    vec4 right = texture(tex, UVs + vec2(texelWidth, 0));
    vec4 left = texture(tex, UVs - vec2(texelWidth, 0));
    vec4 top = texture(tex, UVs + vec2(0, texelWidth));
    vec4 bottom = texture(tex, UVs - vec2(0, texelWidth));

    // Diferencia en intensidad entre los píxeles adyacentes
    float diff = length(color - right) + length(color - left) + length(color - top) + length(color - bottom);

    // Si la diferencia es mayor que un umbral, entonces es un borde
    float threshold = 0.1;
    float isEdge = step(threshold, diff);

    // Colorea el borde con el color de la silueta
    vec3 silhouetteColor = mix(color.rgb, outlineColor, isEdge);

    // Combina la textura original con la silueta
    fragColor = vec4(silhouetteColor, 1.0);
}

'''


semaforo_shader = '''

#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 diffuse = vec3(.1,.1,.1);

vec3 specular = vec3(.05,.05,.05);

float s = 20.0;

vec3 camera = vec3(0.0, 0.0, 1.0);

vec3 color(in vec3 light) {
  
    float diffuseWeight =  max( dot(light, outNormals) , 0.0) ;
    vec3 toEye = normalize(camera - worldPos);
    vec3 reflective = reflect(-light, outNormals);
    float sWeight = pow(max(dot(reflective, toEye), 0.0), s);
  
    float cycleTime = 3.0;  // Tiempo total de un ciclo (verde + amarillo + rojo)
    float currentTime = mod(time, cycleTime);

    if (currentTime < cycleTime / 3.0) {
        // Primer tercio del ciclo - verde
        return vec3(0.0, 1.0, 0.0) + diffuseWeight * diffuse + specular * sWeight;  // Verde
    } else if (currentTime < 2.0 * cycleTime / 3.0) {
        // Segundo tercio del ciclo - amarillo
        return vec3(1.0, 1.0, 0.0) + diffuseWeight * diffuse + specular * sWeight;  // Amarillo
    } else {
        // Último tercio del ciclo - rojo
        return vec3(1.0, 0.0, 0.0) + diffuseWeight * diffuse + specular * sWeight;  // Rojo
    }
}

void main()
{
    vec3 light = vec3(0.0, 1.3, 0.0);
    fragColor = vec4(color(light), 0.6);
}'''

platinum_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 diffuse = vec3(.1,.1,.1);

vec3 ambient = vec3(.3, .3, .3);

vec3 specular = vec3(.05,.05,.05);

float s = 20.0;

vec3 camera = vec3(0.0, 0.0, 1.0);

vec3 phong(in vec3 light)
{
  
  float diffuseWeight =  max( dot(light, outNormals) , 0.0) ;
  vec3 toEye = normalize(camera - worldPos);
  vec3 reflective = reflect(-light, outNormals);
  float sWeight = pow(max(dot(reflective, toEye), 0.0), s);
  return ambient + diffuseWeight * diffuse + specular * sWeight;
}

void main()
{
    vec3 light = vec3(0.0, 1.3, 0.0);
    fragColor = vec4(phong(light), 1.0);
}
'''

disco_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 color() {
  
    vec3 color = vec3(0.0, 0.0, 0.0);
  
    color.x = sin(time * 50.0) * outPosition.y + + sin(time * 50.0) * outPosition.x;
    color.y = sin(time * 20.0) * outPosition.y;
    color.z =  sin(time * 7.0) * outPosition.y;
  
    return color;
}

void main()
{
  fragColor = vec4(color(), 1.0);
}
'''


candle_shader = """
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 candleColor(float intensity) {
    // Mapa de color para simular el fuego
    vec3 color = vec3(1.0, 0.5, 0.0) * intensity +
                 vec3(1.0, 0.9, 0.0) * intensity * intensity * 0.8 +
                 vec3(1.0, 1.0, 1.0) * intensity * intensity * intensity * 0.6;

    return color;
}

vec3 color() {
    // Ajusta los valores según la posición y el tiempo para obtener variaciones de colores de fuego
    float intensity = sin(time * 5.0) * 0.5 + 0.5;
    intensity *= smoothstep(0.0, 1.0, length(outPosition.xy));

    return candleColor(intensity);
}

void main()
{
    fragColor = vec4(color(), 1.0);
}

"""


