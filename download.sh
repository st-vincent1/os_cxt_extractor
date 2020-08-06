#!/bin/bash

lgs=($1 $2)
src=$1
tgt=$2
IFS=$'\n' lgs=($(sort <<<"${lgs[*]}"))
unset IFS

echo ${lgs[@]}

mkdir -p OpenSubtitles
mkdir -p OpenSubtitles/xml
mkdir -p OpenSubtitles/parsed
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$src.zip" -O ./OpenSubtitles/xml/"$src".zip
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$tgt.zip" -O ./OpenSubtitles/xml/"$tgt".zip
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/${lgs[0]}-${lgs[1]}.xml.gz" -O ./OpenSubtitles/"${lgs[0]}"-"${lgs[1]}".xml.gz

unzip OpenSubtitles/xml/"$src".zip
unzip OpenSubtitles/xml/"$tgt".zip

gunzip OpenSubtitles/"${lgs[0]}"-"${lgs[1]}".xml.gz
