import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn
import sys
from scipy import signal
pd.options.mode.chained_assignment = None  # default='warn'

cutoff = 5 # in Hz
fs = 98 # sampling frequency


def get_sampling_rate(x):
    # Calculate sampling rate (rounded to nearest integer) based on recorded data
    # [IN]
    #  x: Series containing the relative time values (from 0-##.##)
    # [OUT]
    #  fs: samples per second, Hz 
    return round(len(x.index) / x.iloc[-1])


def read_data(data):
    seaborn.set()
    df = pd.read_csv(data)
    # Filtering dataset
    df = df[df.time != 'Time'] # there were 'time' values in the Time column
    df = df.drop([0]) # OPTIONAL: drop the first value because there is a gap between the starting time and the subsequent time
    df = df.reset_index(drop=True)

    # Convert date into a DateTime object
    # https://stackoverflow.com/questions/38110263/in-pandas-how-to-convert-a-string-to-a-datetime-object-with-milliseconds
    df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%d %H:%M:%S.%f")
    return df

def calc_time(data):
    # Calculating the time difference between each data point
    # https://stackoverflow.com/questions/53690587/how-to-get-the-difference-between-first-row-and-current-row-in-pandas
    a = np.array([], dtype=np.int64)
    for i in data.index:
        epoch = data['time'][i].timestamp()
        a = np.append(a, epoch)

    df_a=pd.DataFrame({'time': a})

    data['time'] =  df_a.iloc[1:, 0] - df_a.iat[0, 0]

    # Changing time[0] = 0 and drop any rows larger than 60 seconds
    data['time'][0] = 0
    data = data[data.time <= 60]

    # Calculate total acceleration and add to df
    total_acc = (data['ax'] ** 2 + data['ay'] ** 2 + data['az'] ** 2) ** (1/2)
    data['atotal'] = total_acc
    return data

def butterworth_lowpass(df):
    nyq = 0.5 * fs
    normalized_cutoff = cutoff / nyq
    b, a = signal.butter(3, normalized_cutoff, btype='lowpass')
    return signal.filtfilt(b, a, df)

# Overlay plots before and after transform
def overlay(df, df2):
    plt.figure(figsize=(10,5))
    plt.title('x Acceleration')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.plot(df['time'].values, df['ax'].values, 'r-', linewidth=1)
    plt.plot(df2['time'].values, df2['ax'].values, 'b-', linewidth=1)

    plt.figure(figsize=(10,5))
    plt.title('y Acceleration')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.plot(df['time'].values, df['ay'].values, 'r-', linewidth=1)
    plt.plot(df2['time'].values, df2['ay'].values, 'b-', linewidth=1)

    plt.figure(figsize=(10,5))
    plt.title('z Acceleration')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.plot(df['time'].values, df['az'].values, 'r-', linewidth=1)
    plt.plot(df2['time'].values, df2['az'].values, 'b-', linewidth=1)

    plt.figure(figsize=(10,5))
    plt.title('Total Acceleration')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.plot(df['time'].values, df['atotal'].values, 'r-', linewidth=1)
    plt.plot(df2['time'].values, df2['atotal'].values, 'b-', linewidth=1)
    plt.show()

def get_velocity_and_distance(df):
    # Returns the average speed (m/s) and the total distance walked (m) from the dataset
    # [IN]
    # df: dataframe
    # [OUT]
    # 2 variables: speed (the average speed (m/s) and the total distance walked (m)
    # Velocity: Δv = a⋅Δt 
    # Displacement: Δp = v⋅Δt.
    df_shift = df.shift(1)
    time_diff = df['time'] - df_shift['time']
    vx_diff = time_diff * df['ax']
    # vy_diff = time_diff * df['ay']
    # vz_diff = time_diff * df['az']
    # vtotal_diff = time_diff * df['atotal']

    # temp = pd.DataFrame({'vx_diff': vx_diff, 'vy_diff': vy_diff, 'vz_diff': vz_diff, 'vtotal_diff': vtotal_diff})
    temp = pd.DataFrame({'vx_diff': vx_diff})
    # temp['vx_diff'][0] = temp['vy_diff'][0] = temp['vz_diff'][0] = temp['vtotal_diff'][0] = 0
    temp['vx_diff'][0] = 0
    data = df.join(temp)

    # data['vx'] = data['vy'] = data['vz'] = data['vtotal'] = 0
    data['vx'] = 0

    # Calculate final velocity: Δv + initial velocity
    for i in data.index:
        data.loc[i, 'vx'] = data.iloc[i]['vx_diff'] + data.iloc[i-1]['vx']
        # data.loc[i, 'vy'] = data.iloc[i]['vy_diff'] + data.iloc[i-1]['vy']
        # data.loc[i, 'vz'] = data.iloc[i]['vz_diff'] + data.iloc[i-1]['vz']
        # data.loc[i, 'vtotal'] = data.iloc[i]['vtotal_diff'] + data.iloc[i-1]['vtotal']

    # Calculate distance walked: v⋅Δt
    data['distance_walked'] = data['vx'] * time_diff

    speed = data['vx'].mean()
    distance = data['distance_walked'].sum()
    return(speed, distance)

def main(input):
    
    data = read_data(input)
    data = calc_time(data)

    fs = get_sampling_rate(data['time'])
    df_accel = data[['ax','ay','az', 'atotal']].copy()
    df_accel = df_accel.apply(butterworth_lowpass, axis=0)
    df_accel = df_accel.join(data['time'])
    df_accel = df_accel[['time', 'ax', 'ay', 'az', 'atotal']]
    # overlay(data, df_accel)


    stats = get_velocity_and_distance(df_accel)


    speed = stats[0]
    print("The average walking speed (in m/s) is:", speed)
    distance = stats[1]
    print("The distance covered (in m) is:", distance)
    
    

    # python3 main.py 'filename'


if __name__ == '__main__':
    main(sys.argv[1])