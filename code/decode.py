import serial
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import numpy as np

warnings.filterwarnings('ignore')


def setup(port, baudrate):
    ser = serial.Serial(port=port,
                        baudrate=baudrate,
                        bytesize=serial.SEVENBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        timeout=1)

    return ser


def rsv_raw(ser, length):
    mark = ser.read(1)
    result=b''
    if(mark==b'Q'):
        result=ser.read(length)
    if result!=b'':     
        return result


def decode_data(data):
    print(data)

    a=3
    b=5
    c=7

    acc_x = int.from_bytes(data[a:a+1], byteorder='big', signed=True)
    acc_y = int.from_bytes(data[b:b+1], byteorder='big', signed=True)
    acc_z = int.from_bytes(data[c:c+1], byteorder='big', signed=True)

    # acc_x /= 32768.0 * 16.0
    # acc_y /= 32768.0 * 16.0
    # acc_z /= 32768.0 * 16.0

    # acc_x = round(acc_x, 4)
    # acc_y = round(acc_y, 4)
    # acc_z = round(acc_z, 4)

    print(data[a:a+1],acc_x,data[b:b+1],acc_y,data[c:c+1],acc_z)

    return acc_x, acc_y, acc_z


def plot(length,acc_x_list, acc_y_list, acc_z_list):
    if len(acc_x_list) > length:
        acc_x_list = acc_x_list[-length:]
        acc_y_list = acc_y_list[-length:]
        acc_z_list = acc_z_list[-length:]
    plt.cla()

    plt.xlim(0, 20)
    plt.xticks(np.arange(0, 21, 1))
    # plt.ylim(-120, 120)
    # plt.yticks(np.arange(-120, 121, 10))

    plt.plot(acc_x_list, label="acc_x")
    plt.plot(acc_y_list, label="acc_y")
    plt.plot(acc_z_list, label="acc_z")

    plt.xlabel("Time")
    plt.ylabel("Acceleration")
    plt.title("Real-time Plot")
    plt.legend()
    plt.pause(0.01)


if __name__ == "__main__":
    ser = setup("COM9", 115200)
    acc_x_list = []
    acc_y_list = []
    acc_z_list = []

    plt.ion()  # 开启交互模式
    fig, ax = plt.subplots()

    while True:
        data = rsv_raw(ser, 9)
        if data is not None:
            acc_x, acc_y, acc_z = decode_data(data)
            acc_x_list.append(acc_x)
            acc_y_list.append(acc_y)
            acc_z_list.append(acc_z)


            plot(20,acc_x_list, acc_y_list, acc_z_list)

        ax.set_xlim([max(0, len(acc_x_list) - 10), len(acc_x_list) + 1])
        plt.show(block=False)
