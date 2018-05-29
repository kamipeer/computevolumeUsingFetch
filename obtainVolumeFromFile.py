#### import the simple module from the paraview
import matplotlib.pyplot as plt
from paraview.simple import *
from pprint import pprint
import os
import re
import sys

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if __name__ == "__main__":
	if(len(sys.argv) != 3):
		print "Argument List should be: ", str(sys.argv[0]), " filename"
	filePath = str(sys.argv[1])
	particles_200csv = CSVReader(FileName=[filePath])
	particles_200csv.DetectNumericColumns = 1
	particles_200csv.UseStringDelimiter = 1
	particles_200csv.HaveHeaders = 1
	particles_200csv.FieldDelimiterCharacters = ','
	particles_200csv.MergeConsecutiveDelimiters = 0

	# create a new 'Table To Points'
	tableToPoints1 = TableToPoints(Input=particles_200csv)
	tableToPoints1.XColumn = 'APD'
	tableToPoints1.YColumn = 'APD'
	tableToPoints1.ZColumn = 'APD'
	tableToPoints1.a2DPoints = 0
	tableToPoints1.KeepAllDataArrays = 0

	# Properties modified on tableToPoints1
	tableToPoints1.XColumn = 'x'
	tableToPoints1.YColumn = 'y'
	tableToPoints1.ZColumn = 'z'

	# create a new 'Glyph'
	glyph1 = Glyph(Input=tableToPoints1,
	GlyphType='Arrow')
	glyph1.Scalars = ['POINTS', 'APD']
	glyph1.Vectors = ['POINTS', 'None']
	glyph1.Orient = 1
	glyph1.ScaleMode = 'off'
	glyph1.ScaleFactor = 0.0009695249999999999
	glyph1.GlyphMode = 'Uniform Spatial Distribution'
	glyph1.MaximumNumberOfSamplePoints = 5000
	glyph1.Seed = 10339
	glyph1.Stride = 1
	glyph1.GlyphTransform = 'Transform2'

	# init the 'Arrow' selected for 'GlyphType'
	glyph1.GlyphType.TipResolution = 6
	glyph1.GlyphType.TipRadius = 0.1
	glyph1.GlyphType.TipLength = 0.35
	glyph1.GlyphType.ShaftResolution = 6
	glyph1.GlyphType.ShaftRadius = 0.03
	glyph1.GlyphType.Invert = 0

	# init the 'Transform2' selected for 'GlyphTransform'
	glyph1.GlyphTransform.Translate = [0.0, 0.0, 0.0]
	glyph1.GlyphTransform.Rotate = [0.0, 0.0, 0.0]
	glyph1.GlyphTransform.Scale = [1.0, 1.0, 1.0]

	# Properties modified on glyph1.GlyphType
	#glyph1.GlyphType.Radius = 0.1

	# Properties modified on glyph1
	glyph1.GlyphType = 'Sphere'
	glyph1.GlyphMode = 'All Points'

	# Properties modified on glyph1.GlyphType
	glyph1.GlyphType.Radius = 0.1

	# create a new 'Threshold'
	threshold1 = Threshold(Input=glyph1)
	threshold1.Scalars = ['POINTS', 'GlyphScale']
	threshold1.ThresholdRange = [0.2804499864578247, 0.29482001066207886]
	threshold1.AllScalars = 1
	threshold1.UseContinuousCellRange = 0

	# Properties modified on threshold1
	threshold1.Scalars = ['POINTS', 'particleCategory']
	threshold1.ThresholdRange = [98.0, 98.0]

	# create a new 'Delaunay 3D'
	delaunay3D1 = Delaunay3D(Input=threshold1)
	delaunay3D1.Alpha = 0.0
	delaunay3D1.Tolerance = 0.001
	delaunay3D1.Offset = 2.5
	delaunay3D1.BoundingTriangulation = 0
	delaunay3D1.AlphaTets = 1
	delaunay3D1.AlphaTris = 1
	delaunay3D1.AlphaLines = 0
	delaunay3D1.AlphaVerts = 0

	# update the view to ensure updated data information
	#spreadSheetView1.Update()

	# create a new 'Integrate Variables'
	integrateVariables1 = IntegrateVariables(Input=delaunay3D1)
	DataFile = paraview.servermanager.Fetch(integrateVariables1, 1)
	volume = DataFile.GetCellData().GetArray('Volume').GetValue(0)
	f = open('output.txt', 'a')#a from append
	f.write(str(volume) + "\n")
