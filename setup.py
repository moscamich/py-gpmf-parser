from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import sys

class CustomBuildExt(build_ext):
    def build_extensions(self):
        cpp_flags = ["-std=c++17"]
        link_flags = []
        if sys.platform == "darwin":
            cpp_flags += ["-mmacosx-version-min=11.0"]
            link_flags += ["-stdlib=libc++", "-mmacosx-version-min=11.0"]
        for ext in self.extensions:
            if isinstance(ext, Pybind11Extension):
                ext.extra_compile_args = cpp_flags
                ext.extra_link_args = link_flags
        super().build_extensions()

ext_modules = [
    # Build C files as a static library (no special C++ flags needed!)
    Extension(
        "gpmf_c",
        [
            "gpmf-parser/GPMF_parser.c",
            "gpmf-parser/GPMF_utils.c",
            "gpmf-parser/demo/GPMF_mp4reader.c",
        ],
        include_dirs=[
            "gpmf-parser",
            "gpmf-parser/demo",
        ],
    ),
    # Now build the pybind11 C++ extension and link against the static lib
    Pybind11Extension(
        "py_gpmf_parser.gpmf_parser",
        ["src/gpmf_bindings.cpp"],
        include_dirs=[
            "gpmf-parser",
            "gpmf-parser/demo",
        ],
        libraries=["gpmf_c"],  # Link against the static C library above
        language="c++",
    ),
]

setup(
    name="py_gpmf_parser",
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
    packages=["py_gpmf_parser"],
    package_dir={"py_gpmf_parser": "py_gpmf_parser"},
    zip_safe=False,
)
