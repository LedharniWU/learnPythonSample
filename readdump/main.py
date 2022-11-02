import struct
import math

# dump読み込み
f = open('dump.txt', 'r')
data = f.read()

# 内容を配列に保存
dataay = data.split()
print(dataay)


# ファイル閉じ
f.close()

# 偶数要素、奇数要素分割
dataay_o = dataay[0::2]
dataay_t = dataay[1::2]

# print(dataay_o)

# 偶数要素、奇数要素結合
newData = []
k = 0
for dataO in dataay_o:
    newDataSt = dataO + dataay_t[k]
    k += 1
    newData.append(newDataSt)
# print(newData)

# 0x前頭に追加
twNewData = []
for d in newData:
    newD = "0x" + d
    twNewData.append(newD)
# print(twNewData)

hex_s_array = []

# 文字列転16進数
for hex_s in twNewData:
    a = int(hex_s, 16)
    hex_s_array.append(a)
# print(hex_s_array)

# 温度計算式
temp_array = []
for i in hex_s_array:
    temp_array.append((i/(16384-1))*165 - 40)
# print(temp_array)


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
        return {"r":self.r, "g":self.g, "b":self.b, "a":self.a}

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
    print("R = " + str(ret.r))
    print("G = " + str(ret.g))
    print("B = " + str(ret.b))

# ColorScaleBCGYR(0.69)

