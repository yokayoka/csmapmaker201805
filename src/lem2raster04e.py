# coding:cp932
#-------------------------------------------------------------------------------
# Name:        lem2raster04e.py
# Purpose:     lemファイルとヘッダーファイル(csv）からグリッド形式のGeotiffを作成し投影法を設定します
#              複数ファイル処理、ASCII出力を関数化したバージョンです
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

# ArcGISのPython Moduleを使用します
import arcpy

# ----- 以下関数部分 ------
def Lem2Ascii(headerfile, lemfile, asciifile):
    # ヘッダーファイルのオープン
    #hf = open(HeaderList[m],'r')
    hf = codecs.open(headerfile,'r','shift_jis')
    # 出力ASCIIファイルのオープン
    outf = open(asciifile,'w')

    # ヘッダーファイルの情報取得
    # 日本の測量座標系はXYが逆の点に注意！
    for line in hf:
        # 1行をカンマで分割する
        d = line.split(',')

        if d[0]==u'東西方向の点数':
            ncols=d[1].rstrip("\n") # rstrip -> 行末の改行は除去する
            col = int(ncols)
            last_data=col*5+10             #  <--------（戸田修正）
        if d[0]==u'南北方向の点数':
            nrows=d[1].rstrip('\n')
            row=int(d[1])

        if d[0]==u'区画左下Y座標':
            xllcorner= int(d[1])/100

        if d[0]==u'区画左下X座標':
            yllcorner= int(d[1])/100

        if d[0]==u'東西方向のデータ間隔':
            cellsize= d[1].rstrip('\n')
           # cellsize='0.5' #  <--------CSVが間違っている場合は強制指定（戸田）

    outf.write('NCOLS '+ str(col) + '\n')
    outf.write('NROWS '+ str(row) + '\n')
    outf.write('XLLCORNER '+ str(xllcorner) + '\n')
    outf.write('YLLCORNER '+ str(yllcorner) + '\n')
    outf.write('CELLSIZE '+ cellsize + '\n')#  <--------+'\n'が抜けていた（戸田）
    outf.write('NODATA_VALUE '+ nodata + '\n')

    hf.close    # ヘッダーファイルをクローズする

    # lemファイルをオープンします
    f = open(lemfile)

    for line in f:
        # データ本体の11～last_dataを取り込む  <--------東西の点数により読み込み数を可変（戸田修正）
        data = line[10:last_data]           #  <--------（戸田修正）
        # 5バイト毎にデータをelvとして取り込む
        for i in range(col):
            head = i*5
            tail = head+5
            elv = int(data[head:tail])
            # 地理院方式の標高は0.1m単位。マイナス値はそのまま。
            if elv > 0:
                elv = elv * 0.1
            # 標高と区切りスペースを出力
            outf.write(str(elv)+' ')
            # 東端のデータを出力したら改行
        outf.write('\n')
    # lemファイルのクローズ
    f.close
    # 出力ASCIIファイルのクローズ
    outf.close()

# ----- ここまで関数部分 ------

try:
    # 各図郭についてヘッダー情報とｚ値を出力します
    # 以下は国土地理院方式のヘッダーファイルを想定
    # http://www1.gsi.go.jp/geowww/Laser_HP/f5m1.html
    # Esri ASCII ラスタ形式については下記を参照
    # http://help.arcgis.com/ja/arcgisdesktop/10.0/help/index.html#/na/009t0000000z000000/

    # ワークスペースの指定
    arcpy.env.workspace = arcpy.GetParameterAsText(0)
    #arcpy.env.workspace = r"D:\test6" #テスト用

    # 投影法ファイルの指定
    sr = arcpy.GetParameterAsText(1)


    # lemファイルのリストを取得するためのglobコマンドのパラメーターを設定
    Lem_Param= arcpy.env.workspace + '\*.lem'
    LemList = glob.glob(Lem_Param)
    LemList.sort

    # 地図データの総数
    mapcount = len(LemList)

    # ヘッダーファイルのリストを取得するためのglobコマンドのパラメーターを設定
    Head_Param= arcpy.env.workspace + '\*.csv'
    HeaderList = glob.glob(Head_Param)
    HeaderList.sort

    # ASCII型ラスターファイルを格納するためのフォルダー名を設定して作成する
    AsciiPath = arcpy.env.workspace + '\\ascii'
    os.mkdir(AsciiPath)

    # ラスターデータを出力するためのフォルダー名を設定して作成する
    RasterPath = arcpy.env.workspace + '\\raster'
    os.mkdir(RasterPath)


    nodata ='-1111' #ナル値の指定

    # 地図データの名称の配列を作成する
    rasterList = []
    for m in range(mapcount):
        # MapCodeのみを抽出する
        mapname =os.path.basename(LemList[m]).split('.')
        mapcode = mapname[0]
        # ASCII ラスターファイル名を生成する
        outasciifile = AsciiPath + '\\' + mapcode + ".asc"

        ###lem2ascii
        Lem2Ascii(HeaderList[m],LemList[m],outasciifile)

        # 上で出力したASCIIファイルを入力ファイルとして指定
        inasciifile = outasciifile
        print inasciifile

        # 出力用ラスターファイル名を生成

        outrasterfile = RasterPath + '\\' + mapcode + '.tif'
        rasterList.append(outrasterfile)

        # ASCII 形式のデータをラスターにインポート
        arcpy.ASCIIToRaster_conversion(inasciifile, outrasterfile,"FLOAT")
        # 選択した投影法を設定する
        arcpy.DefineProjection_management(outrasterfile, sr)


except arcpy.ExecuteError as e:
    print str(e).decode("UTF-8")
