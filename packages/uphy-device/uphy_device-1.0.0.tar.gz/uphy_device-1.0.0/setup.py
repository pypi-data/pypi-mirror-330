# setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize
from pathlib import Path
import os
import sys
import shutil
import logging


# Copy the uphy install into package data
package_data = {}
if prefix := os.environ.get("LIBUPHY_INSTALL_PATH", None):
    target = Path("uphy/device/server/bin")
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(Path(prefix) / "bin", target)
    package_data["uphy.device.server"] = [
        str(file.relative_to("uphy/device/server")) for file in target.rglob("*")
    ]

    target = Path("uphy/device/share")
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(Path(prefix) / "share" / "uphy", target)
    package_data["uphy.device"] = [
        str(file.relative_to("uphy/device")) for file in target.rglob("*")
    ]
else:
    logging.error("LIBUPHY_INSTALL_PATH not specified")
    exit(-1)

include_dirs = [f"{prefix}/include", "src"]
library_dirs = [f"{prefix}/lib"]
libraries = ["uphy", "erpc", "osal", "upi-host"]

if sys.platform == "win32":
    libraries.extend(["wsock32", "ws2_32", "winmm"])
    server_name = "server.exe"
else:
    server_name = "server"

extensions = [
    Extension(
        name="uphy.device.api",
        sources=["uphy/device/api/*.pyx"],
        include_dirs=include_dirs,
        libraries=libraries,
        library_dirs=library_dirs,
        language="c++",
    ),
]

packages = [
    "uphy.device",
    "uphy.device.api",
    "uphy.device.gui",
    "uphy.device.server",
]

package_data["uphy.device.api"] = ["__init__.pyx", "__init__.pxd"]

setup(
    packages=packages,
    package_data=package_data,
    include_package_data=True,
    ext_modules=cythonize(
        extensions,
        gdb_debug=True,
        language_level="3",
        compiler_directives={
            "c_string_type": "bytes",
            "c_string_encoding": "utf-8",
            "embedsignature": "true",
            "embedsignature.format": "python",
        },
    ),
)
