from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import shutil

class CustomBuildExt(build_ext):
    def build_extensions(self):
        if not shutil.which("swig"):
            sys.stderr.write("Error: SWIG is required to build this package. Install it and retry.\n")
            sys.exit(1)

        swig_cmd = "swig -python -c++ -o swig_parser_wrap.cxx swig_parser.i"
        print(swig_cmd)
        if os.system(swig_cmd) != 0:
            sys.stderr.write("SWIG compilation failed!\n")
            sys.exit(1)

        super().build_extensions()

# Define the SWIG extension
parser_module = Extension(
    "_swig_parser",
    sources=["swig_parser_wrapper.cxx", "swig_parser.cpp"],
    extra_compile_args=["-std=c++11"]
)

setup(
    name="swig_parser",
    version="0.1.0",
    description="A SWIG-based parser module",
    author="Your Name",
    author_email="your.email@example.com",
    ext_modules=[parser_module],
    cmdclass={"build_ext": CustomBuildExt},  # Custom build_ext to run SWIG
    py_modules=["swig_parser"],  # Ensures Python package recognition
    setup_requires=["setuptools", "wheel"],  # Ensure users have setuptools
)

from distutils.core import setup, Extension

parser_module = Extension("_swig_parser",
                          sources=[
                              "swig_parser_wrap.cxx",
                              "swig_parser.cpp"],
                          extra_compile_args=[
                              "-std=c++11",
                              "-o _swig_parser.so"])

setup(name="swig_parser",
      ext_modules=[parser_module],
      py_modules=["swig_parser"])
