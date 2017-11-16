from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

sourcefiles = ['src/memelidar.pyx',
                'src/rplidar_driver.cpp',
                'src/RPlidar.cpp',
                'src/arch/linux/net_serial.cpp',
                'src/hal/thread.cpp']

include_dirs = ['include', 'src']

extensions = [Extension("memelidar", sourcefiles, include_dirs = include_dirs)]

setup(
    ext_modules = cythonize(extensions)
)
