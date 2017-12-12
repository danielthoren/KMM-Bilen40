'''
setup.py is run to compile the actual library/module that
is imported in the rest of the project.

Needs Cython3 to build.
Build with: python3 setup.py build_ext --inplace

Generates a modulename.so that can be imported in python3.
"import modulename"
'''
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from os import environ

# All source files needs to be included here.
# Also, the file.pyx need to have the same name as the module name that
# is defined in the extensions variable:
# Extension("modulename"...) = modulename.pyx
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
