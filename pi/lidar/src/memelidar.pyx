# distutils: language = c++
# distutils: sources = ["src/rplidar_driver.cpp", "src/RPlidar.cpp","src/arch/linux/net_serial.cpp","src/arch/linux/timer.cpp","src/hal/thread.cpp"]
# distutils: include_dirs = ["include","src"]
from cython.operator cimport dereference as deref

from libcpp.memory cimport unique_ptr
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport float
from libcpp cimport bool

cdef extern from "myRPLidar.h" namespace "rp::standalone::rplidar":
  cdef cppclass RPlidar:
    #ptrs
    #void *drv
    #funcs
    RPlidar() except +
    bool setup()
    vector[vector[float]] grabData()
    void _startMotor()
    void _startScan()
    void _stop()
    void _stopMotor()

cdef class PyLidar:
  cdef RPlidar* c_lidar
  def __cinit__(self):
    self.c_lidar = new RPlidar();
  def __dealloc__(self):
    del self.c_lidar

  def setup_lidar(self):
    return self.c_lidar.setup()

  def grab_data(self):
    return self.c_lidar.grabData()

  def start_motor(self):
    self.c_lidar._startMotor()
  def start_scan(self):
    self.c_lidar._startScan()
  def stop_scan(self):
    self.c_lidar._stop()
  def stop_motor(self):
    self.c_lidar._stopMotor()
