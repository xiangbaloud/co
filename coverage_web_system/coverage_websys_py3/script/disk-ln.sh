#!/bin/bash

[[ -d /dev/disk/lfsm ]] || mkdir -p /dev/disk/lfsm

dev_list=('sdb' 'sdc' 'sdd' 'sde' 'sdf' 'sdg' 'sdh' 'sdi')

for ((i=0; i<${#dev_list[@]}; i++))
do
	ln -s /dev/${dev_list[$i]} /dev/disk/lfsm/$i
done