import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('acceleration_data.csv')
time = data['Time (s)'].tolist()
LAx = np.around(data['Linear Acceleration x (m/s^2)'].tolist(),5).tolist()
LAy = np.around(data['Linear Acceleration y (m/s^2)'].tolist(),5).tolist()
LAz = np.around(data['Linear Acceleration z (m/s^2)'].tolist(),5).tolist()
absolute = np.around(data['Absolute acceleration (m/s^2)'].tolist(),5).tolist()

axes = [LAx, LAy, LAz]
colors = ['cornflowerblue', 'orchid', 'darkorange']
labels = ['X', 'Y', 'Z']

fig, graphs = plt.subplots(len(axes), sharex=True)

i = 0
while i < len(axes):
    graphs[i].plot(time,axes[i], color = colors[i])
    graphs[i].plot([0, time[-1]], [0, 0], color = 'black')
    graphs[i].set_ylim([-25,25])
    i += 1


# data analysis
# Rule: For each axis, each step is counted as when the acceleration crosses from positive to negative, then negative to positive 
steps_list = []
i = 0
while i < len(axes):
    LA = axes[i]
    LA_temp = [] 
    for value in axes[i]:
        LA_temp.append(abs(value))
    steps = 0
    primer = False
    j = 0
    prev = 0
    avg = sum(LA_temp)/len(LA_temp)
    scalar = 3
    if sum(axes[i]) < 0:
        directional_constant = -1
    else:
        directional_constant = 1
    print(sum(axes[i]))
    while j < len(time):
        if directional_constant * LA[j] < -0.2 * scalar * avg:
            primer = True
        if directional_constant * LA[j] > scalar * avg and primer:
            primer = False
            steps += 1
            graphs[i].plot(time[j],24.5, marker = '|', color = 'red', markersize=2)
        # print("prev = "+str(prev)+" | new = "+str(LA[j])+" | "+str(primer)+" | "+str(steps))
        prev = LA[j]
        j += 1
    graphs[i].plot([0,time[-1]],[directional_constant*scalar*avg,directional_constant*scalar*avg], color = 'limegreen')
    graphs[i].plot([0,time[-1]],[directional_constant*-0.2*scalar*avg,directional_constant*-0.2*scalar*avg], color = 'blue')
    graphs[i].set(ylabel=str(labels[i])+" Steps: "+str(int(steps/2)))

    print(steps)
    print(avg)
    print(directional_constant)
    print("-----------")
    steps_list.append(int(steps/2))
    i += 1

steps_averaged = sum(steps_list)/len(steps_list)
fig.suptitle('Steps calculated per axis | '+str(int(steps_averaged))+' steps taken')
plt.xlabel("Time (s)")
plt.show(block = True)