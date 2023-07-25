from gl import Renderer, V3, V2, color

width = 900
height = 500

rend = Renderer(width, height)


vertices = [V2(165, 380), V2(185, 360),V2 (180, 330),V2 (207, 345) ,V2(233, 330) ,V2(230, 360) ,V2(250, 380) ,V2(220, 385), V2(205, 410) , V2(193, 383)]
rend.glPoligono(vertices, color(1,0,0))

vertices1 = [V2(321, 335), V2(288, 286), V2(339, 251), V2(374, 302)]
rend.glPoligono(vertices1, color(1,0.5,0))

vertices2 = [V2(377, 249), V2(411, 197), V2(436, 249)]
rend.glPoligono(vertices2, color(1,1,0.3))

vertices3 = [
    V2(413, 177), V2(448, 159), V2(502, 88), V2(553, 53), V2(535, 36), V2(676, 37), V2(660, 52),
    V2(750, 145), V2(761, 179), V2(672, 192), V2(659, 214), V2(615, 214), V2(632, 230), V2(580, 230),
    V2(597, 215), V2(552, 214), V2(517, 144), V2(466, 180)
]
rend.glPoligono(vertices3,color(0,0.5,0.5))


rend.glFinish("outputColor.bmp")

print("Revisa el archivo")