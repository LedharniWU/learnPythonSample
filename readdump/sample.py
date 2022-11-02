import math
import numpy as np
import cv2

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

# dump読み込み
f = open('dump.txt', 'r')
data = f.read()

# 内容を配列に保存
BinData = data.split()

# ファイル閉じ
f.close()

def convertLittleEndianBytesToShort(data, startIndex):
    target = [data[startIndex], data[(startIndex:=startIndex+1)]]
    s = "0x" + target[0] + target[1]
    i = int(s, 16)
    return i

def RcvMelDirBinDataInfo(srcBinData):

    max_temp = -999.9
    min_temp = 999.9

    idx = 0

    StCode     = srcBinData[0];            # 0
    Cmd        = srcBinData[(idx:=idx+1)]; # 1
    ans_bit    = srcBinData[(idx:=idx+1)]; # 2
    status     = srcBinData[(idx:=idx+1)]; # 3
    connection = srcBinData[(idx:=idx+1)]; # 4

    idx=idx+1
    AS1_Temp            = convertLittleEndianBytesToShort(srcBinData, idx) # 5,6
    idx=idx+2
    AS1_Humidity        = convertLittleEndianBytesToShort(srcBinData, idx) # 7,8
    idx=idx+2
    AS1_MelDIR_TEMP_BRD = convertLittleEndianBytesToShort(srcBinData, idx) # 9,10
    idx=idx+1

    AS1_MelDIR_THER_OFFSET = srcBinData[(idx:=idx+1)] # 11

    idx=idx+1
    AS1_CalibrationTemp = convertLittleEndianBytesToShort(srcBinData, idx) # 12 13
    idx=idx+2 # 14

    AS1_MelDIRtemp = []

    for j in range(0, 4800) :
        AS1_MelDIRtemp.append(convertLittleEndianBytesToShort(srcBinData, idx))
        idx=idx+2

    crc = [srcBinData[idx], srcBinData[(idx:=idx+1)]]

    Temp = AS1_Temp / ( 16384 - 1 ) * 165 - 40
    Humidity = AS1_Humidity / ( 16384 - 1 ) * 100
    CalibrationTemp = AS1_CalibrationTemp / ( 16384 - 1 ) * 165 - 40

    MelDirTempArray = []

    for d in AS1_MelDIRtemp :
        MelDirTemp = ( (d - 8192) / 30 ) + CalibrationTemp
        MelDirTempArray.append(MelDirTemp)

        if MelDirTemp > max_temp :
            max_temp = MelDirTemp
        elif MelDirTemp < min_temp :
            min_temp = MelDirTemp

    # 色計算
    def TemperatureTo0to1Double(tempArray, upperLimit, lowerLimit) :
        retArray = []

        i     = 0
        range = 0.0
        if ( upperLimit < 0 ) :
            if ( lowerLimit < 0 ) :
                range =  math.fabs(lowerLimit) - math.fabs(upperLimit)
            else :
                return retArray
        else :
            if ( lowerLimit < 0 ) :
                range = math.fabs(lowerLimit) + math.fabs(upperLimit)
            else :
                range = math.fabs(upperLimit) - math.fabs(lowerLimit)
    
        for d in tempArray :
            if ( lowerLimit < 0 ) :
                retArray.append(( d + math.fabs(lowerLimit) ) / range)
            else :
                retArray.append(( d - math.fabs(lowerLimit) ) / range)
        return retArray

    retArray = TemperatureTo0to1Double(MelDirTempArray, max_temp, min_temp)

    def ColorScaleThrermoRGBA(x):        
        r = 0
        g = 0
        b = 0
        a = 255

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
        return [r, g, b, a]
    
    colorImgArray = []
    for x in retArray:
        colorImgArray.append(ColorScaleThrermoRGBA(x))

    imgNpResult = np.array_split(colorImgArray, 80)
    np_ar = np.array(imgNpResult, dtype = np.uint8)
    cv2.imwrite('img_gray.jpg', np_ar)
    

# ------------------------------------PRINT-------------------------------------    
    print("-------センサーデータ要求---------")
    print(StCode)
    print(Cmd)
    print("-------D1~D3----------")
    print(ans_bit)
    print(status)
    print(connection)
    print("-------AS1----------")
    print(AS1_Temp)
    print(AS1_Humidity)
    print(AS1_MelDIR_TEMP_BRD)
    print(AS1_MelDIR_THER_OFFSET)
    print(AS1_CalibrationTemp)
    # print(AS1_MelDIRtemp)
    print("-------crc----------")
    print(crc)
    print("byte数 = " + str(idx + 1))
    print("-------温度算出----------")
    print("Temp            = " + str(Temp))
    print("Humidity        = " + str(Humidity))
    print("CalibrationTemp = " + str(CalibrationTemp))
    print("-------温度配列算出----------")
    # print(MelDirTempArray)
    print("-----------------")
    # print(retArray)
    print("------------カラー配列--------------")
    # print(colorImgArray)
    # print(np_ar)
# ----------------------------------------PRINT---------------------------------

RcvMelDirBinDataInfo(BinData)

