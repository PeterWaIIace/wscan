import threading
import os, time 
import random 
from scapy.all import *

addresses = [] # transmitters 
AP = {} #Acces Points

def findSSID(pkt):
    device=pkt.getlayer(Dot11)
    if device.addr2 not in addresses:
        addresses.append(device.addr2)
        if pkt.haslayer(Dot11Beacon):
            ssid = pkt.getlayer(Dot11Elt).info
            print(device.addr1,device.addr2,device.addr3,device.payload.name,ssid)
            AP[device.addr2] = ssid
        else:
            if device.addr1 in AP:
                print(AP[device.addr1],device.addr2,device.addr3,device.payload.name)
            else: 
                print(device.addr1,device.addr2,device.addr3,device.payload.name)

def hopper(interface):
    n = 1
    stop_hopper = False
    while not stop_hopper:
        time.sleep(0.5)
        os.system('iwconfig %s channel %d' % (interface, n))
        # print(f"channel {n}")
        n = random.randint(1,13)
        
if __name__=="__main__":
    interface = 'interface_name'
    thread = threading.Thread(target=hopper, args=(interface, ), name="hopper")
    thread.daemon = True
    thread.start()

    sniff(iface=interface, prn=findSSID)

    while True:
        pass