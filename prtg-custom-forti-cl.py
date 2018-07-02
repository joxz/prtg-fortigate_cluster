from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import json
from paepy.ChannelDefinition import CustomSensorResult

class SNMPClient:

    # This is the SNMPClient constructor
    def __init__(self, host, port=161, community='public'):
        
        self.host = host
        self.port = port
        self.community = community
 
    def snmpget(self, oid, *more_oids):
 
        cmdGen = cmdgen.CommandGenerator()
         
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            oid,
            *more_oids
        )
 
        # Predefine our results list    
        results = {}
 
        # Check for errors and print out results
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    results[str(val)] = str(name)
 
        return results

    def snmpwalk(self, oid):

        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            oid
        )

        # Predefine our results list    
        results = {}

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        results[str(val)] = str(name)
            
        return results                        

# load PRTG parameters
params = json.loads(sys.argv[1])

conn = SNMPClient(params['host'], 161, params['snmpcommv2'])

# get serial numbers of cluster members
deviceSerialsHashtable = conn.snmpget('1.3.6.1.4.1.12356.101.13.2.1.1.2.1', '1.3.6.1.4.1.12356.101.13.2.1.1.2.2')

# switch keys and values and replace oid with unit number 
device = dict((v,k) for k,v in deviceSerialsHashtable.items())
device['unit1'] = device.pop('1.3.6.1.4.1.12356.101.13.2.1.1.2.1')
device['unit2'] = device.pop('1.3.6.1.4.1.12356.101.13.2.1.1.2.2')

for k,v in device.items():
    device[k] = {'serial': v}

for i in device:
    # construct snmp community for each cluster member
    device[i]['snmpc'] = params['snmpcommv2'] + '-' + device[i]['serial']

    # snmpwalk ifName OID
    conn = SNMPClient(params['host'], 161, device[i]['snmpc'])
    interfaces = conn.snmpwalk('1.3.6.1.2.1.31.1.1.1.1')

    # cut oid to interface id
    for k,v in interfaces.items():
        interfaces[k] = {'ifindex': v.replace("1.3.6.1.2.1.31.1.1.1.1.","")}

    # join to 'device' dict
    device[i]['int'] = interfaces

    # get cluster index of unit
    clindex = conn.snmpget('1.3.6.1.4.1.12356.101.13.2.1.1.1.' + i.replace('unit',''))
    for p in clindex.keys():
        device[i].update({'clindex': str(p)})

    # get hsotname
    hostname = conn.snmpget('1.3.6.1.4.1.12356.101.13.2.1.1.11.1')
    for p in hostname.keys():
        device[i].update({'hostname': str(p)})

    # get ifOperstatus for all interfaces
    for p in device[i]['int'].keys():
        ifstatus = conn.snmpget('1.3.6.1.2.1.2.2.1.8' + "." + device[i]['int'][p]['ifindex'])
        for k,v in ifstatus.items():
            device[i]['int'][p].update({'ifstatus': str(k)})

# create interface list from sensor additional parameters
iflist = params['params']

# create PRTG sensor channels
<<<<<<< HEAD
result = CustomSensorResult("Result from FortiGate Sensor " + params['host'])
for i in device:
    for k in device[i]['int'].keys():
        cname = device[i]['hostname'] + " " + k
        if k in iflist:
            if k == 'wan1' and device[i]['clIndex'] == '1':
                result.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'knauf.custom.lookup.forti.interfaces', primary_channel=True)
                #print(cname + " ifstatus: " + device[i]['int'][k]['ifstatus'])
            else:
                result.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'knauf.custom.lookup.forti.interfaces')
        else:
            pass

print(result.get_json_result())
=======
prtg = CustomSensorResult('OK')
for i in device:
    for k in device[i]['int'].keys():
        cname = device[i]['hostname'] + " " + k
        # set primary channel: inteface wan 1 of cluster unit 1
        if 'wan1' in k and device[i]['clIndex'] == '1':
            prtg.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'custom.lookup.forti.interfaces', primary_channel=True) 
        
        # other channels of interest 
        elif 'internal' in k:
            prtg.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'custom.lookup.forti.interfaces')
        elif 'dmz' in k:
            prtg.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'custom.lookup.forti.interfaces')
        elif 'ha' in k:
            prtg.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'custom.lookup.forti.interfaces')
        elif 'glt' in k:
            prtg.add_channel(channel_name = cname, value = device[i]['int'][k]['ifstatus'], value_lookup = 'custom.lookup.forti.interfaces')
        else:
            pass

print(prtg.get_json_result())
>>>>>>> a4fba2919790d4f42935d5c2a757e10f59954c45
