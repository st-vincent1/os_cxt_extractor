#!/bin/bash

src=$1
tgt=$2

wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$src.zip" -O "OpenSubtitles/xml/$src.zip"
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$tgt.zip" -O "OpenSubtitles/xml/$tgt.zip"
wget "http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/$src-$tgt.xml.gz" -O "OpenSubtitles/$src-$tgt.xml.gz"

unzip OpenSubtitles/xml/"$src".zip
unzip OpenSubtitles/xml/"$tgt".zip

gzip OpenSubtitles/"$src"-"$tgt".xml.gz
