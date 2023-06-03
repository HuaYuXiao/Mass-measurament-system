import os
import glob
import pandas as pd
import fileinput
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
from tsmoothie.smoother import *


def deltxt():
    txt_files = glob.glob("*.txt")

    newest_file = max(txt_files, key=os.path.getmtime)

    for file in txt_files:
        if file != newest_file:
            os.remove(file)


def txt2df():
    file_list = [file for file in os.listdir() if file.endswith('.txt')]

    for file in file_list:
        with fileinput.FileInput(file, inplace=True) as f:
            for line_number, line in enumerate(f, 1):
                if line_number != 1:
                    print(line, end='')

    df = pd.read_csv(file, delimiter='\t')

    return df


def find(df):
# 骤降的阈值，根据实际情况调整
    threshold = -0.1  
    index_of_drop = df[df < threshold].index[0]
    df = df.loc[:index_of_drop-10]

    return df


def filter(df):
    _, axs = plt.subplots(2, 2)

    plot(df, axs[0, 0],'original')

    measurements = df.values

    filter = KalmanFilter()
    filtered_state_means, _ = filter.filter(measurements)
    filtered_values = filtered_state_means[:, 0]
    df = pd.DataFrame(filtered_values, columns=['Filtered_Data'])

    plot(df, axs[0, 1],'KalmanFilter')

    df = df.rolling(20, center=True).mean()

    plot(df, axs[1, 0],'MeanFilter')

    smoother = KalmanSmoother(component='level_trend',component_noise={'level': 0.1, 'trend': 0.1}) 
    df = smoother.smooth(df).smooth_data.T

    plot(df, axs[1, 1],'KalmanSmoother')

    plt.show()

    df = df[5:-5]

    return df


def calmass(df):
    para_a =  -243.8885141731842
    para_b =  311.271972539197
    para_c =  0.04298453883976162

    df = df['ay(g)']

    df = find(df)

    df = filter(df)
    
    acc = df.mean() * 9.7803
    print(acc)

    mass = para_a + para_b / (acc + para_c)
    print(mass)
    
    return mass


def plot(df,ax,title):
    ax.plot(df)
    ax.set_xlabel('Time')
    ax.set_ylabel('ay(m/s^2)')
    ax.set_title(title)
