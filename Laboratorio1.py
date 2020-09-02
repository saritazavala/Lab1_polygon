#Lab 1: Filling any polygon
#Graficas por computador
#Sara Zavala 18893
#Universidad del Valle de Guatemala

import struct 


def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def word(c):
    return struct.pack('=h', c)

# 4 bytes
def dword(c):
    return struct.pack('=l', c)

def color(red, green, blue):
     return bytes([round(blue * 255), round(green * 255), round(red * 255)])


class Render(object):

    #Initial values -------------------------------

    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.framebuffer = []
        self.change_color = color(1,1,1)
        self.filename = filename
        self.x_position = 0
        self.y_position = 0
        self.ViewPort_height = 0
        self.ViewPort_width = 0
        self.glClear()

    
    #File Header ----------------------------------

    def header(self):
        doc = open(self.filename,'bw')
        doc.write(char('B'))
        doc.write(char('M'))
        doc.write(dword(54 + self.width * self.height * 3))
        doc.write(dword(0))
        doc.write(dword(54))
        self.info(doc)
        
        
    #Info header ---------------------------------------

    def info(self, doc):
        doc.write(dword(40))
        doc.write(dword(self.width))
        doc.write(dword(self.height))
        doc.write(word(1))
        doc.write(word(24))
        doc.write(dword(0))
        doc.write(dword(self.width * self.height * 3))
        doc.write(dword(0))
        doc.write(dword(0))
        doc.write(dword(0))
        doc.write(dword(0))
        
        #Image ----------------------------------
        for x in range(self.height):
            for y in range(self.width):
                doc.write(self.framebuffer[x][y])
        doc.close()

    #Cleans a full image with the color defined in "change_color"
    def glClear(self):
        self.framebuffer = [
            [self.change_color for x in range(self.width)]
            for y in range(self.height)
        ]

    #Takes a new color  
    def glClearColor(self, red,blue,green):
        self.change_color = color(red,blue,green)

    #Writes all the doc
    def glFinish(self):
        self.header()
    
    def glColor(self, red, green, blue):
        self.change_color = color(red, green, blue)

    #Draws a point according ot frameBuffer
    def glpoint(self, x, y):
        self.framebuffer[y][x] = self.change_color


    #Creates a window 
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    #Defines the area where will be able to draw
    def glViewPort(self, x_position, y_position,  ViewPort_width, ViewPort_height):
        self.x_position = x_position
        self.y_position = y_position
        self.ViewPort_height = ViewPort_height
        self.ViewPort_width = ViewPort_width
    
    #Compuse el vertex por que me daba error el range
    def glVertex(self, x, y):
        x_temp  = round((x + 1) * (self.ViewPort_width/ 2) + self.x_position)
        y_temp  = round((y + 1) * (self.ViewPort_height/2) + self.y_position)
        self.glpoint(round(x_temp ), round(y_temp ))


    #Codigo basado en codigo visto en clase
    #Dennis Aldana 2020

    def glLine(self, x1, y1, x2, y2):
        x1 = round((x1 + 1) * (self.ViewPort_width * 0.5) + self.x_position)
        y1 = round((y1 + 1) * (self.ViewPort_height * 0.5) + self.y_position)
        x2 = round((x2 + 1) * (self.ViewPort_width * 0.5) + self.x_position)
        y2 = round((y2 + 1) * (self.ViewPort_height * 0.5) + self.y_position)
        
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            
        offset = 0
        threshold = 1
        y = y1
        for x in range(x1, x2):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)
                
            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx
    
    #MODELS --------------------------------------
    '''
    def load_model(self, filename, scale, translate):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)
            for position in range(vcount):
                vi_1 = int(face[position][0]) - 1
                vi_2 = int(face[(position + 1) % vcount][0]) - 1
                
                v1 = model.vertex[vi_1] 
                v2 = model.vertex[vi_2]
                
                x1 = round(v1[0] * scale[0] + translate[0])
                y1 = round(v1[1] * scale[1] + translate[1])
                x2 = round(v2[0] * scale[0] + translate[0])
                y2 = round(v2[1] * scale[1] + translate[1])
                
                self.glLine(x1, y1, x2, y2)
    '''

    #POLYGONS ------------------------------------------

    def glOtherLine(self, x1, y1, x2, y2):
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            
        offset = 0
        threshold = 1
        y = y1
        for x in range(x1, x2):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)
                
            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx
    #Algoritmo referenciado
    #Even–odd rule
    #https://handwiki.org/wiki/Even%E2%80%93odd_rule
    def glIs_inside(self, x,y,points):
        longi  = len(points)
        i = 0
        j = longi - 1
        isInside = False

        for i in range(longi):
            if ((points[i][1] > y) != (points[j][1] >y )) and (x < points[i][0] + (points[j][0] - points[i][0]) * (y - points[i][1])/(points[j][1] - points[i][1])):
                isInside = not isInside
            j = i
        return isInside

    
    def gldraw_polygons(self, points):
        for x in range(self.width):
            for y in range(self.height):
                if(self.glIs_inside(x,y,points)):
                    self.glpoint(x,y)
        


first_polygon = [(165, 380),(185, 360),(180, 330),(207, 345),(233, 330),(230, 360),(250, 380),(220, 385),(205, 410),(193, 383)]
second = [(321, 335),(288, 286),(339, 251),(374, 302)]
third = [(377, 249),(411, 197),(436, 249)]
fourth = [(413, 177), (448, 159),(502, 88),(553, 53),(535, 36),(676, 37),(660, 52),(750, 145),(761, 179),(672, 192),
(659, 214),(615, 214),(632, 230),(580, 230),(597, 215),(552, 214),(517, 144),(466, 180)]

fifth = [(682, 175),(708, 120),(735, 148),(739, 170)]        

r = Render('Poligonos.bmp')
r.glCreateWindow(800, 800)

# --------------------------------------

#Tomo el bote de pintura de este color
r.glClearColor(0,0,0) 
#Echo el bote de pintura y pinto todo
r.glClear()
#Amarillito
r.glColor(0.9,0.7,0.13)
r.gldraw_polygons(first_polygon)

r.glColor(0.19,0.76,0.84)
r.gldraw_polygons(second)

r.glColor(0.19,0.84,0.26)
r.gldraw_polygons(third)

r.glColor(0.97,0.56,0)
r.gldraw_polygons(fourth)
r.glColor(0,0,0)

r.gldraw_polygons(fifth)

r.glFinish()


