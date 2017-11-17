# distutils: language = c++
# distutils: sources = ["src/rplidar_driver.cpp", "src/memeRPlidar.cpp","src/arch/linux/net_serial.cpp","src/arch/linux/timer.cpp","src/hal/thread.cpp"]
# distutils: include_dirs = ["include","src"]
from cython.operator cimport dereference as deref

from libcpp.memory cimport unique_ptr
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport float
from libcpp cimport bool

cdef extern from "memeRPlidar.h" namespace "rp::standalone::rplidar":
  cdef cppclass memeRPlidar:
    memeRPlidar() except +
    bool setup()
    vector[vector[float]] grabData()
    void startMotor()
    void startScan()
    void stop()
    void stopMotor()

cdef class PyLidar:
  cdef memeRPlidar* c_lidar
  def __cinit__(self):
    self.c_lidar = new memeRPlidar();
  def __dealloc__(self):
    del self.c_lidar

  def setup(self):
    return self.c_lidar.setup()

  def grab_data(self):
    return self.c_lidar.grabData()

  def start_motor(self):
    self.c_lidar.startMotor()
  def start_scan(self):
    self.c_lidar.startScan()
  def stop(self):
    self.c_lidar.stop()
  def stop_motor(self):
    self.c_lidar.stopMotor()
