from vtk import *
from math import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import csv
import re

numbers = re.compile(r'(\d+)')
def numericalSort(value):
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts


plot_lines = []					
fileNumber = 0
idMinZ = 0
idMaxZ = 0
length_init = 0
length_end = 0
glsValues = []
timeSeries = []
time = 0
minZAfter = 0
maxZAfter = 0

dir_path = os.path.dirname(os.path.realpath(__file__))
for root, directories, filenames in os.walk(dir_path + '/particleFolder2'):
	for filename in sorted(filenames, key=numericalSort):
		if(filename.startswith("particles_")):
			undeformedFileNameFolder = os.path.join(root)
			with open('particleFolder2/' + filename, 'rb') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				rowNumber = 0
				maxZ = -float("inf")
				minZ = float("inf")
				
				for row in spamreader:					
					if(rowNumber > 1):
						if(fileNumber == 0):
							if(float(row[3]) < minZ):
								minZ = float(row[3])
								idMinZ = int(row[0])
							if(float(row[3]) > maxZ):
								maxZ = float(row[3])	
								idMaxZ = int(row[0])
						else:
							if(int(row[0]) == idMinZ):
								minZAfter = float(row[3])
							if(int(row[0]) == idMaxZ):
								maxZAfter = float(row[3])
					rowNumber += 1
			if(fileNumber == 0):
				print minZ, maxZ, idMinZ, idMaxZ
				length_init = maxZ - minZ
				timeSeries.append(0)
				glsValues.append(0)
			else:
				length_end = maxZAfter - minZAfter
				GLS = (length_end - length_init) / length_init
				glsValues.append(GLS)
				time += 1e-5
				timeSeries.append(time)
			fileNumber += 1

plt.plot(timeSeries, glsValues)
plt.show()



			
#			l1 = centerLineFEM(pointsWithIds_FEM, deformedPointsWithIds_FEM)
#			l3 = centerLineSPH(pointsWithIds_sph, deformedPointsWithIds_sph)

#			plot_lines.append([l1,l3])
#			legend1=plt.legend(plot_lines[0],["FEM","SPH"],loc=4)
#			plt.gca().add_artist(legend1)
#			plt.ylabel('z (mm)')
#			plt.xlabel('x (mm)')
#			plt.savefig("centerlineComparison", bbox_inches='tight', dpi = 300)

#			plt.clf()
