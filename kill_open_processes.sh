#!/bin/sh

killables=$(ps aux | grep $1 | grep -v mykill | grep -v grep)
if [ ! "${killables}" = "" ]
then
  echo "You are going to kill some process:"
  echo "${killables}"
else
  echo "No process with the pattern $1 found."
  return
fi
echo -n "Is it ok?(Y/N)"
read input
if [ "$input" = "Y" ]
then
  for pid in $(echo "${killables}" | awk '{print $2}')
  do
    echo killing $pid "..."
    kill -9 $pid 
    echo $pid killed
  done
fi
