# coding:cp932
#-------------------------------------------------------------------------------
# Name:        dem2csmaptif02.py
# Purpose:     元となるDEMからCS立体図の作成に必要なマップドキュメントを出力
# するとともにGeoTiff形式のCS立体図を出力します
# Author:      Hiromu Daimaru
# Improvement    2バイト文字対応版、GeoTiffの作成機能を削除
# Licence:     Hiromu Daimaru
# Created:     28 Ap. 2018
# Copyright:   (c) Daimaru and Toda 2016
#-------------------------------------------------------------------------------
import math
import os
import shutil

# ArcGISのPython Moduleを使用します
import arcpy
from arcpy import env
from arcpy.sa import *

# Spatial Analyst extension license　を使用します
arcpy.CheckOutExtension("Spatial")

# csmap_layers: CS立体図を作成する関数
# inputdem: 材料DEM,  outputdir: 出力フォルダー, weightfile: 平滑化フィルター
# sybdir: 色調を設定したお手本レイヤーのフォルダー
def csmap_layers(inputdem, outputdir, weightfile, sybdir):
    # ワークスペースを出力先フォルダーに設定
    env.workspace = outputdir
    # 加重ファイル（テキスト形式）を読み込んでフィルターを作成
    weight = NbrWeight(weightfile)
    # 平滑化処理の実行
    outFocalStatistics =  FocalStatistics(inputdem, weight, "MEAN", "NODATA")
    # 計算結果をsmoothdemという名前のグリッドで保存
    outFocalStatistics.save("smoothdem.tif")

    # DEMレイヤーのコピー
    arcpy.CopyRaster_management(inputdem,"dem.tif")
    # DEMレイヤーの作成と保存
    arcpy.MakeRasterLayer_management("dem.tif", "demlayer","#")
    arcpy.SaveToLayerFile_management("demlayer", "dem.lyr", "RELATIVE")

    # DEMレイヤーのシンボルのコピー
    # Set layer to apply symbology to
    inputLayer = "dem.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/dem.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # 曲率の計算
    # 入力には平滑化したDEMを使用
    inRaster = "smoothdem.tif"
    zFactor = 1.0
    # 計算の実行
    outCurve = Curvature(inRaster, zFactor)
    # 計算結果の出力
    outCurve.save("curvature.tif")
    # 曲率レイヤーの作成
    arcpy.MakeRasterLayer_management("curvature.tif", "curvlayer","#")

    # 曲率レイヤー１の保存
    arcpy.SaveToLayerFile_management("curvlayer", "curvature1.lyr", "RELATIVE")
    # 曲率レイヤー１のシンボルのコピー
    inputLayer = "curvature1.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/curvature1.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # 曲率レイヤー２の保存
    arcpy.SaveToLayerFile_management("curvlayer", "curvature2.lyr", "RELATIVE")
    # 曲率レイヤー２のシンボルのコピー
    inputLayer = "curvature2.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/curvature2.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # 傾斜角の計算
    outMeasurement = "DEGREE"
    zFactor = 1.0  # 修正2015/04/05
    # 計算の実行
    outSlope = Slope(orgDEM, outMeasurement, zFactor)
    # 計算結果の保存
    outSlope.save("slope.tif")
    # 傾斜レイヤーの作成
    arcpy.MakeRasterLayer_management("slope.tif", "slopelayer","#")

    # 傾斜レイヤー１の保存
    arcpy.SaveToLayerFile_management("slopelayer", "slope1.lyr", "RELATIVE")
    # 傾斜レイヤー１のシンボルのコピー
    inputLayer = "slope1.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/slope1.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # 傾斜レイヤー２の保存
    arcpy.SaveToLayerFile_management("slopelayer", "slope2.lyr", "RELATIVE")
    # 傾斜レイヤー２のシンボルのコピー
    inputLayer = "slope2.lyr"
    # 見本となるシンボルレイヤを指定
    symbologyLayer = sybdir + "/slope2.lyr"
    # 見本のシンボルの適用
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

# CS立体図を構成するレイヤー群からCS立体図作成用のマップドキュメントを作成する関数
# indocument => 見本となる空のmxdファイル
def make_csmap_document(demlayer, slopelayer1, slopelayer2, curvlayer1, curvlayer2, indocument, outdocument):
    mxd = arcpy.mapping.MapDocument(indocument)
    df = arcpy.mapping.ListDataFrames(mxd, "New Data Frame")[0]
    addLayer = arcpy.mapping.Layer(slopelayer1)
    arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
    addLayer = arcpy.mapping.Layer(curvlayer1)
    arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
    addLayer = arcpy.mapping.Layer(slopelayer2)
    arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
    addLayer = arcpy.mapping.Layer(curvlayer2)
    arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
    addLayer = arcpy.mapping.Layer(demlayer)
    arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
    mxd.saveACopy(outdocument)
    # del mxd, addLayer


# 元となるDEMの指定
orgDEM = arcpy.GetParameterAsText(0)
orgDEM  = orgDEM .encode('utf-8')

# 出力先フォルダーの指定
outdir = arcpy.GetParameterAsText(1)
outdir  = outdir .encode('utf-8')

# カーネルファイルの指定
inWeightFile = arcpy.GetParameterAsText(2)

# 色調を設定するサンプルファイルの場所の指定
sybdir = arcpy.GetParameterAsText(3)
# 空のマップドキュメントの指定
#orgdoc = arcpy.GetParameterAsText(4)
orgdoc = sybdir + "\\newmap1.mxd"


# CS立体図の材料となるレイヤー群の作成（関数の呼び出し）
csmap_layers(orgDEM, outdir, inWeightFile,sybdir)

try:
    # CS立体図のArcMapドキュメントの作成
    makemxd = arcpy.GetParameterAsText(4)
    if makemxd == "true":
        # Map Documentに読み込むレイヤー群の指定
        # CS立体図のレイヤー群が格納されるArcMapドキュメント
        resultdoc = outdir + "\\csmap.mxd"
        slope1 =   outdir + "\\slope1.lyr"
        slope2 =   outdir + "\\slope2.lyr"
        curv1 =   outdir + "\\curvature1.lyr"
        curv2 =   outdir + "\\curvature2.lyr"
        demlyr =  outdir + "\\dem.lyr"

        #　CS立体図の材料となるレイヤー群をドキュメントに読み込む
        # make_csmap_document　関数の呼び出し
        make_csmap_document(demlyr,slope1,slope2,curv1,curv2,orgdoc,resultdoc)
        mxd = arcpy.mapping.MapDocument(resultdoc)
        df = arcpy.mapping.ListDataFrames(mxd, "New Data Frame")[0]
        #df = arcpy.mapping.ListDataFrames(mxd)[0]

except arcpy.ExecuteError as e:
    print str(e).decode("UTF-8")
