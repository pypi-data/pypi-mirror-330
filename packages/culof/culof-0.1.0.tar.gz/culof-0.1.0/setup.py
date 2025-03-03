#!/usr/bin/env python3
"""
Setup script for cuLOF package.
"""

import os
import sys
import platform
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        # Check for CMake
        try:
            subprocess.check_call(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the extension. "
                "Please install CMake 3.18+ and try again."
            )

        # Check for CUDA
        try:
            nvcc_output = subprocess.check_output(['nvcc', '--version']).decode('utf-8')
            print(f"Found CUDA: {nvcc_output.strip()}")
        except (OSError, subprocess.SubprocessError):
            raise RuntimeError(
                "CUDA not found. This package requires CUDA 11.0+ to build. "
                "Please install CUDA toolkit from https://developer.nvidia.com/cuda-downloads "
                "and make sure nvcc is in your PATH."
            )

        # Print build environment information
        print(f"Python: {sys.version}")
        print(f"Platform: {platform.platform()}")
        print(f"Compiler: {self.compiler.compiler_type}")
        
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        
        # Required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}',
            f'-DPYTHON_EXECUTABLE={sys.executable}',
            '-DBUILD_PYTHON=ON',
            '-DBUILD_TESTS=OFF',
        ]

        # Set build type
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        # CMake lets you override the generator - we need to ensure we use the same
        # one that was used to compile Python.
        cmake_args += [f'-DCMAKE_BUILD_TYPE={cfg}']

        # Assuming Windows and not cross-compiling
        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
                cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            build_args += ['--', '-j4']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())

        # Make directory if it doesn't exist
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        print(f"Building in {self.build_temp}")
        print(f"CMake args: {cmake_args}")
        
        # Build the project
        try:
            subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
            subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
            print(f"Build successful! Extension will be installed to {extdir}")
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")
            raise RuntimeError(
                f"Error building the extension: {e}\n"
                "Please check that you have the required dependencies:\n"
                "- CUDA Toolkit 11.0+\n"
                "- CMake 3.18+\n"
                "- C++14 compatible compiler\n"
                "For detailed installation instructions, see https://github.com/Aminsed/cuLOF"
            ) from e

# Read the long description from README.md 
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='culof',
    version='0.1.0',
    author='Amin Sedaghat',
    author_email='amin32846@gmail.com',
    description='CUDA-accelerated Local Outlier Factor implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Aminsed/cuLOF',
    project_urls={
        'Bug Tracker': 'https://github.com/Aminsed/cuLOF/issues',
        'Documentation': 'https://github.com/Aminsed/cuLOF',
        'Source Code': 'https://github.com/Aminsed/cuLOF',
    },
    packages=find_packages(),
    ext_modules=[CMakeExtension('culof')],
    cmdclass=dict(build_ext=CMakeBuild),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.15.0',
        'matplotlib>=3.0.0',
        'scikit-learn>=0.22.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: C++',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Environment :: GPU :: NVIDIA CUDA',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='anomaly detection, outlier detection, cuda, gpu, lof, local outlier factor',
) 