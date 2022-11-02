import math
import numpy as np
from FileHelper import *

class egna_info():
    """
    """
    def __init__(self):
        """
        """
        self.egna_info = {
            "stx"         : None,
            "cmd"         : None,
            "ans"         : None,
            "sta"         : None,
            "con"         : None,
            "as1_tmp"     : None,
            "as1_hum"     : None,
            "as1_mel_brd" : None,
            "as1_mel_thr" : None,
            "as1_cal"     : None
        }

        self.tempture = None
        self.humidity = None
        self.calibration_tempture = None
        self.max_tempture = None
        self.min_tempture = None
        self.meldir_data = []

        self.filename = None
        self.width = None
        self.height = None

    def parse_egna_info(self, data):
        """
        """
        index = 0
        self.egna_info["stx"] = data[index]; index+=1
        self.egna_info["cmd"] = data[index]; index+=1
        self.egna_info["ans"] = data[index]; index+=1
        self.egna_info["sta"] = data[index]; index+=1
        self.egna_info["con"] = data[index]; index+=1

        self.egna_info["as1_tmp"] = int.from_bytes([data[index], data[index+1]],'big'); index+=2
        self.egna_info["as1_hum"] = int.from_bytes([data[index], data[index+1]], 'big'); index+=2
        self.egna_info["as1_mel_brd"] = int.from_bytes([data[index], data[index+1]], 'big'); index+=2
        self.egna_info["as1_mel_thr"] = data[index]; index+=1
        self.egna_info["as1_cal"] = int.from_bytes([data[index], data[index+1]], 'big'); index+=2

        mel_temp = []
        for i in range(4800):
            mel_temp.append(int.from_bytes([data[index], data[index+1]], 'big')); index+=2
        self.egna_info["as1_mel_tmp"] = mel_temp
        print(self.egna_info["as1_mel_tmp"])

        self.tempture = self.egna_info["as1_tmp"] / ( 16384 - 1 ) * 165 - 40
        self.humidity = self.egna_info["as1_hum"] / ( 16384 - 1 ) * 100
        self.calibration_tempture = self.egna_info["as1_cal"] / ( 16384 - 1 ) * 165 - 40

        for d in self.egna_info["as1_mel_tmp"]:
            temp = (d - 8192) / 30 + self.calibration_tempture
            self.meldir_data.append(temp)
        self.max_tempture = max(self.meldir_data)
        print(self.max_tempture)
        self.min_tempture = min(self.meldir_data)
        print(self.min_tempture)

    def create_meldir_image(self):
        """
        """

        img_data_array = bytearray()
        for d in self.meldir_data:
            mid = (self.max_tempture + self.min_tempture) / 2
            sig_input = d - mid
            if (sig_input == 0) :
                pass
            else :
                sig_input = sig_input / ((self.max_tempture - self.min_tempture) / 12)

            sig_out = 1 / (1 + math.e**-sig_input)
            c = sig_out * 255
            if ( c <= 50):
                c = 0
            else:
                pass

            img_data_array.append(int(c))
            img_data_array.append(int(c))
            img_data_array.append(int(c))

        self._create_bmp(img_data_array)

    def set_melder_info(self, width, height):
        """
        """
        self.width = width
        self.height = height

    def set_filename(self, filename):
        """
        """
        self.filename = filename

    def _create_bmp(self, data):
        """
        """

        try:
            header_size = 0x0e
            info_header_size = 0x28
            data_size = len(data)
            file_total_size = header_size + info_header_size + data_size

            f = open(self.filename, 'wb')

            # file header
            b = bytearray([0x42, 0x4d])
            b.extend(file_total_size.to_bytes(4, 'little'))
            b.extend((0).to_bytes(2, 'little'))
            b.extend((0).to_bytes(2, 'little'))
            b.extend((header_size + info_header_size).to_bytes(4, 'little'))

            # information header
            b.extend((0x28).to_bytes(4, 'little'))
            b.extend(self.width.to_bytes(4, 'little'))
            b.extend(self.height.to_bytes(4, 'little'))
            b.extend((1).to_bytes(2, 'little'))
            b.extend((24).to_bytes(2, 'little'))
            b.extend((0).to_bytes(4, 'little'))
            b.extend(data_size.to_bytes(4, 'little'))
            b.extend((0).to_bytes(4, 'little'))
            b.extend((0).to_bytes(4, 'little'))
            b.extend((0).to_bytes(4, 'little'))
            b.extend((0).to_bytes(4, 'little'))

            # data body
            for i in range(60, 0, -1):
                for j in range(80*3):
                    b.extend(data[80*3*(i-1)+j].to_bytes(1,'big'))
            f.write(b)
        except:
            pass

        finally:
            f.close()



f = FileHelper()
f.set_fileName("serial_recv_01.dat")
f.readFile()
egna = egna_info()
egna.set_filename("serial_recv_01.bmp")
egna.set_melder_info(80, 60)
egna.parse_egna_info(f.results)
egna.create_meldir_image()