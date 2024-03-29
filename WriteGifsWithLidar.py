#!/usr/bin/env python3
'''Animates distances and measurment quality'''
#from rplidar import RPLidar
from adafruit_rplida import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from datetime import datetime

PORT_NAME = '/dev/ttyUSB0'
DMAX = 2000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    #try:
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                        cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(False)
    iterator = lidar.iter_scans(max_buf_meas=100, min_len=5)
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    f = r"../../pictures/0.gif" 
    
    writergif = animation.PillowWriter(fps=30) 
    ani.save(f, writer=writergif)
    #plt.savefig('0.png')
    lidar.stop()
    lidar.disconnect()

    #except Exception:
    #    lidar.stop()
    #    lidar.disconnect()
    
if __name__ == '__main__':


    while True:
        run()