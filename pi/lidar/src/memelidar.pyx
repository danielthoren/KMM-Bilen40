'''
Participants:
    Alexander Zeijlon
Last changed:
    07/12-2017
'''

# distutils: language = c++
# distutils: sources = ["src/rplidar_driver.cpp", "src/memeRPlidar.cpp","src/arch/linux/net_serial.cpp","src/arch/linux/timer.cpp","src/hal/thread.cpp"]
# distutils: include_dirs = ["include","src"]

# The above comments are parsed when compiling the wrapper and therefore
# needs to correspond with the definitions in sourcefiles in setup.py.

from cython.operator cimport dereference as deref

from libcpp.memory cimport unique_ptr
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport float
from libcpp cimport bool

# Cython definitions for the contents of the C++ header file that is to be wrapped.
# Each function definition should correspond to a desired python function call
# in the wrapper definitions later on (in cdef class PyLidar).
cdef extern from "memeRPlidar.h" namespace "rp::standalone::rplidar":
  cdef cppclass memeRPlidar:
    memeRPlidar() except +
    bool setup()
    vector[vector[float]] grabData()
    vector[vector[float]] grabNonZeroData()
    void startMotor()
    void startScan()
    void stop()
    void stopMotor()

# Corresponding functions that should be visible in python3.
# When imported in python, an instance is initialized by calling
# modulename.Pylidar() which then will call it's __cinit__() and
# init the actual C++ instance.
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

  def grab_nonzero_data(self):
    return self.c_lidar.grabNonZeroData()

  def start_motor(self):
    self.c_lidar.startMotor()
  def start_scan(self):
    self.c_lidar.startScan()
  def stop(self):
    self.c_lidar.stop()
  def stop_motor(self):
    self.c_lidar.stopMotor()
