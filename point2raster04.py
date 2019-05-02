# coding:cp932
#-------------------------------------------------------------------------------
# Name:        point2raster01.py
# Purpose:     csv�`����xyz�e�L�X�g�t�@�C������DEM���X�^�[���쐬���܂�
# Author:      Hiromu Daimaru
# 	ArcToolbox �Ή���
# Created:     8/04/2018
# Copyright:   (c) Daimaru
#-------------------------------------------------------------------------------
import math
import codecs
import glob
import os
import os.path
import arcpy
#from arcpy import env
from arcpy.sa import *

try:
	def txt2dbf(Location, txtFile):
		#nameList = txtFile.split(".")
		mapName = txtFile.split(".")[-2]
		outLocation = Location
		outTable = mapName
		arcpy.TableToTable_conversion(txtFile, outLocation, outTable)

	def dbf2shp(dbfFile,x_coords, y_coords, savedLayer, outShape, spRef, z_coords):
		#  �e���|�����ȃ��C���[�t�@�C���̎w��
		out_Layer = "dem_layer"
		# ���e�@�̐ݒ�
		spRef = "D:/arcpy_work/Lidar_tool/point2raster/prj/JGD2000_xy9.prj"
		# dbf�t�@�C������|�C���g���C���[�𐶐�
		arcpy.MakeXYEventLayer_management(dbfFile, x_coords, y_coords, savedLayer, spRef, z_coords)
		# �|�C���g���C���[��ۑ�
		arcpy.SaveToLayerFile_management(out_Layer, savedLayer)

	def txt2lyr(Location, txtFile, sr):
		#nameList = txtFile.split(".")
		mapName = txtFile.split(".")[-2]
		outLocation = Location
		outTable = mapName
		outLayer = mapName
		savedLayer = outLayer +'.lyr'
		arcpy.TableToTable_conversion(txtFile, outLocation, outTable)
		arcpy.MakeXYEventLayer_management(txtFile, "x", "y", outLayer, sr, "z")

		arcpy.SaveToLayerFile_management(outLayer, savedLayer)

	def txt2raster(Location, txtFile, sr, cellSize, pointNum, radius):
		# Location: �p�X, txtFile: �t�@�C����, sr: ���e�@, cellSize: ���X�^�[�̃O���b�h�T�C�Y, pointNum: �����_��, radius: �������a
		#nameList = txtFile.split(".")
		mapName = txtFile.split(".")[-2]
		outLocation = Location
		outTable = mapName
		outLayer = mapName
		savedLayer = outLayer +'.lyr'
		arcpy.TableToTable_conversion(txtFile, outLocation, outTable)
		arcpy.MakeXYEventLayer_management(txtFile, "x", "y", outLayer, sr, "z")
		arcpy.SaveToLayerFile_management(outLayer, savedLayer)
		#inPointFeatures = "ca_ozone_pts.shp"
		zField = "z"
		#cellSize = 5
		power = 2
		arcpy.CheckOutExtension("Spatial")
		searchRadius = RadiusVariable(pointNum, radius)
		# Execute IDW
		#outIDW = Idw(inPointFeatures, zField, cellSize, power, searchRadius)
		outIDW = Idw(outLayer, zField, cellSize, power, searchRadius)
		savedRaster = Location + '/' + mapName +'.tif'
		# Save the output
		#outIDW.save("C:/sapyexamples/output/idwout02")
		outIDW.save(savedRaster)
	# ��ƃt�H���_�[�̐ݒ�
	arcpy.env.workspace = arcpy.GetParameterAsText(0)
	# ���e�@�̐ݒ�
	spRef = arcpy.GetParameterAsText(1)
	# �g���q�̐ݒ�
	ext = arcpy.GetParameterAsText(2)
#	inFile = "09KF691_grd.txt"
	# �o�̓��X�^�[�̃Z���T�C�Y
	gridSize = int(arcpy.GetParameterAsText(3))
	# ���}�Ɏg�p����_�̐�
	points = int(arcpy.GetParameterAsText(4))
	# ���}�̌������a
	radius = int(arcpy.GetParameterAsText(5))

	# �t�@�C�������̂��߂̐��K�\���̐ݒ�
	fileParam = arcpy.env.workspace + '/*.' + ext

	# ���K�\���ɍ��v�����t�@�C�����X�g�̎擾���ăt�@�C�����̂݃��X�g���擾�j
	fileList =  [r.split('\\')[-1] for r in glob.glob(fileParam)]
#	codeList = [c.split("_")[-2] for c in fl]

	for f in fileList:
		#txt2dbf(env.workspace, f)
		#txt2lyr(env.workspace, f, spRef)
		txt2raster(arcpy.env.workspace, f, spRef, gridSize, points, radius)

	#fileList.sort

	#for f in fileList:
	#	txt2dbf(env.workspace, f)

except arcpy.ExecuteError as e:
    print str(e).decode("UTF-8")
