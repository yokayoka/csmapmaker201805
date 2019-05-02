# coding:cp932
#-------------------------------------------------------------------------------
# Name:        putheader001.py
# Purpose:     n,x,y,z�`����csv�t�@�C���Ƀw�b�_�[�s��t������ArcGIS�ɃC���|�[�g�\�ȃt�@�C���𐶐����܂�
# Author:      Hiromu Daimaru
#
# Created:     15 Apr. 2018
# Copyright:   (c) Daimaru and Toda 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
try:
    import os
    import glob
    # ���[�N�X�y�[�X�̎w��
    arcpy.env.workspace = arcpy.GetParameterAsText(0)
    # ���͂���f�[�^�t�@�C���̊g���q
    ext = arcpy.GetParameterAsText(1)
    # glob�Ńt�@�C�������������鐳�K�\���̐ݒ�
    param = arcpy.env.workspace + '\*.' + ext
    fileList = glob.glob(param)
    # �w�b�_�[�t���̃e�L�X�g�t�@�C�����o�͂���t�H���_�[���쐬����
    outPath = arcpy.env.workspace + '\\header_txt'
    os.mkdir(outPath)
    # �w�b�_�[�s�̒�`
    header = 'num,x,y,z\n'
    for f in fileList:
        # �t�@�C�����̊g���q�̑O�̕�����map���Ƃ���
        map = f.split('\\')[-1].split('.')[-2]
        # print map

        outFile = outPath +'\\' + map + '.txt'
        outf = open(outFile, 'w')
        outf.write(header)
        for list in open(f, 'r'):
            dat = list
            outf.write(dat)
        outf.close

except arcpy.ExecuteError as e:
    print str(e).decode("UTF-8")
