input_data = open('./serial_recv_data/serial_recv_01.dat', 'r')

data = input_data.read()

print(data)
# ファイルを閉じる
input_data.close()