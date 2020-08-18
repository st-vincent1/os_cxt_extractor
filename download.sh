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

if [ ! -f ./OpenSubtitles/xml/"$src".zip ]; then
  wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$src.zip" -O ./OpenSubtitles/xml/"$src".zip
  unzip OpenSubtitles/xml/"$src".zip
fi

if [ ! -f ./OpenSubtitles/xml/"$tgt".zip ]; then
  wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$tgt.zip" -O ./OpenSubtitles/xml/"$tgt".zip
  unzip OpenSubtitles/xml/"$tgt".zip
fi

if [ ! -f ./OpenSubtitles/"$pairname"/"$pairname".xml.gz ]; then
  wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$pairname.xml.gz" -O ./OpenSubtitles/"$pairname"/"$pairname".xml.gz
  gunzip OpenSubtitles/"$pairname"/"$pairname".xml.gz
fi
