# prtg-fortigate_cluster
PRTG custom sensor to query both units behind the virtual management IP

[Fortinet Link for Monitoring HA Clusters][forti-link]

Sample Data Structure:

```
{'unit1': {'clIndex': '1',
           'hostname': 'de-xxx-fw02',
           'int': {'dmz': {'ifIndex': '3', 'ifstatus': '1'},
                   'internal': {'ifIndex': '101', 'ifstatus': '1'},
                   'internal7': {'ifIndex': '110', 'ifstatus': '1'},
                   'modem': {'ifIndex': '6', 'ifstatus': '2'},
                   'npu0_vlink0': {'ifIndex': '4', 'ifstatus': '2'},
                   'npu0_vlink1': {'ifIndex': '5', 'ifstatus': '2'},
                   'ssl.root': {'ifIndex': '7', 'ifstatus': '1'},
                   'wan1': {'ifIndex': '1', 'ifstatus': '1'},
                   'wan2': {'ifIndex': '2', 'ifstatus': '2'}},
           'serial': 'FGT60E4Q855555455',
           'snmpc': 'public-FGT60E4Q855555455'},
 'unit2': {'clIndex': '2',
           'hostname': 'de-xxx-fw01',
           'int': {'dmz': {'ifIndex': '3', 'ifstatus': '1'},
                   'internal': {'ifIndex': '101', 'ifstatus': '1'},
                   'internal7': {'ifIndex': '110', 'ifstatus': '1'},
                   'modem': {'ifIndex': '6', 'ifstatus': '2'},
                   'npu0_vlink0': {'ifIndex': '4', 'ifstatus': '2'},
                   'npu0_vlink1': {'ifIndex': '5', 'ifstatus': '2'},
                   'ssl.root': {'ifIndex': '7', 'ifstatus': '1'},
                   'wan1': {'ifIndex': '1', 'ifstatus': '1'},
                   'wan2': {'ifIndex': '2', 'ifstatus': '2'}},
           'serial': 'FGT60E4Q56565656565',
           'snmpc': 'public-FGT60E4Q56565656565'}}
```

Sample Sensor Output:

```json
6/21/2018 12:28:15 PM Exit Code: 0
6/21/2018 12:28:15 PM RawStream Size: 458
6/21/2018 12:28:15 PM OutputStream Size: 458
6/21/2018 12:28:15 PM Script Output (UTF8 Encoding): {"prtg": {"text": "Result from FortiGate Sensor 10.0.16.7", "result": [{"Channel": "de-xxx-fw02 WAN1", "Value": 1, "Unit": "Custom"}, {"Channel": "de-xxx-fw02 INTERNAL", "Value": 1, "Unit": "Custom"}, {"Channel": "de-xxx-fw02 DMZ", "Value": 1, "Unit": "Custom"}, {"Channel": "de-xxx-fw01 WAN1", "Value": 1, "Unit": "Custom"}, {"Channel": "de-xxx-fw01 INTERNAL", "Value": 1, "Unit": "Custom"}, {"Channel": "de-xxx-fw01 DMZ", "Value": 1, "Unit": "Custom"}]}}, "Channel": "de-xxx-fw01 DMZ"}]}}
```

[forti-link]: http://help.fortinet.com/fos50hlp/54/Content/FortiOS/fortigate-high-availability-52/HA_operatingSNMP.htm