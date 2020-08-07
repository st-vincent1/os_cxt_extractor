#!/bin/bash

lgs=($1 $2)
src=$1
tgt=$2
IFS=$'\n' lgs=($(sort <<<"${lgs[*]}"))
unset IFS

echo ${lgs[@]}
pairname="${lgs[0]}-${lgs[1]}"
echo $pairname

mkdir -p OpenSubtitles
mkdir -p OpenSubtitles/xml
mkdir -p OpenSubtitles/"$pairname"/parsed
mkdir -p OpenSubtitles/"$pairname"/cxt_dataset

wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$src.zip" -O ./OpenSubtitles/xml/"$src".zip
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$tgt.zip" -O ./OpenSubtitles/xml/"$tgt".zip
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$pairname.xml.gz" -O ./OpenSubtitles/"$pairname"/"$pairname".xml.gz

unzip OpenSubtitles/xml/"$src".zip
unzip OpenSubtitles/xml/"$tgt".zip

gunzip OpenSubtitles/"$pairname"/"$pairname".xml.gz
