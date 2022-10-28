#!/bin/bash

while read i; 
do
  sed -i "/^${i}\s.*/d" $2
done <$1

#bash script.sh your_config_file patterns_file