#!/bin/bash

path_lfsm='/home/lfsm/yakin'

size_seu=$(grep 'DSSD_SIZE_IN_SEU' $path_lfsm/Makefile | cut -d'=' -f3)
chk_coverage=$(grep 'coverage' $path_lfsm/Makefile | grep '#')

if [[ $size_seu == 0 ]]; then
	cd $path_lfsm
	awk '{ if ($1~"CFLAGS_SSD_SIZE_IN_SEU") $3="-DSSD_SIZE_IN_SEU=200" } {print}' $path_lfsm/Makefile > tmpf
	mv tmpf Makefile
fi

if [[ -n $chk_coverage ]]; then
	cd $path_lfsm
	awk '{ if ($4 ~ "-ftest-coverage") $1="EXTRA_CFLAGS" } {print}' $path_lfsm/Makefile > tmpf
	mv tmpf Makefile
fi