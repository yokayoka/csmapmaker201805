# coding:cp932
#-------------------------------------------------------------------------------
# Name:        dem2csmaptif02.py
# Purpose:     ���ƂȂ�DEM����CS���̐}�̍쐬�ɕK�v�ȃ}�b�v�h�L�������g���o��
# ����ƂƂ���GeoTiff�`����CS���̐}���o�͂��܂�
# Author:      Hiromu Daimaru
# Improvement    2�o�C�g�����Ή��ŁAGeoTiff�̍쐬�@�\���폜
# Licence:     Hiromu Daimaru
# Created:     28 Ap. 2018
# Copyright:   (c) Daimaru and Toda 2016
#-------------------------------------------------------------------------------
import math
import os
import shutil

# ArcGIS��Python Module���g�p���܂�
import arcpy
from arcpy import env
from arcpy.sa import *

# Spatial Analyst extension license�@���g�p���܂�
arcpy.CheckOutExtension("Spatial")

# csmap_layers: CS���̐}���쐬����֐�
# inputdem: �ޗ�DEM,  outputdir: �o�̓t�H���_�[, weightfile: �������t�B���^�[
# sybdir: �F����ݒ肵������{���C���[�̃t�H���_�[
def csmap_layers(inputdem, outputdir, weightfile, sybdir):
    # ���[�N�X�y�[�X���o�͐�t�H���_�[�ɐݒ�
    env.workspace = outputdir
    # ���d�t�@�C���i�e�L�X�g�`���j��ǂݍ���Ńt�B���^�[���쐬
    weight = NbrWeight(weightfile)
    # �����������̎��s
    outFocalStatistics =  FocalStatistics(inputdem, weight, "MEAN", "NODATA")
    # �v�Z���ʂ�smoothdem�Ƃ������O�̃O���b�h�ŕۑ�
    outFocalStatistics.save("smoothdem.tif")

    # DEM���C���[�̃R�s�[
    arcpy.CopyRaster_management(inputdem,"dem.tif")
    # DEM���C���[�̍쐬�ƕۑ�
    arcpy.MakeRasterLayer_management("dem.tif", "demlayer","#")
    arcpy.SaveToLayerFile_management("demlayer", "dem.lyr", "RELATIVE")

    # DEM���C���[�̃V���{���̃R�s�[
    # Set layer to apply symbology to
    inputLayer = "dem.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/dem.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # �ȗ��̌v�Z
    # ���͂ɂ͕���������DEM���g�p
    inRaster = "smoothdem.tif"
    zFactor = 1.0
    # �v�Z�̎��s
    outCurve = Curvature(inRaster, zFactor)
    # �v�Z���ʂ̏o��
    outCurve.save("curvature.tif")
    # �ȗ����C���[�̍쐬
    arcpy.MakeRasterLayer_management("curvature.tif", "curvlayer","#")

    # �ȗ����C���[�P�̕ۑ�
    arcpy.SaveToLayerFile_management("curvlayer", "curvature1.lyr", "RELATIVE")
    # �ȗ����C���[�P�̃V���{���̃R�s�[
    inputLayer = "curvature1.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/curvature1.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # �ȗ����C���[�Q�̕ۑ�
    arcpy.SaveToLayerFile_management("curvlayer", "curvature2.lyr", "RELATIVE")
    # �ȗ����C���[�Q�̃V���{���̃R�s�[
    inputLayer = "curvature2.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/curvature2.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # �X�Ίp�̌v�Z
    outMeasurement = "DEGREE"
    zFactor = 1.0  # �C��2015/04/05
    # �v�Z�̎��s
    outSlope = Slope(orgDEM, outMeasurement, zFactor)
    # �v�Z���ʂ̕ۑ�
    outSlope.save("slope.tif")
    # �X�΃��C���[�̍쐬
    arcpy.MakeRasterLayer_management("slope.tif", "slopelayer","#")

    # �X�΃��C���[�P�̕ۑ�
    arcpy.SaveToLayerFile_management("slopelayer", "slope1.lyr", "RELATIVE")
    # �X�΃��C���[�P�̃V���{���̃R�s�[
    inputLayer = "slope1.lyr"
    # Set layer that output symbology will be based on
    symbologyLayer = sybdir + "/slope1.lyr"
    # Apply the symbology from the symbology layer to the input layer
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

    # �X�΃��C���[�Q�̕ۑ�
    arcpy.SaveToLayerFile_management("slopelayer", "slope2.lyr", "RELATIVE")
    # �X�΃��C���[�Q�̃V���{���̃R�s�[
    inputLayer = "slope2.lyr"
    # ���{�ƂȂ�V���{�����C�����w��
    symbologyLayer = sybdir + "/slope2.lyr"
    # ���{�̃V���{���̓K�p
    arcpy.ApplySymbologyFromLayer_management (inputLayer, symbologyLayer)

# CS���̐}���\�����郌�C���[�Q����CS���̐}�쐬�p�̃}�b�v�h�L�������g���쐬����֐�
# indocument => ���{�ƂȂ���mxd�t�@�C��
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


# ���ƂȂ�DEM�̎w��
orgDEM = arcpy.GetParameterAsText(0)
orgDEM  = orgDEM .encode('utf-8')

# �o�͐�t�H���_�[�̎w��
outdir = arcpy.GetParameterAsText(1)
outdir  = outdir .encode('utf-8')

# �J�[�l���t�@�C���̎w��
inWeightFile = arcpy.GetParameterAsText(2)

# �F����ݒ肷��T���v���t�@�C���̏ꏊ�̎w��
sybdir = arcpy.GetParameterAsText(3)
# ��̃}�b�v�h�L�������g�̎w��
#orgdoc = arcpy.GetParameterAsText(4)
orgdoc = sybdir + "\\newmap1.mxd"


# CS���̐}�̍ޗ��ƂȂ郌�C���[�Q�̍쐬�i�֐��̌Ăяo���j
csmap_layers(orgDEM, outdir, inWeightFile,sybdir)

try:
    # CS���̐}��ArcMap�h�L�������g�̍쐬
    makemxd = arcpy.GetParameterAsText(4)
    if makemxd == "true":
        # Map Document�ɓǂݍ��ރ��C���[�Q�̎w��
        # CS���̐}�̃��C���[�Q���i�[�����ArcMap�h�L�������g
        resultdoc = outdir + "\\csmap.mxd"
        slope1 =   outdir + "\\slope1.lyr"
        slope2 =   outdir + "\\slope2.lyr"
        curv1 =   outdir + "\\curvature1.lyr"
        curv2 =   outdir + "\\curvature2.lyr"
        demlyr =  outdir + "\\dem.lyr"

        #�@CS���̐}�̍ޗ��ƂȂ郌�C���[�Q���h�L�������g�ɓǂݍ���
        # make_csmap_document�@�֐��̌Ăяo��
        make_csmap_document(demlyr,slope1,slope2,curv1,curv2,orgdoc,resultdoc)
        mxd = arcpy.mapping.MapDocument(resultdoc)
        df = arcpy.mapping.ListDataFrames(mxd, "New Data Frame")[0]
        #df = arcpy.mapping.ListDataFrames(mxd)[0]

except arcpy.ExecuteError as e:
    print str(e).decode("UTF-8")
