import os
import sys
from setuptools import setup

# OS-specific external Darknet library locations.
if os.name == "posix":
    # POSIX systems (Linux/macOS)
    libpath = "/usr/lib/libdarknet.so"
elif os.name == "nt":
    # Windows systems
    libpath = r"C:\Program Files\darknet\bin\darknet.dll"
else:
    sys.exit("Unsupported operating system.")

# Optional: Warn users if the external Darknet library does not seem to be installed.
if not os.path.exists(libpath):
    print(
        f"Warning: Expected Darknet library not found at {libpath}.\n"
        "Please install Darknet (or ensure its library is in the correct location) "
        "before using this package."
    )

setup(
    name="darknet-hankai",
    version="3.0.0",
    description="Python bindings for Darknet",
    license="Apache-2.0",
    py_modules=["darknet"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ]
)
