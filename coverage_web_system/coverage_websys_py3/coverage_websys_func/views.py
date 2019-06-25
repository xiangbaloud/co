from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from coverage_websys_func.models import Document
from coverage_websys_func.forms import DocumentForm

from . import tasks

import git
import json
import os
import signal
import subprocess as sp
import time

path_yakin = '/home/lfsm/yakin'
path_coverage = '/home/coverage'

def homepage(request):
    if request.method == 'POST':
        if open('/tmp/covt_result', 'r').readlines()[-1].strip() != 'finish':
            branch_list = list_yakin_branch('all')
            current_branch = list_yakin_branch('active')
            documents = Document.objects.all()
            return render(request, 'cws_index.html', {
                'all_branch': branch_list,
                'current_branch': current_branch,
                'documents': documents,
                'systemisbusy': 'busy la',
            })
        else:
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()
                return HttpResponseRedirect(reverse('hp'))
    else:
        form = DocumentForm()

    inuse = chk_env('homepage')
    documents = Document.objects.all()
    branch_list = list_yakin_branch('all')
    current_branch = list_yakin_branch('active')
    case_list = list_test_case()
    return render(request, 'cws_index.html', {
        'documents': documents,
        'form': form,
        'all_branch': branch_list,
        'all_cases': case_list,
        'current_branch': current_branch,
        'in_use': inuse
    })

@csrf_exempt
def hp_run_testing(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))

        inuse = chk_env('hp_start')
        if inuse is 'busy':
            return HttpResponse('systemisbusy')

        consolelog_file = "/tmp/console.log"
        with open(consolelog_file, 'w') as f:
            f.write('[info] starting coverage test\n')

        tasks.get_log()
        tasks.start_coverage_test.delay()
        # tasks.print_result_to_console.delay('RESULT_lfsm_key_test.log')
        # tasks.print_result_to_console.delay('RESULT_SCRIPT.log')
        tasks.output_result_html.delay('auto')
        return HttpResponse('ok')
    else:
        return HttpResponse('do nothing')

@csrf_exempt
def hp_checkout_git(request):
    if request.method == 'POST':
        inuse = chk_env('homepage')
        if inuse is 'busy':
            return HttpResponse('systemisbusy')
        
        dict_yakin_coverage = "/home/lfsm/yakin/coverage"
        git_repo = "http://git200:0p5ZxFEBHz4eApOTa6CRnOpK0NIxLzoQ@10.144.1.200:10080/weafon/yakin.git"
        commit_id = json.loads(request.body)
        reset_yakin_env = sp.run(['cd /home/lfsm/yakin && git checkout -- .'], shell=True)
        try:
            res = git.Git(path_yakin).checkout(str(commit_id['commit_id']), force=True)
        except:
            return HttpResponse('didnotmatchanybranch')
        try:
            res_pull_latest_yakin = git.Git(path_yakin).pull()
        except:
            print('fail to git pull latest code.')
        os.rename(dict_yakin_coverage, '/home/lfsm/yakin/coverage' + time.strftime('%Y%m%d%H%M%S'))
        exe_env_rsync = sp.run(['rsync -arvhq --exclude=coverage_web_system --exclude=.git --exclude=yakin /home/coverage /home/lfsm/yakin/'], shell=True)
        exe_chk_lfsm_config = sp.run(['/home/coverage/coverage_web_system/coverage_websys_py3/script/chk-lfsm-cof.sh'], shell=True)
        return HttpResponse(res, content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('do nothing')

@csrf_exempt
def hp_chk_test_case(request):
    f_user_case = "/tmp/user_case.lst"
    if request.method == 'POST':
        req_content = json.loads(request.body.decode('utf-8'))

        inuse = chk_env('homepage')
        if inuse is 'busy':
            return HttpResponse('systemisbusy')

        user_case = req_content['case']
        bypass_user_case = ['.awk', '.fio']

        if os.path.isfile(f_user_case):
            os.remove(f_user_case)

        for u_case in user_case:
            if any(x in u_case for x in bypass_user_case):
                pass
            else:
                with open(f_user_case, 'a') as f:
                    f.write(u_case + '\n')

        return HttpResponse('ok')
    else:
        return HttpResponse('do nothing')

@csrf_exempt
def hp_user_upload(request):
    if request.method == 'POST':
        inuse = chk_env('hp_user_upload')
        if inuse is 'busy':
            return HttpResponse('systemisbusy')

        req_content = json.loads(request.body.decode('utf-8'))
        user_upload = req_content['op_content']
        tasks.chk_user_upload.delay(user_upload)
        return HttpResponse('ok')
    else:
        return HttpResponse('do nothing')

@csrf_exempt
def hp_gen_result_html(request):
    if request.method == 'POST':
        process_httpserver = sp.run(['pgrep', '-cf', 'simple-cors-httpserver.py'], stdout=sp.PIPE)
        if int(process_httpserver.stdout.decode('utf-8').strip()) != 0:        
            process_httpserver = sp.run(['pgrep', '-f', 'simple-cors-httpserver.py'], stdout=sp.PIPE)
            pid_httpserver = int(process_httpserver.stdout.decode("utf-8").split()[0])
            pk_httpserver = pid_killer(pid_httpserver)
        
        tasks.output_result_html.delay('byhand')
        return HttpResponse('ok')
    else:
        return HttpResponse('do nothing')

@csrf_exempt
def hp_restart_server(request):
    if request.method == 'POST':
        restart_cws = sp.run(['systemctl', 'restart', 'cws'])
        restart_cws_worker = sp.run(['systemctl', 'restart', 'cws_worker'])
        return HttpResponse('ok')
    else:
        return HttpResponse('do nothing.')

def chk_env(entrance):
    path_coverage_scripts = path_yakin + "/coverage/scripts"
    path_yakin_git = True
    tasks.chk_system_inuse.delay()
    if open('/tmp/covt_result', 'r').readlines()[-1].strip() != 'finish':
        return 'busy'

    if os.path.isdir(path_yakin) is False:
        exe_env_rsync_yakin = sp.run(['rsync -arvhq /home/coverage/yakin /home/lfsm/'], shell=True)

    process_httpserver = sp.run(['pgrep', '-cf', 'simple-cors-httpserver.py'], stdout=sp.PIPE)
    if int(process_httpserver.stdout.decode('utf-8').strip()) != 0:
        process_httpserver = sp.run(['pgrep', '-f', 'simple-cors-httpserver.py'], stdout=sp.PIPE)
        pid_httpserver = int(process_httpserver.stdout.decode("utf-8").split()[0])
        pk_httpserver = pid_killer(pid_httpserver)
    
    if entrance != 'hp_user_upload':
        try:
            git.Repo(path_yakin)
        except git.exc.InvalidGitRepositoryError:
            path_yakin_git = False

        if path_yakin_git is False:
            exe_env_rsync_yakin = sp.run(['rsync -arvhq /home/coverage/yakin /home/lfsm/'], shell=True)

    if os.path.isdir(path_coverage_scripts) is False:
        exe_env_rsync = sp.run(['rsync -arvhq --exclude=coverage_web_system --exclude=.git --exclude=yakin /home/coverage /home/lfsm/yakin/'], shell=True)

    if entrance != 'homepage':   
        websocket_consolelog = sp.run(['ps ax | grep 1234 -c'], shell=True, stdout=sp.PIPE)
        websocket_consolelog = int(websocket_consolelog.stdout.decode('utf-8').strip())
        if websocket_consolelog > 1:
            get_pid_websocket = sp.run(['pgrep', '-f', '1234'], stdout=sp.PIPE)
            pid_websocket = get_pid_websocket.stdout.decode('utf-8').split()
            for i in pid_websocket:
                pid_killer(int(i))

    if os.path.isfile('/tmp/covt_result') is False:
        return

def list_yakin_branch(yakin_branch):
    use_branch = 'local'
    act_branch = str(git.Repo('/home/lfsm/yakin').active_branch)
    reset_yakin_env = sp.run(['cd /home/lfsm/yakin && git checkout -- .'], shell=True)
    try:
        res_pull_latest_yakin = git.Git(path_yakin).pull()
    except:
        print('fail to git pull latest code.')
    branch_list = git.Git(path_yakin).branch(all=True).split('\n')
    if yakin_branch is 'all':
        re_branch_list = []
        for br in  branch_list:
            if 'remotes/origin/' in br:
                re_branch_list.append(br.replace('remotes/origin/', ''))
            elif 'HEAD' in br:
                return
            else:
                re_branch_list.append(br.strip('*'))
        return re_branch_list
    else:
        return act_branch

def list_test_case():
    src_scripts = path_coverage + '/scripts'
    path_testcase = path_yakin + '/coverage/scripts'

    # if os.path.isdir(path_testcase):
    change_case_mode = sp.run(['chmod +x /home/coverage/scripts/*'], shell=True)
    auto_sync_case = sp.run(['rsync', '-arvhq', src_scripts, path_yakin + '/coverage', '--delete'])

    all_file_list = os.listdir(path_testcase)
    filter_case = ['.awk', '.fio', '.scp', 'start.run']
    re_case_list = []
    for case in all_file_list:
        if any(x in case for x in filter_case):
            pass
        else:
            re_case_list.append(case)

    return re_case_list

def pid_killer(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return False
    else:
        return True