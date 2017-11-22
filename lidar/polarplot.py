import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import memelidar
import time


def radian(degree):
    return degree * np.pi/180

def draw():
    lidar = memelidar.PyLidar()
    if not lidar.setup_lidar():
        return
    lidar.start_motor()
    lidar.start_scan()
    time.sleep(1)
    print("done waiting")
    array = np.array(lidar.grab_data())
    lidar.stop_scan()
    lidar.stop_motor()

    print(array)

    maxdist = 0;
    ax = plt.subplot(111,projection='polar')
    for elem in array:
        #if elem[3] > 0:
        r = elem[2]
        if r > maxdist:
            maxdist = r
        theta = radian(elem[1])
        ax.plot(theta, r, marker = 'o', markersize=2, color="red")
    ax.set_rmax(maxdist)
    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    matplotlib.use('Agg')
    draw()
