from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import sys

class CustomBuildExt(build_ext):
    """Custom build_ext to add platform-specific compiler flags."""
    def build_extensions(self):
        cpp_flags = ["-std=c++17"]
        link_flags = []
        if sys.platform == "darwin":
            cpp_flags += ["-mmacosx-version-min=11.0"]
            link_flags += ["-stdlib=libc++", "-mmacosx-version-min=11.0"]

        for ext in self.extensions:
            # Use dict to avoid passing C++ flags to C sources!
            ext.extra_compile_args = {
                "cxx": cpp_flags,
                "c":   [],
            }
            ext.extra_link_args = link_flags
        super().build_extensions()

ext_modules = [
    Pybind11Extension(
        "py_gpmf_parser.gpmf_parser",  # Ensures it installs in package dir
        [
            "src/gpmf_bindings.cpp",
            "gpmf-parser/GPMF_parser.c",
            "gpmf-parser/GPMF_utils.c",
            "gpmf-parser/demo/GPMF_mp4reader.c",
        ],
        include_dirs=[
            "gpmf-parser",
            "gpmf-parser/demo",
        ],
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
