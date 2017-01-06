url : http://localhost:5000/node/Node157 method: GET

```
{
  "process_info": [
    {
      "description": "pid 23281, uptime 3:32:10",
      "exitstatus": 0,
      "group": "portal_jpos",
      "logfile": "/apps/portal_jpos/portal_jpos/install/jpos/log/supervisor-access.log",
      "name": "portal_jpos",
      "now": 1483536544,
      "pid": 23281,
      "spawnerr": "",
      "start": 1483523814,
      "state": 20,
      "statename": "RUNNING",
      "stderr_logfile": "/apps/portal_jpos/portal_jpos/install/jpos/log/supervisor-error.log",
      "stdout_logfile": "/apps/portal_jpos/portal_jpos/install/jpos/log/supervisor-access.log",
      "stop": 1483523094
    },
    {
      "description": "pid 6388, uptime 12 days, 2:05:34",
      "exitstatus": 0,
      "group": "portal_jposdr",
      "logfile": "/appsdr/portal_jposdr/portal_jposdr/install/jpos/log/supervisor-access.log",
      "name": "portal_jposdr",
      "now": 1483536544,
      "pid": 6388,
      "spawnerr": "",
      "start": 1482492210,
      "state": 20,
      "statename": "RUNNING",
      "stderr_logfile": "/appsdr/portal_jposdr/portal_jposdr/install/jpos/log/supervisor-error.log",
      "stdout_logfile": "/appsdr/portal_jposdr/portal_jposdr/install/jpos/log/supervisor-access.log",
      "stop": 1482492210
    },
    {
      "description": "Exited too quickly (process log may have details)",
      "exitstatus": 0,
      "group": "tomcat-unipaynext",
      "logfile": "/apps/portal_jpos/portal_jpos/install/jpos/log/supervisor-access.log",
      "name": "tomcat-unipaynext",
      "now": 1483536544,
      "pid": 0,
      "spawnerr": "Exited too quickly (process log may have details)",
      "start": 1481785398,
      "state": 200,
      "statename": "FATAL",
      "stderr_logfile": "/apps/portal_jpos/portal_jpos/install/jpos/log/supervisor-error.log",
      "stdout_logfile": "/apps/portal_jpos/portal_jpos/install/jpos/log/supervisor-access.log",
      "stop": 1481785398
    },
    {
      "description": "pid 6156, uptime 12 days, 2:12:29",
      "exitstatus": 0,
      "group": "unipaynext_jpos",
      "logfile": "/apps/unipaynext_jpos/unipaynext_jpos/install/jpos/log/supervisor-access.log",
      "name": "unipaynext_jpos",
      "now": 1483536544,
      "pid": 6156,
      "spawnerr": "",
      "start": 1482491795,
      "state": 20,
      "statename": "RUNNING",
      "stderr_logfile": "/apps/unipaynext_jpos/unipaynext_jpos/install/jpos/log/supervisor-error.log",
      "stdout_logfile": "/apps/unipaynext_jpos/unipaynext_jpos/install/jpos/log/supervisor-access.log",
      "stop": 1482491744
    },
    {
      "description": "pid 15560, uptime 13 days, 3:44:45",
      "exitstatus": 0,
      "group": "unipaynext_jposdr",
      "logfile": "/appsdr/unipaynext_jposdr/unipaynext_jposdr/install/jpos/log/supervisor-access.log",
      "name": "unipaynext_jposdr",
      "now": 1483536544,
      "pid": 15560,
      "spawnerr": "",
      "start": 1482399859,
      "state": 20,
      "statename": "RUNNING",
      "stderr_logfile": "/appsdr/unipaynext_jposdr/unipaynext_jposdr/install/jpos/log/supervisor-error.log",
      "stdout_logfile": "/appsdr/unipaynext_jposdr/unipaynext_jposdr/install/jpos/log/supervisor-access.log",
      "stop": 1482399859
    }
  ]
}
```

url : http://localhost:5000/node/name/list Method: GET

```
{"node_name_list": ["Node157", "Node179", "Node141", "Node220", "mysql", "pycharm"]}

```

url: http://localhost:5000/node/Node157/process/portal_jpos/readlog Method: GET

```
{
  "log": "0\"/>\n  <field id=\"58\" value=\"0,180.151.248.197:20041\"/>\n  <field id=\"59\" value=\"0,180.151.248.197:20041,edc,null,null\"/>\n  <field id=\"60\" value=\"111:000\"/>\n  <field id=\"61\" value=\"0,180.151.248.197:20040\"/>\n  <field id=\"62\" value=\"0,180.151.248.197:20040\"/>\n  <field id=\"63\" value=\"#00060002:0:0:0:13:16#ENDED546:0:1:1:00:16\"/>\n</isomsg>\n2017-01-04 17:12:25.253  INFO [ DbConnection:closeCfgDBConnection:222 ] Session Count While Closing DB Connection : 0 - Thread activeCount : 1\n<peer-disconnect/>\n",
  "status": "success",
  "url": "node/Node157/process/portal_jpos/read"
}

```

url : http://localhost:5000/group/portal_jpos/environment/QASetup  Method

```
{
  "process_list": [
    [
      23281,
      "portal_jpos",
      "Node157",
      "2:01:24",
      20,
      "RUNNING"
    ]
  ]
}
```

url : http://localhost:5000/node/Node179/process/unipaynext_jpos_1/start  Method : POST

```
{
  "code": 80,
  "data": {
    "description": "pid 28422, uptime 0:00:03",
    "exitstatus": 0,
    "group": "unipaynext_jpos_1",
    "logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-access.log",
    "name": "unipaynext_jpos_1",
    "now": 1483535934,
    "pid": 28422,
    "spawnerr": "",
    "start": 1483535931,
    "state": 20,
    "statename": "RUNNING",
    "stderr_logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-error.log",
    "stdout_logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-access.log",
    "stop": 1482212229
  },
  "message": "Node179 unipaynext_jpos_1 start event succesfully",
  "nodename": "Node179",
  "status": "Success"
}

```

url : http://localhost:5000/node/Node179/process/unipaynext_jpos_1/stop  Method : GET

```
{
  "code": 80,
  "data": {
    "description": "Jan 04 06:50 PM",
    "exitstatus": 143,
    "group": "unipaynext_jpos_1",
    "logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-access.log",
    "name": "unipaynext_jpos_1",
    "now": 1483536005,
    "pid": 0,
    "spawnerr": "",
    "start": 1483535931,
    "state": 0,
    "statename": "STOPPED",
    "stderr_logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-error.log",
    "stdout_logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-access.log",
    "stop": 1483536005
  },
  "message": "Node179 unipaynext_jpos_1 stop event succesfully",
  "nodename": "Node179",
  "status": "Success"
}

```

url : http://localhost:5000/node/Node179/process/unipaynext_jpos_1/restart  Method : GET

```

{
  "code": 80,
  "data": {
    "description": "pid 28487, uptime 0:00:01",
    "exitstatus": 0,
    "group": "unipaynext_jpos_1",
    "logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-access.log",
    "name": "unipaynext_jpos_1",
    "now": 1483537267,
    "pid": 28487,
    "spawnerr": "",
    "start": 1483537266,
    "state": 20,
    "statename": "RUNNING",
    "stderr_logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-error.log",
    "stdout_logfile": "/apps/unipaynext_jpos_1/unipaynext_jpos_1/install/jpos/log/supervisor-access.log",
    "stop": 1483537266
  },
  "message": "Node179 unipaynext_jpos_1 restart event succesfully",
  "nodename": "Node179",
  "status": "Success"
}

```
