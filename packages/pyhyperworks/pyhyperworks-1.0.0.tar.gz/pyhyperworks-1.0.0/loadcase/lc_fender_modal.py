import sys
import os
import json
import time
import ansa
from ansa import *

fileName = os.path.basename(__file__)
groupTitle = fileName.split(".")[0].split("_")[1]
btnTitle = "_".join(fileName.split(".")[0].split("_")[2:])
#
@ansa.session.defbutton(groupTitle, btnTitle)
def main():
    print("Running "+fileName)