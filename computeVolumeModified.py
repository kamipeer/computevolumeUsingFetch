#### import the simple module from the paraview
import matplotlib.pyplot as plt
from paraview.simple import *
from pprint import pprint
import os
import re
#import obtainVolumeFromFile
import subprocess

numbers = re.compile(r'(\d+)')
def numericalSort(value):
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


dir_path = os.path.dirname(os.path.realpath(__file__))
volumeTrack = []
it = 0
os.remove("output.txt")
for root, directories, filenames in os.walk(dir_path + '/particleFolder1'):
	for filename in sorted(filenames, key=numericalSort):
		if(filename.startswith("particles_")):
			undeformedFileNameFolder = os.path.join(root)
			#filePath = undeformedFileNameFolder +"/"+ filename
			filePath = undeformedFileNameFolder + "/" + filename
			print filePath
			#obtainVolumeFromFile(filePath)
			#execfile("obtainVolumeFromFile.py")
			subprocess.call("python obtainVolumeFromFile.py " + filePath + " output.txt ", shell=True)

with open("output.txt") as f:
    volume = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
volume = [x.strip() for x in volume] 

plt.plot(volume)
plt.show()
