class RcvMelDirBinDataInfo:
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

    def RcvMelDirBinDataInfo(srcBinData, self):

        max_temp = -999.9
        min_temp = 999.9

        idx = 0

        StCode     = srcBinData[0];            # 0
        Cmd        = srcBinData[(idx:=idx+1)]; # 1
        ans_bit    = srcBinData[(idx:=idx+1)]; # 2
        status     = srcBinData[(idx:=idx+1)]; # 3
        connection = srcBinData[(idx:=idx+1)]; # 4

        idx=idx+1
        AS1_Temp            = self.convertLittleEndianBytesToShort(srcBinData, idx) # 5,6
        idx=idx+2
        AS1_Humidity        = self.convertLittleEndianBytesToShort(srcBinData, idx) # 7,8
        idx=idx+2
        AS1_MelDIR_TEMP_BRD = self.convertLittleEndianBytesToShort(srcBinData, idx) # 9,10
        idx=idx+1

        AS1_MelDIR_THER_OFFSET = srcBinData[(idx:=idx+1)] # 11

        idx=idx+1
        AS1_CalibrationTemp = self.convertLittleEndianBytesToShort(srcBinData, idx) # 12 13
        idx=idx+2 # 14

        AS1_MelDIRtemp = []

        for j in range(0, 4800) :
            AS1_MelDIRtemp.append(self.convertLittleEndianBytesToShort(srcBinData, idx))
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
        print(len(MelDirTempArray))

    RcvMelDirBinDataInfo(BinData)

