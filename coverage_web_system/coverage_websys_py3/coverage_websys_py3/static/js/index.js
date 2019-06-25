// jQuery.fn.center = function () {
//     this.css("position","absolute");
//     this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");
//     this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + 
//     $(window).scrollLeft()) + "px");
//     return this;
// };

// get server ip
var use_server_ip = location.host;
document.getElementById("h_header_content").href = 'http://' + use_server_ip + '/';

// go test history
var history_page = ':8080/';
// var history_page = '/test-history/browse';

// get system state
var get_system_state = new WebSocket('ws://' + use_server_ip + ':1230/');
waitForSocketConnection(get_system_state);
setInterval(getsystemstate, 0.1)
function getsystemstate() {
    get_system_state.onmessage = function(e) {
        if (e.data == 'finish') {
            document.getElementById('system_state').innerHTML = '<font color="grey">( System is Free )</font>';
        } else {
            document.getElementById('system_state').innerHTML = '<font color="red">( System is Busy )</font>';
        }
    }
}

// default block console log
document.getElementById("console").style.display = "block";

// branch search box
searchBox = document.getElementById("branch_searchBox");
hp_select_branch = document.getElementById("hp_select_branch");
var when = "keyup"; //You can change this to keydown, keypress or change
searchBox.addEventListener(when, function(e) {
    var text = e.target.value; //searchBox value
    var options = hp_select_branch.options; //select options
    for (var i = 0; i < options.length; i++) {
        var option = options[i]; //current option
        var optionText = option.text;
        var lowerOptionText = optionText.toLowerCase(); //option text lowercased for case insensitive testing
        var lowerText = text.toLowerCase(); //searchBox value lowercased for case insensitive testing
        var regex = new RegExp("^" + text, "i"); //regExp, explained in post
        var match = optionText.match(regex); //test if regExp is true
        var contains = lowerOptionText.indexOf(lowerText) != -1; //test if searchBox value is contained by the option text
        if (match || contains) { //if one or the other goes through
            option.selected = true; //select that option
            return; //prevent other code inside this event from executing
        }
        searchBox.selectedIndex = 0; //if nothing matches it selects the default option
    }
});

async function restart_everything() {
    let url = 'http://' + use_server_ip + '/cws/hp_restart_server';
    let req = $.ajax({
        async: true,
        url: url,
        type: 'POST',
        dataType: 'json',
    })
    
    document.getElementById("d-reload").style.display = "block";
    
    await sleep(5000);
    window.location.reload();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function switchlogtab(evt, log_type) {
    let i, tabcontent, tablinks;

    // get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("btn btn-secondary");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace("active", "");
    }

    // show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(log_type).style.display = "block";
    evt.currentTarget.className += " active";
}

function branch_selector(sel) {
    sel_branch = sel.options[sel.selectedIndex].text;
    document.getElementById("commit_id").value = sel_branch;
}

function check_out() {
    let check_out_id = document.getElementById("commit_id").value;
    let url = 'http://' + use_server_ip + '/cws/hp_checkout_git';
    let op = {
        'commit_id': check_out_id
    }
    if (check_out_id == "") {
        document.getElementById("check_out_id").innerHTML = "<span style='color: red;'> commit id empty ... </span>";
    } else {
        document.getElementById("commit_id").value = "";
        // document.getElementById("check_out_id").innerHTML = "checkout to ..." + check_out_id;
        let res = $.ajax({
            async: false,
            url: url,
            type: "POST",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(op),
            // success: function(XMLHttpRequest) {
            //     alert(String(XMLHttpRequest.responseText));
            // },
            // error: function(XMLHttpRequest) {
            //     alert(String(XMLHttpRequest.responseText));
            // }
        });

        if (res.responseText == 'systemisbusy') {
            alert('System is busy. Please try again later');
            return;
        }

        if (res.status == 200) {
            if (res.responseText == 'didnotmatchanybranch') {
                alert('did not match any branch, please check.');
                return;
            }
            document.getElementById("check_out_id").innerHTML = "checkout to " + check_out_id + " ...... Ok";
            document.getElementById('current_branch').innerHTML = check_out_id;
        } else {
            document.getElementById("check_out_id").innerHTML = "<span style='color: red;'> checkout to " + check_out_id + " ...... Fail </span>";
        }
    }
}

function select_case() {
    let b_close = document.getElementById("select_case_box_header_close");
    let b_apply = document.getElementById("select_case_box_bottom_apply");

    document.getElementById('select_case_box').style.display = "block";

    b_close.onclick = function() {
        document.getElementById('select_case_box').style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == document.getElementById('select_case_box')) {
            document.getElementById('select_case_box').style.display = "none";
        }
    }

    b_apply.onclick = function() {
        document.getElementById('select_case_box').style.display = "none";
        let seled_box = document.getElementById("selected_cased");
        let l_console = document.getElementById("return_log_a");
        let j = 1;
        let user_cases = [];
        let url = 'http://' + use_server_ip + '/cws/hp_chk_case';

        for (i = 0; i < seled_box.options.length; i++) {
            let t_case = seled_box.options[i].text;
            user_cases.push(t_case);
            if (i == 0) {
                l_console.innerHTML += '[info] selected test case :' + '<br>' + '(' + j + ') ' + t_case + '<br>';
            } else {
                l_console.innerHTML += '(' + j + ') ' + t_case + '<br>';
            }
            j++;
        }

        l_console.innerHTML += '<br>';

        let data = {
            case: user_cases,
        };

        let req = $.ajax({
            async: false,
            url: url,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
        })

        if (req.responseText == 'systemisbusy') {
            alert('System is busy. Please try again later');
            return;
        }
    }

    removeOptions(document.getElementById("selected_cased"));
}

function case_selector(sel) {
    let sel_case = sel.options[sel.selectedIndex].text;

    let seled_case = document.getElementById("selected_cased");
    let opt = document.createElement('option');
    opt.value = sel_case;
    opt.innerHTML = sel_case;
    seled_case.appendChild(opt);
}

function cased_selector(sel) {
    let seled_case = sel.options[sel.selectedIndex].text;

    let seled_box = document.getElementById("selected_cased");
    seled_box.options[seled_box.selectedIndex].remove();
}

function select_all(op) {
    let case_box = document.getElementById("select_case").options;
    let sel_case_box = document.getElementById("selected_cased");
    if (op == 'all') {
        for (i = 0; i < case_box.length; i ++) {
            opt = document.createElement('option');
            opt.value = case_box[i].text;
            opt.text = case_box[i].text;
            sel_case_box.add(opt);
        }
    } else {
        removeOptions(document.getElementById("selected_cased"));
    }
}

function removeOptions(selectbox) {
    for (let i = selectbox.options.length - 1 ; i >= 0 ; i--) {
        selectbox.remove(i);
    }
}

function waitForSocketConnection(socket, callback) {
    setTimeout(
        function () {
            if (socket.readyState === 1) {
                console.log(socket.url + " connection is made");
                if(callback != null){
                    callback();
                }
                return;
            } else {
                console.log("wait for connection...")
                waitForSocketConnection(socket, callback);
            }
        }, 1000);
}

function start_test() {
    let url = 'http://' + use_server_ip + '/cws/hp_run_testing';
    let op = {
        'start_t': 'start_t',
    }

    let req = $.ajax({
        async: false,
        url: url,
        type: "post",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(op)
    })

    if (req.responseText == 'systemisbusy') {
        alert('System is busy. Please try again later');
        return;
    }

    let consolelog_url = 'http://' + use_server_ip + ':1234/';
    let syslog_url = 'http://' + use_server_ip + ':1235/';

    let ws_case_result = new WebSocket('ws://' + use_server_ip + ':1231/');
    let ws_consolelog_url = new WebSocket('ws://' + use_server_ip + ':1234/');
    // let ws_syslog_url = new WebSocket('ws://' + use_server_ip + ':1235/');

    waitForSocketConnection(ws_case_result);
    waitForSocketConnection(ws_consolelog_url);

    // new EventSource(consolelog_url).onmessage = function(e) {
    ws_consolelog_url.onmessage = function(e) {
        $('#return_log_a').append(e.data + '<br/>');
        document.getElementById("console").scrollTop = document.getElementById("console").scrollHeight;
    };

    ws_case_result.onmessage = function(e) {
        $('#return_log_case_result').append(e.data + '<br/>');
        document.getElementById("case_result").scrollTop = document.getElementById("case_result").scrollHeight;
    }

    new EventSource(syslog_url).onmessage = function(e) {
    // ws_syslog_url.onmessage = function(e) {
        $('#return_log_b').append(e.data + '<br/>');
        document.getElementById("syslog").scrollTop = document.getElementById("syslog").scrollHeight;
    };

    // ws_syslog_url.onerror = function(e) {
    //     console.log('p1235 error in connection.')
    // }

    var wait_conter = 0;
    var wait_message = ["waitting for output", "waitting for output .", "waitting for output ..", "waitting for output ..."];
    var interval_chk_result = setInterval(function chk_testing_result() {
        let out_url = 'http://' + use_server_ip + ':8000/';
        let xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                if (xmlhttp.status == 200) {
                    console.log(out_url + " connection is made.")
                    document.getElementById("h_result_box_body").innerHTML = '<object type="text/html" width="100%" height="100%" data="http://' + use_server_ip + ':8000/"></object>';
                    clearInterval(interval_chk_result);
                } else {
                    if (wait_message[wait_conter] != undefined) {
                        document.getElementById("h_result_box_body").innerHTML = wait_message[wait_conter];
                    }
                }
            }
        }
        xmlhttp.open( "GET", out_url, true);
        xmlhttp.send();
        wait_conter++;
        if (wait_conter > wait_message.length -1) {
            wait_conter = 0;
        }
    }, 1000);
}

async function waiting_for_result_html() {
    let wait_conter = 0;
    let wait_message = ["waitting for output", "waitting for output .", "waitting for output ..", "waitting for output ..."];
    let res = 0;
    let result_url = 'http://' + use_server_ip + ':8000/';

    while (res != 200) {
        let res = $.ajax({
            async: false,
            url: result_url,
            type: 'get',
        })
        if (res.status == 200) {
            let res = 200;
            console.log(result_url + "connection is made.")
            document.getElementById("h_result_box_body").innerHTML = '<object type="text/html" width="100%" height="100%" data="http://' + use_server_ip + ':8000/"></object>';
            return;
        } else {
            document.getElementById("h_result_box_body").innerHTML = wait_message[wait_conter];
        }
        wait_conter++;
        if (wait_conter > wait_message.length - 1) {
            wait_conter = 0;
        }

        await sleep(1000);
    }
}

function gen_result_html() {
    let url = 'http://' + use_server_ip + '/cws/hp_gen_result_html';
    let op = {
        'op': 'gen_res_html',
    }
    let res = $.ajax({
        async: false,
        url: url,
        type: "POST",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(op),
    });
    let l_console = document.getElementById("return_log_a");
    if (res.status == 200) {
        l_console.innerHTML += '[info] generate result html, ' + '<a href="http://' + use_server_ip + ':8000/" target="_blank">click me</a>' + '<br>';
    }
}

function user_upload() {
    let hp_user_upload = document.getElementById("h_user_upload");
    let hp_user_upload_ok = document.getElementById("list_user_upload_ok");

    hp_user_upload.style.display = "block";

    let ob_upload_file = document.getElementById("list_user_upload");

    hp_user_upload_ok.onclick = function() {
        hp_user_upload.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == hp_user_upload ) {
            hp_user_upload.style.display = "none";
        }
    }
}

function select_user_upload(self) {
    if (self.checked) {
        self.classList.add("marked");
    } else {
        self.classList.remove("marked");
    }

    if (document.getElementsByClassName("marked").length > 1) {
        alert("ONLY ONE can be selected at a time.");
        self.checked = false;
        self.classList.remove("marked");
    } else {
        user_upload_selected = self.value;
        let h_console = document.getElementById("return_log_a");
        document.getElementById("list_user_upload_ok").onclick = function() {
            h_console.innerHTML += '[info] use upload yakin:' + '<br>' + user_upload_selected + '<br><br>';
            document.getElementById("h_user_upload").style.display = "none";
            let url = 'http://' + use_server_ip + '/cws/hp_user_upload';
            let op = {
                'op_name': 'use_user_upload',
                'op_content': user_upload_selected,
            }
            let res = $.ajax({
                async: false,
                url: url,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(op),
            });

            if (res.responseText == 'systemisbusy') {
                alert('System is busy. Please try again later');
                return;
            }

            // if (res.status == 200) {
            //     h_console.innerHTML += res.responseText;
            // }
        }
    }
}

function get_result() {
    let close_result = document.getElementById("h_result_box_content_close");
    let result_box = document.getElementById('h_result_box');

    result_box.style.display = "block";

    window.onclick = function(event) {
        if (event.target == result_box) {
            result_box.style.display = "none";
        }
    }
    
    close_result.onclick = function() {
        result_box.style.display = "none";
    }
}

function go_history() {
    let history_box = document.getElementById('h_history_box');
    let close_history_box = document.getElementById("h_history_box_content_close");
    let pageup_history_box = document.getElementById("h_history_box_content_header0_pageup");
    let pagedown_history_box = document.getElementById("h_history_box_content_header0_pagedown");
    let back_history_box = document.getElementById("h_history_box_content_header0_back");

    history_box.style.display = "block";
    document.getElementById("h_history_box_body").innerHTML = '<object type="text/html" width="100%" height="100%" data="http://' + use_server_ip + history_page + '"></object>';

    window.onclick = function(event) {
        if (event.target == history_box) {
            history_box.style.display = "none";
        }
    }

    back_history_box.onclick = function() {
        document.getElementById("h_history_box_body").innerHTML = '<object type="text/html" width="100%" height="100%" data="http://' + use_server_ip + history_page + '"></object>';
    }
    
    close_history_box.onclick = function() {
        history_box.style.display = "none";
    }
}

function ws_demo() {
    let ws_url = "ws://" + window.location.host;
    let ws = new WebSocket(ws_url);
    let msg = {
        id: "01",
        name: "hank",
        message: "hello",
    }
    ws.onopen = function(e) {
        console.log("ws open");
        ws.send(JSON.stringify({
            id: '001',
            username: 'hank',
            message: 'seeya'
        }))
    };
    ws.onmessage = function(e) {
        console.log('ws get messages:' + e.data);
        $('#return_log_c').append(e.data);
    };
    ws.onclose = function(e) {
        console.log("ws close");
    };
}