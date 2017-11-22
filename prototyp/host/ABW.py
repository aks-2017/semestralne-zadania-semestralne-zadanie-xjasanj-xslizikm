#!/usr/bin/python
import os
import sys
import json
import time
import subprocess
from collections import namedtuple
from timeit import default_timer

if len(sys.argv) <= 1:
 print "Pre spustenie programu je potrebne zadat argument: ako casto ma program vypisovat dostupny bandwidth v sekundach"
 print "Program je mozno ukoncit cez klavesovu skratku CTRL-C"
 sys.exit()
if int(sys.argv[1]) <= 0:
 sys.exit()
#ipadress of controller host
address="localhost"
SwitchToSwitchABW = namedtuple("SwitchToSwitchABW",["src_switch","dst_switch","availableBW"])
Link = namedtuple("Link",["src_switch","dst_switch"])
MyStruct = namedtuple("MyStruct",["linkBW","src_switch","dst_switch"])
MyStruct2 = namedtuple("MyStruct2",["linkBW","src_switch","dst_switch","src_port","dst_port"])
MyStruct3 = namedtuple("MyStruct3",["linkBW","src_switch","dst_switch","src_port","dst_port","availableBW"])
MyStruct4 = namedtuple("MyStruct4",["sender","reciever"])
LinkArray = []
time.sleep(10)
# Generate info about links in topology
os.system("curl -X GET http://"+address+":8080/wm/topology/links/json | python -m json.tool > links.json")
#enable statistics in floodlight
os.system("curl -X POST http://"+address+":8080/wm/statistics/config/enable/json")
# sem je potrebne vpisat vsetky kapacity linkov urcene v mininete
link1 = MyStruct(linkBW=10,src_switch="00:00:00:00:00:00:00:01",dst_switch="00:00:00:00:00:00:00:02")
link2 = MyStruct(linkBW=20,src_switch="00:00:00:00:00:00:00:02",dst_switch="00:00:00:00:00:00:00:03")
link3 = MyStruct(linkBW=10,src_switch="00:00:00:00:00:00:00:03",dst_switch="00:00:00:00:00:00:00:04")
link4 = MyStruct(linkBW=10,src_switch="00:00:00:00:00:00:00:02",dst_switch="00:00:00:00:00:00:00:04")
link5 = MyStruct(linkBW=5,src_switch="00:00:00:00:00:00:00:01",dst_switch="00:00:00:00:00:00:00:04")
## assignement of link capacity to switches
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
try:
 while True:
## calculate avalilible bandwith for every link DONE
    FinalArray = []
    for item in LinkArray:
           dstBWrx = subprocess.check_output('curl -X GET http://'+address+':8080/wm/statistics/bandwidth/' + item.dst_switch + '/' + str(item.dst_port) + '/json | python -m json.tool | grep rx | tr -dc \'0-9\'', shell=True)
           dstBWtx = subprocess.check_output('curl -X GET http://'+address+':8080/wm/statistics/bandwidth/' + item.dst_switch + '/' + str(item.dst_port) + '/json | python -m json.tool | grep tx | tr -dc \'0-9\'', shell=True)
           print item.dst_switch +';'+ str(item.dst_port) + 'BWrx:  ' + str(dstBWrx) + '  BWtx: ' + str(dstBWtx)
           dstBW = (int(dstBWrx)  + int(dstBWtx))
           FinalArray.append(MyStruct3(linkBW=item.linkBW,src_switch=item.src_switch,dst_switch=item.dst_switch,src_port=item.src_port,dst_port=item.dst_port,availableBW=(item.linkBW*1000000)-dstBW))
           print 'abc   ' + str(len(FinalArray))
           print ' BANDWIDTH cesta : ' + item.src_switch + 'dst  ' + item.dst_switch + '  SRC PORT : ' + str(item.src_port) + ' DST PORT : ' + str(item.dst_port) + '  '   + str(item.linkBW*1000000-dstBW)
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
##check all active flows besides controller generated ones -- and return distinct flows in network -DONE
    os.system("curl -X GET http://"+address+":8080/wm/core/switch/all/flow/json | python -m json.tool > flows.json")
    flows = []
    with open('flows.json') as json_flows:
     a = json.load(json_flows)
     for key in a:
      for key1 in a[key]:
       for key2 in a[key][key1]:
            if 'eth_src' in key2["match"]:
                tuple = (key2["match"]["eth_src"],key2["match"]["eth_dst"])
                flows.append(tuple)
     distinctFlowsList = list(set(flows))
     FlowsArray = []
     for key in distinctFlowsList:
      FlowsArray.append(MyStruct4(sender=key[0],reciever=key[1]))

## map hosts generating flows onto attachment point and get route betweeen hosts DONE
     os.system("rm route.json")
     SwitchAbwArray = []
     for keya in FlowsArray:
      for key in DeviceArray:
       if keya[0] == key[0]:
         src_dpid = key[1]
         src_port = key[2]
       elif keya[1] == key[0]:
         dst_dpid = key[1]
         dst_port = key[2]
      SwitchAbwArray.append(SwitchToSwitchABW(src_switch=src_dpid,dst_switch=dst_dpid,availableBW=0))
# create path from links -DONE
# need to Remove file route.json at the end of every cycle
      os.system("curl -X GET http://"+address+":8080/wm/routing/path/"+src_dpid+"/"+src_port+"/"+dst_dpid+"/"+dst_port+"/json | python -m json.tool > route.json")
      with open("route.json") as f:
       a = json.load(f)
       for key in a:
        b = 0
        SwitchArray = []
        for k in a[key][1:][:-1]:
         b = b+1
         if "switch" in k and b % 2 == 1:
          tmp = k["switch"]
         elif "switch" in k:
          SwitchArray.append(Link(src_switch=tmp,dst_switch=k["switch"]))
#calculate availible bandwidth
        minBW = 99999999999
        for i in SwitchArray:
         for j in FinalArray:
#          print "I src SWITCH: " + i.src_switch + "  j src switch  "+ j.src_switch +" I DST SWITCH  "+i.dst_switch+"  j DST SWITCH "+j.dst_switch+" AVAILIABLE BW :" + str(j.availableBW) + " MIN BW " + str(minBW)
          if ((i.src_switch == j.src_switch and i.dst_switch == j.dst_switch) and j.availableBW < minBW) or ((i.src_switch == j.dst_switch and i.dst_switch == j.src_switch) and j.availableBW < minBW) :
           minBW = j.availableBW
        #   print "AVAILABLEBANDWITH: " + str(j.availableBW)
         print "switche pre ktore vypisujeme bandwidth: SRC: " + i.src_switch + " DST: " + i.dst_switch
        print "dostupny bandwidth pre cestu : "  + str(minBW)
## TODO nejaky rozumny output do fileu
      # for i in FinalArray:
       #    duration = default_timer() - start
        #   f = open( 'file.log', 'a' )
         #  f.write( 'Link capacity: ' + str(i.linkBW) + ' src_switch: ' + i.src_switch + ' dst_switch: ' + i.dst_switch + ' Availiable bandwith: ' + str(i.availiableBW) + 'Bps time:' + str(duration) + ' \n' )
          # f.close()
         #  print i.src_switch + '  ' + i.dst_switch + '  availibleBW: =  ' + str(i.availiableBW)
    time.sleep(float(sys.argv[1]))
except KeyboardInterrupt:
# remove temp files needed for bandwidth calculation
  os.system("rm links.json")
  os.system("rm flows.json")
  os.system("rm route.json")
  os.system("rm devices.json")
  print("program bol ukonceny")
# pushovat flowy cez staticflowpusherAPI
