#!/bin/bash

waitting_for_result() {
	test_result="/tmp/covt_result"
	while [[ $(cat $test_result) != 0 ]];
	do
		sleep 1
	done
}

chk_process_exist() {
	exist_pid=$(ps ax | grep 'simple-cors-httpserver' | head -n1 | awk '{print $1}')
	kill -9 $exist_pid
}

result_output_to_http() {
	local path_log=$1
	[[ ! -d /home/cws_test_history ]] && mkdir -p /home/cws_test_history
	[[ ! -L /home/coverage/coverage_web_system/coverage_websys_py3/upload/cws_test_history ]] && ln -s /home/cws_test_history /home/coverage/coverage_web_system/coverage_websys_py3/upload/cws_test_history
	local bk_history='/home/cws_test_history'
	echo $path_log > /tmp/result_output_to_http
	local path_yakin="/home/lfsm/yakin"
	local path_http_tool="/home/coverage/coverage_web_system/coverage_websys_py3/script/simple-cors-httpserver.py"
	[[ -n $(alias | grep cp ) ]] && unalias cp
	if [[ -d $path_log/output ]]; then
		cp -rf $path_http_tool $path_log/output/
		cp -rf $path_log $bk_history
		cd $path_log/output
    	/usr/bin/python simple-cors-httpserver.py
	else
		echo "$path_log/output, No such directory"
	fi    	
}

if [[ -n $1 ]]; then
	echo 0 > /tmp/result_output_to_http
else
	echo 1 > /tmp/result_output_to_http
	exit
fi

result_output_to_http $1 &