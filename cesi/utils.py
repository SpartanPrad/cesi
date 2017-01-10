from cesi import Config, Node, CONFIG_FILE
from flask import session

import requests
import urllib


def dashboard_info():
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
    node_count = 0
    node_name_list = []
    connected_count = []
    not_connected_count = 0
    environment_name_list = []
    usertype = 0
    node_name_list = Config(CONFIG_FILE).node_list
    node_count = len(node_name_list)
    environment_name_list = Config(CONFIG_FILE).environment_list

    for nodename in node_name_list:
        nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)

        try:
            node = Node(nodeconfig)
            if not nodename in connected_node_list:
                connected_node_list.append(nodename);
        except Exception as err:
            if not nodename in not_connected_node_list:
                not_connected_node_list.append(nodename);
            continue

        for name in node.process_dict2.keys():
            p_group = name.split(':')[0]
            p_name = name.split(':')[1]
            if p_group != p_name:
                if not p_group in group_list:
                    group_list.append(p_group)

        for process in node.process_list:
            all_process_count = all_process_count + 1
            if process.state == 20:
                running_process_count = running_process_count + 1
            if process.state == 0:
                stopped_process_count = stopped_process_count + 1

    # get environment list
    for env_name in environment_name_list:
        env_members = Config(CONFIG_FILE).getMemberNames(env_name)
        for index, node in enumerate(env_members):
            if not node in connected_node_list:
                env_members.pop(index);
        environment_list.append(env_members)

    for g_name in group_list:
        tmp = []
        for nodename in connected_node_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)
            node = Node(nodeconfig)
            for name in node.process_dict2.keys():
                group_name = name.split(':')[0]
                if group_name == g_name:
                    if not nodename in tmp:
                        tmp.append(nodename)
        g_node_list.append(tmp)

    for sublist in g_node_list:
        tmp = []
        for name in sublist:
            for env_name in environment_name_list:
                if name in Config(CONFIG_FILE).getMemberNames(env_name):
                    if name in connected_node_list:
                        if not env_name in tmp:
                            tmp.append(env_name)
        g_environment_list.append(tmp)

    connected_count = len(connected_node_list)
    not_connected_count = len(not_connected_node_list)
    output={}
    output['all_process_count']=all_process_count
    output['running_process_count']=running_process_count
    output['stopped_process_count']= stopped_process_count
    output['node_count'] = node_count
    output['node_name_list']= node_name_list
    output['connected_count']= connected_count
    output['not_connected_count'] = not_connected_count
    output['environment_list'] = environment_list
    output['environment_name_list'] = environment_name_list
    output['group_list'] = group_list
    output['g_environment_list'] = g_environment_list
    output['connected_node_list'] = connected_node_list
    output['not_connected_node_list'] = not_connected_node_list
    output['username'] = session['username']
    output['usertype'] = usertype
    output['usertypecode'] = session['usertype']
    return output


def otp_send(mobile_number,otp):
    message = "Use otp as {otp} for accessing portal".format(otp=otp)
    message = urllib.quote(message)
    requestUrl = "http://api-alerts.solutionsinfini.com/v3/?method=sms&api_key=A8aedaeb78654abbd47e299c40a51e014&to=" + mobile_number + "&sender=UNIPAY&message=" + message + "&format=json&custom=1,2&flash=0"
    res = requests.get(requestUrl)
    data = res.json()
    print data