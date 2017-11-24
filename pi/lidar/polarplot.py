import matplotlib.pyplot as plt
import numpy as np
import memelidar
import matplotlib.animation as animation

RMAX = 9000
IMIN = 0
IMAX = 50

def run():
    plt.cla()
    data = lidar.grab_data()
    for elem in data:
        if elem[3] > 0:
            plt.plot(np.radians(elem[1]), elem[2], marker='o',markersize=1, color='red')




if __name__ == "__main__":
    count = 0
    plt.ion()
    lidar = memelidar.PyLidar()
    lidar.start_motor()
    lidar.start_scan()
    fig = plt.figure()
    ax = plt.subplot(111,projection='polar')
    line = ax.scatter([0,0], [0,0], s=5,
        c=[IMIN,IMAX],
        cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(RMAX)
    ax.grid(True)
    while True:
        try:
            count +=1
            print("grabbing scan", count )
            run()
            plt.pause(0.000001)
            plt.draw()
        except KeyboardInterrupt:
            lidar.stop()
            lidar.stop_motor()
            break
