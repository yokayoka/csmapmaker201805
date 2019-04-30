# coding:cp932
#-------------------------------------------------------------------------------
# Name:        putheader001.py
# Purpose:     n,x,y,z形式のcsvファイルにヘッダー行を付加してArcGISにインポート可能なファイルを生成します
# Author:      Hiromu Daimaru
#
# Created:     15 Apr. 2018
# Copyright:   (c) Daimaru and Toda 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
try:
    import os
    import glob
    # ワークスペースの指定
    arcpy.env.workspace = arcpy.GetParameterAsText(0)
    # 入力するデータファイルの拡張子
    ext = arcpy.GetParameterAsText(1)
    # globでファイル名を検索する正規表現の設定
    param = arcpy.env.workspace + '\*.' + ext
    fileList = glob.glob(param)
    # ヘッダー付きのテキストファイルを出力するフォルダーを作成する
    outPath = arcpy.env.workspace + '\\header_txt'
    os.mkdir(outPath)
    # ヘッダー行の定義
    header = 'num,x,y,z\n'
    for f in fileList:
        # ファイル名の拡張子の前の部分をmap名とする
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
