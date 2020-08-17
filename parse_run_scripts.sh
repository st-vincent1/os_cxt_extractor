#!/bin/bash
lg=$1

for f in *.sh
do
  cp -- "$f" "$lg/$f"
  sed "s/ru/$lg/g" "$lg/*.sh"
done