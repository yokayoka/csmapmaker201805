# coding:cp932
#-------------------------------------------------------------------------------
# Name:        lem2raster04e.py
# Purpose:     lem�t�@�C���ƃw�b�_�[�t�@�C��(csv�j����O���b�h�`����Geotiff���쐬�����e�@��ݒ肵�܂�
#              �����t�@�C�������AASCII�o�͂��֐��������o�[�W�����ł�
# Author:      Hiromu Daimaru
#
# Created:     02 May 2015
# Copyright:   (c) Daimaru and Toda 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import codecs
import glob
import os
import os.path

# ArcGIS��Python Module���g�p���܂�
import arcpy

# ----- �ȉ��֐����� ------
def Lem2Ascii(headerfile, lemfile, asciifile):
    # �w�b�_�[�t�@�C���̃I�[�v��
    #hf = open(HeaderList[m],'r')
    hf = codecs.open(headerfile,'r','shift_jis')
    # �o��ASCII�t�@�C���̃I�[�v��
    outf = open(asciifile,'w')

    # �w�b�_�[�t�@�C���̏��擾
    # ���{�̑��ʍ��W�n��XY���t�̓_�ɒ��ӁI
    for line in hf:
        # 1�s���J���}�ŕ�������
        d = line.split(',')

        if d[0]==u'���������̓_��':
            ncols=d[1].rstrip("\n") # rstrip -> �s���̉��s�͏�������
            col = int(ncols)
            last_data=col*5+10             #  <--------�i�˓c�C���j
        if d[0]==u'��k�����̓_��':
            nrows=d[1].rstrip('\n')
            row=int(d[1])

        if d[0]==u'��捶��Y���W':
            xllcorner= int(d[1])/100

        if d[0]==u'��捶��X���W':
            yllcorner= int(d[1])/100

        if d[0]==u'���������̃f�[�^�Ԋu':
            cellsize= d[1].rstrip('\n')
           # cellsize='0.5' #  <--------CSV���Ԉ���Ă���ꍇ�͋����w��i�˓c�j

    outf.write('NCOLS '+ str(col) + '\n')
    outf.write('NROWS '+ str(row) + '\n')
    outf.write('XLLCORNER '+ str(xllcorner) + '\n')
    outf.write('YLLCORNER '+ str(yllcorner) + '\n')
    outf.write('CELLSIZE '+ cellsize + '\n')#  <--------+'\n'�������Ă����i�˓c�j
    outf.write('NODATA_VALUE '+ nodata + '\n')

    hf.close    # �w�b�_�[�t�@�C�����N���[�Y����

    # lem�t�@�C�����I�[�v�����܂�
    f = open(lemfile)

    for line in f:
        # �f�[�^�{�̂�11�`last_data����荞��  <--------�����̓_���ɂ��ǂݍ��ݐ����ρi�˓c�C���j
        data = line[10:last_data]           #  <--------�i�˓c�C���j
        # 5�o�C�g���Ƀf�[�^��elv�Ƃ��Ď�荞��
        for i in range(col):
            head = i*5
            tail = head+5
            elv = int(data[head:tail])
            # �n���@�����̕W����0.1m�P�ʁB�}�C�i�X�l�͂��̂܂܁B
            if elv > 0:
                elv = elv * 0.1
            # �W���Ƌ�؂�X�y�[�X���o��
            outf.write(str(elv)+' ')
            # ���[�̃f�[�^���o�͂�������s
        outf.write('\n')
    # lem�t�@�C���̃N���[�Y
    f.close
    # �o��ASCII�t�@�C���̃N���[�Y
    outf.close()

# ----- �����܂Ŋ֐����� ------

try:
    # �e�}�s�ɂ��ăw�b�_�[���Ƃ��l���o�͂��܂�
    # �ȉ��͍��y�n���@�����̃w�b�_�[�t�@�C����z��
    # http://www1.gsi.go.jp/geowww/Laser_HP/f5m1.html
    # Esri ASCII ���X�^�`���ɂ��Ă͉��L���Q��
    # http://help.arcgis.com/ja/arcgisdesktop/10.0/help/index.html#/na/009t0000000z000000/

    # ���[�N�X�y�[�X�̎w��
    arcpy.env.workspace = arcpy.GetParameterAsText(0)
    #arcpy.env.workspace = r"D:\test6" #�e�X�g�p

    # ���e�@�t�@�C���̎w��
    sr = arcpy.GetParameterAsText(1)


    # lem�t�@�C���̃��X�g���擾���邽�߂�glob�R�}���h�̃p�����[�^�[��ݒ�
    Lem_Param= arcpy.env.workspace + '\*.lem'
    LemList = glob.glob(Lem_Param)
    LemList.sort

    # �n�}�f�[�^�̑���
    mapcount = len(LemList)

    # �w�b�_�[�t�@�C���̃��X�g���擾���邽�߂�glob�R�}���h�̃p�����[�^�[��ݒ�
    Head_Param= arcpy.env.workspace + '\*.csv'
    HeaderList = glob.glob(Head_Param)
    HeaderList.sort

    # ASCII�^���X�^�[�t�@�C�����i�[���邽�߂̃t�H���_�[����ݒ肵�č쐬����
    AsciiPath = arcpy.env.workspace + '\\ascii'
    os.mkdir(AsciiPath)

    # ���X�^�[�f�[�^���o�͂��邽�߂̃t�H���_�[����ݒ肵�č쐬����
    RasterPath = arcpy.env.workspace + '\\raster'
    os.mkdir(RasterPath)


    nodata ='-1111' #�i���l�̎w��

    # �n�}�f�[�^�̖��̂̔z����쐬����
    rasterList = []
    for m in range(mapcount):
        # MapCode�݂̂𒊏o����
        mapname =os.path.basename(LemList[m]).split('.')
        mapcode = mapname[0]
        # ASCII ���X�^�[�t�@�C�����𐶐�����
        outasciifile = AsciiPath + '\\' + mapcode + ".asc"

        ###lem2ascii
        Lem2Ascii(HeaderList[m],LemList[m],outasciifile)

        # ��ŏo�͂���ASCII�t�@�C������̓t�@�C���Ƃ��Ďw��
        inasciifile = outasciifile
        print inasciifile

        # �o�͗p���X�^�[�t�@�C�����𐶐�

        outrasterfile = RasterPath + '\\' + mapcode + '.tif'
        rasterList.append(outrasterfile)

        # ASCII �`���̃f�[�^�����X�^�[�ɃC���|�[�g
        arcpy.ASCIIToRaster_conversion(inasciifile, outrasterfile,"FLOAT")
        # �I���������e�@��ݒ肷��
        arcpy.DefineProjection_management(outrasterfile, sr)


except arcpy.ExecuteError as e:
    print str(e).decode("UTF-8")
