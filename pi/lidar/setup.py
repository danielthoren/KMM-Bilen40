from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from os import environ
#environ["CC"] = "g++"
#environ["CXX"] = "g++"

#pyx-filen måste ha samma namn som modulen som kompileras.
sourcefiles = ['src/memelidar.pyx',
                'src/rplidar_driver.cpp',
                'src/memeRPlidar.cpp',
                'src/arch/linux/net_serial.cpp',
                'src/hal/thread.cpp']

include_dirs = ['include', 'src']

extensions = [Extension("memelidar", sourcefiles, include_dirs = include_dirs)]

setup(
    ext_modules = cythonize(extensions)
)
