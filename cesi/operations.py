from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash
from cesi import Config, Connection, Node, CONFIG_FILE, ProcessInfo, JsonValue

from config import ACTIVITY_LOG,get_db
from datetime import datetime
import cesi
from utils import dashboard_info
import xmlrpclib

import mmap
import os
import time
from flask import render_template, Blueprint



operations_blueprint = Blueprint('operations', __name__,)




@operations_blueprint.route('/activitylog')
def getlogtail():
    n=12
    try:
        if session.get('logged_in'):
            size = os.path.getsize(ACTIVITY_LOG)
            with open(ACTIVITY_LOG, "rb") as f:
                # for Windows the mmap parameters are different
                fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
            for i in xrange(size - 1, -1, -1):
                if fm[i] == '\n':
                    n -= 1
                    if n == -1:
                        break
                lines = fm[i + 1 if i else 0:].splitlines()
            return jsonify(status = "success",
                           log = lines)
    except Exception as err:
            return jsonify(status = "error",
                           messagge= err)
    finally:
            try:
                fm.close()
            except (UnboundLocalError, TypeError):
                return jsonify(status="error",
                               message = "Activity log file is empty")
            




# Dashboard
@operations_blueprint.route('/',methods = ['GET', 'POST'])
def showMain():
# get user type
    all_process_count = 0
    running_process_count = 0
    stopped_process_count = 0
    member_names = []
    environment_list = []
    g_node_list = []
    g_process_list = []
    g_environment_list = []
    group_list = []
    not_connected_node_list = []
    connected_node_list = []
    node_count=0
    node_name_list=[]
    connected_count=[]
    not_connected_count=0
    environment_name_list=[]
    usertype=0

    if 'application/json' in request.mimetype:
           return jsonify(dashboard_info())
    if session.get('logged_in'):
        if session['usertype']==0:
            usertype = "Admin"
        elif session['usertype']==1:
            usertype = "Standart User"
        elif session['usertype']==2:
            usertype = "Only Log"
        elif session['usertype']==3:
            usertype = "Read Only"
        output=dashboard_info()
        return render_template('index.html',
                               all_process_count=output.get('all_process_count'),
                               running_process_count=output.get('running_process_count'),
                               stopped_process_count=output.get('stopped_process_count'),
                               node_count=output.get('node_count'),
                               node_name_list=output.get('node_name_list'),
                               connected_count=output.get('connected_count'),
                               not_connected_count=output.get('not_connected_count'),
                               environment_list=output.get('environment_list'),
                               environment_name_list=output.get('environment_name_list'),
                               group_list=output.get('group_list'),
                               g_environment_list=output.get('g_environment_list'),
                               connected_node_list=output.get('connected_node_list'),
                               not_connected_node_list=output.get('not_connected_node_list'),
                               username=output.get('username'),
                               usertype=output.get('usertype'),
                               usertypecode=output.get('session'))

    else:
        return render_template('login.html')






# Show node
@operations_blueprint.route('/node/<node_name>')
def showNode(node_name):
    if session.get('logged_in'):
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - %s viewed node %s .\n"%( datetime.now().ctime(), session['username'], node_name ))
        return jsonify( process_info = Node(node_config).process_dict) 
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for view node %s .\n"%( datetime.now().ctime(), node_name ))
        return redirect(url_for('login'))

@operations_blueprint.route('/group/<group_name>/environment/<environment_name>')
def showGroup(group_name, environment_name):
    if session.get('logged_in'):
        env_memberlist = Config(CONFIG_FILE).getMemberNames(environment_name)
        process_list = []
        for nodename in env_memberlist:
            node_config = Config(CONFIG_FILE).getNodeConfig(nodename)
            try:
                node = Node(node_config)
            except Exception as err:
                continue
            p_list = node.process_dict2.keys()
            for name in p_list:
                if name.split(':')[0] == group_name:
                    tmp = []
                    tmp.append(node.process_dict2[name].pid)
                    tmp.append(name.split(':')[1])
                    tmp.append(nodename)
                    tmp.append(node.process_dict2[name].uptime)
                    tmp.append(node.process_dict2[name].state)
                    tmp.append(node.process_dict2[name].statename)
                    process_list.append(tmp)
        return jsonify(process_list = process_list)
    else:
        return redirect(url_for('login'))


@operations_blueprint.route('/node/<node_name>/process/<process_name>/restart')
def json_restart(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.stopProcess(process_name):
                    if node.connection.supervisor.startProcess(process_name):
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - %s restarted %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                        return JsonValue(process_name, node_name, "restart").success()
            except xmlrpclib.Fault as err:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsucces restart event %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                return JsonValue(process_name, node_name, "restart").error(err.faultCode, err.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for restart. Restart event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for restart to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return redirect(url_for('login'))

# Process start
@operations_blueprint.route('/node/<node_name>/process/<process_name>/start')
def json_start(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.startProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s started %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                    return JsonValue(process_name, node_name, "start").success()
            except xmlrpclib.Fault as err:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsucces start event %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                return JsonValue(process_name, node_name, "start").error(err.faultCode, err.faultString)
        else:   
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for start. Start event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for start to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return redirect(url_for('login'))

# Process stop
@operations_blueprint.route('/node/<node_name>/process/<process_name>/stop')
def json_stop(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.stopProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s stopped %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                    return JsonValue(process_name, node_name, "stop").success()
            except xmlrpclib.Fault as err:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsucces stop event %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                return JsonValue(process_name, node_name, "stop").error(err.faultCode, err.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for stop. Stop event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for stop to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return redirect(url_for('login'))

# Node name list in the configuration file
@operations_blueprint.route('/node/name/list')
def getlist():
    if session.get('logged_in'):
        node_name_list = Config(CONFIG_FILE).node_list
        return jsonify( node_name_list = node_name_list )
    else:
        return redirect(url_for('login'))

# Show log for process
@operations_blueprint.route('/node/<node_name>/process/<process_name>/readlog')
def readlog(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1 or session['usertype'] == 2:
            node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
            node = Node(node_config)
            log = node.connection.supervisor.tailProcessStdoutLog(process_name, 0, 500)[0]
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s read log %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify( status = "success", url="node/"+node_name+"/process/"+process_name+"/read" , log=log)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for read log. Read log event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify( status = "error", message= "You are not authorized for this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for read log to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return jsonify( status = "error", message= "First login please")









