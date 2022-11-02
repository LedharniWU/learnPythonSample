import math
import re
from turtle import st

class PixelInfo:
    r = 0
    g = 0
    b = 0
    a = 0

    def set_r(self, r):
        self.r = r
    
    def set_g(self, g):
        self.g = g
    
    def set_b(self, b):
        self.b = b

    def set_a(self, a):
        self.a = a

    def getAll(self):
        data = {"r":self.r, "g":self.g, "b":self.b, "a":self.a}
        return data

def ColorScaleBCGYR(in_value):
    ret = PixelInfo()
    ret.set_a(255)
    value = in_value
    tmp_val = math.cos(4 * math.pi * value)
    col_val = ( -tmp_val / 2 + 0.5 ) * 255

    if ( value >= (4.0 / 4.0) ) :   # 赤
        ret.set_r(255) 
        ret.set_g(0)
        ret.set_b(0)
    elif ( value >= (3.0 / 4.0) ) : # 黄～赤
        ret.set_r(255)
        ret.set_g(col_val)
        ret.set_b(0)
    elif ( value >= (2.0 / 4.0) ) : # 緑～黄
        ret.set_r(col_val)
        ret.set_g(255)
        ret.set_b(0)
    elif ( value >= (1.0 / 4.0) ) : # 水～緑
        ret.set_r(0) 
        ret.set_g(255)
        ret.set_b(col_val)
    elif ( value >= (0.0 / 4.0) ) : # 水～緑
        ret.set_r(0) 
        ret.set_g(col_val)
        ret.set_b(255)    
    else :                          # 青
        ret.set_r(0) 
        ret.set_g(0)
        ret.set_b(255)


    print("tmp_val = " + str(tmp_val))
    print(ret.getAll())
# ColorScaleBCGYR(0.69)


def ColorScaleThrermoRGBA(x):
    ret = PixelInfo()
    ret.set_a(255)
    r = 0
    g = 0
    b = 0
    i = int(x * 256 - 1)
    
    if ( i < 32 ) :
        r = 0
    elif ( i < 164 ) :
        r = int( (math.cos(math.pi * ( i * 360 / 255.0 - 255 ) / 180.0 ) + 1 ) * 127.5 )
    else :
        r = 255

    if ( i < 96 ) :
        g = 0
    elif ( i < 224 ) :
        g = int( (math.cos(math.pi * ( i * 360 / 255.0 + 45 ) / 180.0 ) + 1 ) * 127.5 )
    else :
        g = 255
    
    if ( i < 128 ) :
        b = int( (math.cos(math.pi * ( i * 720 / 255.0 - 180 ) / 180.0 ) + 1 ) * 127.5 )
    elif ( i < 192 ) :
        b = 0
    else :
        b = int( (math.cos(math.pi * ( i * 720 / 255.0 ) / 180.0 ) + 1 ) * 127.5 )

    ret.set_r(r) 
    ret.set_g(g)
    ret.set_b(b)

    print("I = " + str(i))
    print(ret.getAll())

ColorScaleThrermoRGBA(0.7)