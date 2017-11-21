#!/usr/bin/python
import os
import json
import time
import subprocess
from collections import namedtuple
from timeit import default_timer

#ipadress of controller host
address="localhost"

MyStruct = namedtuple("MyStruct",["linkBW","src_switch","dst_switch"])
MyStruct2 = namedtuple("MyStruct2",["linkBW","src_switch","dst_switch","src_port","dst_port"])
MyStruct3 = namedtuple("MyStruct3",["linkBW","src_switch","dst_switch","src_port","dst_port","availiableBW"])
LinkArray = []
# Generate info about links in topology
os.system("curl -X GET http://"+address+":8080/wm/topology/links/json | python -m json.tool > links.json")
#enable statistics in floodlight
#os.system("curl -X POST http://"+address+":8080/wm/statistics/config/enable/json")
# sem je potrebne vpisat vsetky kapacity linkov urcene v mininete
link1 = MyStruct(linkBW=10,src_switch="00:00:00:00:00:00:00:01",dst_switch="00:00:00:00:00:00:00:02")
link2 = MyStruct(linkBW=20,src_switch="00:00:00:00:00:00:00:02",dst_switch="00:00:00:00:00:00:00:03")
link3 = MyStruct(linkBW=10,src_switch="00:00:00:00:00:00:00:03",dst_switch="00:00:00:00:00:00:00:04")
link4 = MyStruct(linkBW=10,src_switch="00:00:00:00:00:00:00:02",dst_switch="00:00:00:00:00:00:00:04")
link5 = MyStruct(linkBW=5,src_switch="00:00:00:00:00:00:00:01",dst_switch="00:00:00:00:00:00:00:04")
## priradenie kapacit linkov k switchom a portom
with open('links.json') as json_links:
    a = json.load(json_links)
    for value1 in a:
      if value1['src-switch'] == link1[1] and value1['dst-switch'] == link1[2]:
        LinkArray.append(MyStruct2(linkBW=link1[0],src_switch=value1['src-switch'],dst_switch=value1['dst-switch'],src_port=value1['src-port'],dst_port=value1['dst-port']))
      elif value1['src-switch'] == link2[1] and value1['dst-switch'] == link2[2]:
        LinkArray.append(MyStruct2(linkBW=link2[0],src_switch=value1['src-switch'],dst_switch=value1['dst-switch'],src_port=value1['src-port'],dst_port=value1['dst-port']))
      elif value1['src-switch'] == link3[1] and value1['dst-switch'] == link3[2]:
        LinkArray.append(MyStruct2(linkBW=link3[0],src_switch=value1['src-switch'],dst_switch=value1['dst-switch'],src_port=value1['src-port'],dst_port=value1['dst-port']))
      elif value1['src-switch'] == link4[1] and value1['dst-switch'] == link4[2]:
        LinkArray.append(MyStruct2(linkBW=link4[0],src_switch=value1['src-switch'],dst_switch=value1['dst-switch'],src_port=value1['src-port'],dst_port=value1['dst-port']))
      elif value1['src-switch'] == link5[1] and value1['dst-switch'] == link5[2]:
        LinkArray.append(MyStruct2(linkBW=link5[0],src_switch=value1['src-switch'],dst_switch=value1['dst-switch'],src_port=value1['src-port'],dst_port=value1['dst-port']))
start = default_timer()
while True:
    #check attachement points of all hosts DONE
    os.system("curl -X GET http://"+address+":8080/wm/device/ | python -m json.tool > devices.json")
    DeviceArray = []
    HostStruct = namedtuple("HostStruct",["mac","switch","port"])
    with open('devices.json') as json_devices:
     a = json.load(json_devices)
     for key in a:
      for key1 in a[key]:
       mac = key1["mac"][0]
       for key2 in key1["attachmentPoint"]:
         DeviceArray.append(HostStruct(mac=mac,switch=key2["switch"],port=key2["port"]))
##check all active flows besides controller generated ones -- TODO
#os.system("curl -X GET http://"+address+":8080/wm/core/switch/all/flow/json | python -m json.tool > flows.json")

## map hosts generating flows onto attachment point and get route betweeen hosts TODO
#os.system("curl -X GET http://"+address+"8080/wm/routing/path/<src-dpid>/<src-port>/<dst-dpid>/<dst-port>/json | python -m json.tool > route.json")

## create path from links TODO
##
## calculate avalilible bandwith for every link DONE
    FinalArray = []
    for item in LinkArray:
           dstBWrx = subprocess.check_output('curl -X GET http://'+address+':8080/wm/statistics/bandwidth/' + item.dst_switch + '/' + str(item.dst_port) + '/json | python -m json.tool | grep rx | tr -dc \'0-9\'', shell=True)
           dstBWtx = subprocess.check_output('curl -X GET http://'+address+':8080/wm/statistics/bandwidth/' + item.dst_switch + '/' + str(item.dst_port) + '/json | python -m json.tool | grep tx | tr -dc \'0-9\'', shell=True)
           print 'BWrx:  ' + str(dstBWrx) + '  BWtx: ' + str(dstBWtx)
           dstBW = (int(dstBWrx) + int(dstBWtx))
           FinalArray.append(MyStruct3(linkBW=item.linkBW,src_switch=item.src_switch,dst_switch=item.dst_switch,src_port=item.src_port,dst_port=item.dst_port,availiableBW=(item.linkBW*1000000)-dstBW))
           print 'abc   ' + str(len(FinalArray))
    for i in FinalArray:
           duration = default_timer() - start
           f = open( 'file.log', 'a' )
           f.write( 'Link capacity: ' + str(i.linkBW) + ' src_switch: ' + i.src_switch + ' dst_switch: ' + i.dst_switch + ' Availiable bandwith: ' + str(i.availiableBW) + 'Bps time:' + str(duration) + ' \n' )
           f.close()
           print i.src_switch + '  ' + i.dst_switch + '  availibleBW: =  ' + str(i.availiableBW)
    time.sleep(30)
#TODO pushovat flowy cez staticflowpusherAPI
