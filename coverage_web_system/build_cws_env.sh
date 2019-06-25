#!/bin/bash

[[ ! -d /home/cws_test_history ]] && mkdir -p /home/cws_test_history
[[ ! -d /home/coverage/coverage_web_system/coverage_websys_py3/upload ]] && mkdir -p /home/coverage/coverage_web_system/coverage_websys_py3/upload
[[ ! -L /home/coverage/coverage_web_system/coverage_websys_py3/upload/cws_test_history ]] && ln -s /home/cws_test_history /home/coverage/coverage_web_system/coverage_websys_py3/upload/cws_test_history
[[ ! -d env_py3 ]] && /usr/bin/python3 -m venv env_py3

firewall-cmd --add-port=1230/tcp --permanent
firewall-cmd --add-port=1231/tcp --permanent
firewall-cmd --add-port=1234/tcp --permanent
firewall-cmd --add-port=1235/tcp --permanent
firewall-cmd --add-port=8000/tcp --permanent
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload

source env_py3/bin/activate
pip install -r requirements.txt