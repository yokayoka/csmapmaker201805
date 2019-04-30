CSMapMaker1805
====

このスクリプトはArcGISを用いてCS立体図の作成に必要なレイヤー群を出力するものです。
## Description
CS立体図は航空レーザー測量で得られた高解像度の地形情報を可視化するうえで非常に便利な表示技術です。
このスクリプトはArcGIS上でDEMからCS立体図の表示に必要なレイヤー群を自動的に作成します。
CS立体図については下記の文献を参照してください。


## Demo
![CSMapMaker](resources/csmap_demo.gif)
## VS.
このスクリプトはArcGISを必要としますが、フリーのQGISを用いてCS立体図を作成するツールがG空間情報センターから公開されています。
https://www.geospatial.jp/ckan/dataset/cs-tool

## Requirement
ArcPyで記述されているので、ArcGIS および SpatialAnalyst が必要になります。
ArcGIS 10.1より前のバージョンでは動作確認が出来ていません。

## Usage
DEMファイル（GeoTiffなど）を選択した後、出力先のフォルダー（空である必要があります）を指定してください。シンボルのフォルダーはとりあえず、同梱の"symbol"というフォルダーを指定するとよいでしょう（ご自分で好みの色調にカスタマイズできます）。
内挿補完用のカーネルファイルは各種準備していますが、最初は kernel フォルダーの中の、gaus2503.txt あたりを指定して見てください。また、行政機関からLEM形式の標高データの提供を受けた場合などに、geotifに変換するためのlem2rasterというスクリプトも同梱してありますのでご利用ください。
詳細は、documentフォルダーの中のpdfファイルをご覧ください。

## Install
zipファイルを展開して出来たフォルダーをArcCatalogで開いてDEMからCS立体図を作成するツールを立ち上げてください。

## Licence

[CCBY-NC-SA4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Author
[yokayoka](https://github.com/yokayoka)
