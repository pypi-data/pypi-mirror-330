import os
import subprocess
import sys
from shutil import which
from typing import List
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools_scm import get_version


ROOT_DIR = os.path.dirname(__file__)


def is_ninja_available() -> bool:
    return which("ninja") is not None


def get_path(*filepath) -> str:
    return os.path.join(ROOT_DIR, *filepath)


def get_requirements() -> List[str]:
    """Get Python package dependencies from requirements.txt."""
    with open(get_path("requirements.txt")) as f:
        requirements = f.read().strip().split("\n")
    return requirements


class CMakeExtension(Extension):
    def __init__(self, name: str, cmake_lists_dir: str = '.', **kwa) -> None:
        super().__init__(name, sources=[], **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class cmake_build_ext(build_ext):
    def compute_num_jobs(self):
        try:
            num_jobs = len(os.sched_getaffinity(0))
        except AttributeError:
            num_jobs = os.cpu_count()
        return num_jobs

    def configure(self, ext: CMakeExtension) -> None:
        # Select build type
        cfg = "Debug" if self.debug else "RelWithDebInfo"
        
        # Where .so files will be written
        outdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = [
            f'-DCMAKE_BUILD_TYPE={cfg}',
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={outdir}',
            f'-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY={self.build_temp}',
            f'-DVIDUR_PYTHON_EXECUTABLE={sys.executable}',
            '-DCMAKE_POSITION_INDEPENDENT_CODE=ON',
        ]

        # Setup build tool
        if is_ninja_available():
            num_jobs = self.compute_num_jobs()
            build_tool = ['-G', 'Ninja']
            cmake_args += [
                '-DCMAKE_JOB_POOL_COMPILE:STRING=compile',
                f'-DCMAKE_JOB_POOLS:STRING=compile={num_jobs}',
            ]
        else:
            build_tool = []

        subprocess.check_call(
            ['cmake', ext.cmake_lists_dir, *build_tool, *cmake_args],
            cwd=self.build_temp)

    def build_extensions(self) -> None:
        # Ensure CMake is present
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        # Create build directory
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Build extensions
        for ext in self.extensions:
            self.configure(ext)
            num_jobs = self.compute_num_jobs()
            
            # Build both targets
            build_args = ['--build', '.', '--target', 'vidur', '_native', '-j', str(num_jobs)]
            subprocess.check_call(['cmake', *build_args], cwd=self.build_temp)


# Define extensions
ext_modules = [CMakeExtension(name="vidur._native")]

setup(
    author="Systems for AI Lab, Georgia Tech; Microsoft Corporation",
    python_requires='>=3.10',
    description="A LLM inference cluster simulator",
    keywords='Simulator, LLM, Inference, Cluster',
    name='vidur',
    packages=find_packages(include=['vidur', 'vidur.*']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://mlsys.org/virtual/2024/poster/2667',
    version=get_version(),
    install_requires=get_requirements(),
    ext_modules=ext_modules,
    cmdclass={'build_ext': cmake_build_ext},
    entry_points={
        "console_scripts": [
            "vidur-data = vidur.cli.data_cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)