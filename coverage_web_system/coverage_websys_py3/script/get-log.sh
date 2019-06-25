#!/bin/bash

# Port in use
# system state  1230
# case result   1231
# console.log   1234
# syslog        1235

[[ ! -f /usr/bin/nc ]] && yum install -y nc

clean_existwebsocket() {
	if (( $(ps aux | grep websocketd -c) > 1 )); then
		killall websocketd
	fi
}

clean_exist_log() {
	echo > /tmp/console.log
}

get_console_log() {
	websocketd --port 1234 tail -f /tmp/console.log
	# (echo -e 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nContent-type: text/event-stream\n' && tail -f /tmp/console.log -n1 | sed -u -e 's/^/data: /g; s/$/\n/g') | nc -l 1234
}

redirct_message() {
	return
	tail -f /var/log/messages -n1 | egrep --line-buffered -v 'Disk Serial scsi' | tee  /tmp/syslog.log
}

get_syslog() {
	(echo -e 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nContent-type: text/event-stream\n' && tail -f /var/log/messages -n1 | sed -u -e 's/^/data: /g; s/$/\n/g') | nc -l 1235
	# websocketd --port 1235 tail -f /var/log/messages -n1
}

get_console_case_result() {
	echo " " > /tmp/console_case_result.log
	websocketd --port 1231 tail -f /tmp/console_case_result.log
}

# clean_existwebsocket
get_console_log &
get_syslog &
get_console_case_result &