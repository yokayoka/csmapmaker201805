# coding:cp932
#-------------------------------------------------------------------------------
# Name:        point2raster01.py
# Purpose:     csv形式のxyzテキストファイルからDEMラスターを作成します
# Author:      Hiromu Daimaru
# 	ArcToolbox 対応版
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
		#  テンポラリなレイヤーファイルの指定
		out_Layer = "dem_layer"
		# 投影法の設定
		spRef = "D:/arcpy_work/Lidar_tool/point2raster/prj/JGD2000_xy9.prj"
		# dbfファイルからポイントレイヤーを生成
		arcpy.MakeXYEventLayer_management(dbfFile, x_coords, y_coords, savedLayer, spRef, z_coords)
		# ポイントレイヤーを保存
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
		# Location: パス, txtFile: ファイル名, sr: 投影法, cellSize: ラスターのグリッドサイズ, pointNum: 検索点数, radius: 検索半径
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
	# 作業フォルダーの設定
	arcpy.env.workspace = arcpy.GetParameterAsText(0)
	# 投影法の設定
	spRef = arcpy.GetParameterAsText(1)
	# 拡張子の設定
	ext = arcpy.GetParameterAsText(2)
#	inFile = "09KF691_grd.txt"
	# 出力ラスターのセルサイズ
	gridSize = int(arcpy.GetParameterAsText(3))
	# 内挿に使用する点の数
	points = int(arcpy.GetParameterAsText(4))
	# 内挿の検索半径
	radius = int(arcpy.GetParameterAsText(5))

	# ファイル検索のための正規表現の設定
	fileParam = arcpy.env.workspace + '/*.' + ext

	# 正規表現に合致したファイルリストの取得してファイル名のみリストを取得）
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
