from __future__ import absolute_import, unicode_literals
from celery import shared_task

import gzip
import inotify.adapters
import os
import shutil
import subprocess as sp
import tarfile
import time

path_yakin = "/home/lfsm/yakin"

@shared_task
def monitor_file(resultlog_path):
    i = inotify.adapters.Inotify()
    i.add_watch(resultlog_path)
    for evt in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = evt

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPE={}".format(path, filename, type_names))

@shared_task
def process_state(self):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})

@shared_task
def get_log():
    exe_process = sp.run(['/home/coverage/coverage_web_system/coverage_websys_py3/script/get-log.sh'], shell=True)

@shared_task
def start_coverage_test():
    if os.path.isdir('/dev/disk/lfsm') is False:
        disk_link = sp.run(['/home/coverage/coverage_web_system/coverage_websys_py3/script/disk-ln.sh'], shell=True)

    exe_chk_lfsm_config = sp.run(['/home/coverage/coverage_web_system/coverage_websys_py3/script/chk-lfsm-cof.sh'], shell=True)
    exe_process = sp.run(['cd /home/lfsm/yakin/coverage/scripts && /usr/bin/bash start.run >> /tmp/console.log 2>&1'], shell=True)

@shared_task
def print_result_to_console(log_name):
    log_dir = path_yakin + '/coverage/log'
    latest_dir = max([os.path.join(log_dir, d) for d in os.listdir(log_dir)], key=os.path.getmtime)
    result_scp_log = latest_dir + '/' + log_name
    output_file = '/tmp/console.log'
    i = inotify.adapters.Inotify()
    i.add_watch(latest_dir)
    for events in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = events
        if 'IN_CLOSE_WRITE' in type_names:
            if os.path.isfile(result_scp_log):
                with open(result_scp_log) as file1, open(output_file, 'a') as file2:
                    file1_lines = file1.readlines()
                    file2.write(file1_lines[0])
                    file2.close()

@shared_task
def output_result_html(op_mode):
    log_dir = path_yakin + '/coverage/log'

    if op_mode == 'auto':
        time.sleep(15)
    else:
        if len(os.listdir(log_dir)) == 0:
            return False
        with open('/tmp/covt_result', 'w') as f:
            f.write('finish')

    while len(os.listdir(log_dir)) == 0:
        time.sleep(1)
    try:
        latest_dir = max([os.path.join(log_dir, d) for d in os.listdir(log_dir)], key=os.path.getmtime)
    except:
        print('missing log, maybe there is no any log')

    while len(os.listdir(latest_dir)) == 0:
        time.sleep(1)

    output_html = latest_dir + '/output/index.html'

    while os.path.isfile(output_html) is False:
        time.sleep(1)

    while open('/tmp/covt_result', 'r').readlines()[-1].strip() != 'finish':
        time.sleep(1)
    
    chk_result_exist = sp.run(['pgrep', '-cf', 'simple-cors-httpserver.py'], stdout=sp.PIPE)
    if int(chk_result_exist.stdout.decode('utf-8').strip()) > 0:
        pid_chk_result_exist = sp.run(['pgrep', '-f', 'simple-cors-httpserver.py'], stdout=sp.PIPE)
        kill_p = os.kill(int(pid_chk_result_exist.stdout.decode('utf-8').strip()), 9)

    exe_process = sp.run(['/home/coverage/coverage_web_system/coverage_websys_py3/script/post-test.sh', latest_dir])

@shared_task
def chk_user_upload(f_gz):
    path_upload = "/home/coverage/coverage_web_system/coverage_websys_py3/upload"
    path_tmp = "/home/tmpfolder"
    f_user_upload = path_upload + '/' + f_gz
    f_name = f_gz.split('.')[0]

    if len(os.listdir(path_upload)) == 0:
        return False

    if os.path.isfile(f_user_upload) is False:
        return False

    if tarfile.is_tarfile(f_user_upload) is False:
        return False
    else:
        try:
            t_f = tarfile.open(shutil.copy(f_user_upload, path_tmp))
            t_f.extractall(path=path_tmp)
        except:
            print('open tar file fail.')

        os.rename(path_yakin, '/home/lfsm/yakin' + time.strftime('%Y%m%d%H%M%S'))
        exe_sync_yakin = sp.run(['rsync', '-arvhq', path_tmp + '/' + t_f.getnames()[0], '/home/lfsm/'])
        exe_chk_lfsm_config = sp.run(['/home/coverage/coverage_web_system/coverage_websys_py3/script/chk-lfsm-cof.sh'], shell=True)

@shared_task
def chk_system_inuse():
    file_system_inuse = '/tmp/covt_result'
    get_exist_process = sp.run(['pgrep', '-cf', '1230'], stdout=sp.PIPE)
    n_get_exist_process = get_exist_process.stdout.decode('utf-8').strip()
    if int(n_get_exist_process) == 0:
        monitor_system_inuse = sp.run(['websocketd', '--port', '1230', 'tail', '-f', file_system_inuse])
    else:
        return