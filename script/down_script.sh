#!/bin/bash



for y in $(seq 1980 2019); do
	for d in $(seq 1 31); do
		python3 prova.py -d $d -m 01 -y $y -mlon -20 -mlat 26 -mxlon -10 -mxlat 31
	done
done
