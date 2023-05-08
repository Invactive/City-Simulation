# ===============================================#
# Topic: Synthetic data generation for object    #
#        detection systems using Unreal Engine 5 #
# Author: Jakub Grzesiak                         #
# University: Poznan University of Technology    #
# Python version: 3.9.7                          #
# ===============================================#

import os
import pathlib
import subprocess


def install(system: str, package: str) -> None:
    """
    Package installer for Python in Unreal Engine 5.
    Installs package inside Unreal Engine directory.

    Args:
        system (str): System that you are using.
                        Available options:
                        - Linux
                        - Mac
                        - Win64 
        package (str): Package to install
    """
    try:
        pth = pathlib.Path(os.__file__).parents[2] / system / 'python.exe'
        cmd = "\"{}\" -m pip install {}".format(pth, package)
        print(cmd)
        proc = subprocess.run(cmd, capture_output=True)
        if not proc.stderr.decode("utf-8"):
            print("No errors")
        else:
            print(proc.stderr.decode("utf-8"))
            print("STDOUT: ", proc.stdout)
    except Exception as e:
        print(e)

# Examples of use:
# install("Win64", "PyQt5")
# install("Win64", "importlib")
# install("Win64", "unreal")
# install("Win64", "tk")
# install("Win64", "PySide6")

