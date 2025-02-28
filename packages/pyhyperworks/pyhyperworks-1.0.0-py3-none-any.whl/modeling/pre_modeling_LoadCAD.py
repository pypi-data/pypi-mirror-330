import sys
import os
import ansa
import json
import time

fileName = os.path.basename(__file__)
groupTitle = fileName.split(".")[0].split("_")[1]
btnTitle = "_".join(fileName.split(".")[0].split("_")[2:])
#
def LoadCAD():
	'''
        Name:CreateContacts
        Description: Opens an assist window where the user
             select from the screen or properties. The
             script will then create sets, GEB_SB and contact between
             the parts. In the case that a part changes by 
             re-applying the GEB the sets are updated.
	'''
	print("loadcad.py name:",__file__)
	return
