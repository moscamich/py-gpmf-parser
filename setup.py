from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11
import sys

class BuildExt(build_ext):
    """Add C++ build flags for Mac and ensure pybind11 is present."""
    def build_extensions(self):
        cpp_flags = ["-std=c++17"]
        link_flags = []
        if sys.platform == "darwin":
            cpp_flags += ["-mmacosx-version-min=11.0"]
            link_flags += ["-stdlib=libc++", "-mmacosx-version-min=11.0"]

        # Apply to all C++ sources only
        for ext in self.extensions:
            ext.extra_compile_args = cpp_flags
            ext.extra_link_args = link_flags
        super().build_extensions()

ext_modules = [
    Extension(
        "py_gpmf_parser.gpmf_parser",
        sources=[
            "src/gpmf_bindings.cpp",
            "gpmf-parser/GPMF_parser.c",
            "gpmf-parser/GPMF_utils.c",
            "gpmf-parser/demo/GPMF_mp4reader.c",
        ],
        include_dirs=[
            pybind11.get_include(),
            "gpmf-parser",
            "gpmf-parser/demo",
        ],
        language="c++",
    ),
]

setup(
    name="py_gpmf_parser",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
    packages=["py_gpmf_parser"],
    package_dir={"py_gpmf_parser": "py_gpmf_parser"},
    # Version and metadata are in pyproject.toml (PEP 621)!
    zip_safe=False,
)

