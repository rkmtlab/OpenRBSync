from cmath import e
import datetime
import matplotlib.pyplot as plt
import socket

import argparse
import os

from pythonosc import dispatcher
from pythonosc import osc_server

import netifaces as ni
import psutil

def get_local_ip() -> list:
    if os.name == "nt":
        # Windows
        return socket.gethostbyname_ex(socket.gethostname())[2]
        pass
    else:
        # それ以外
        result = []
        address_list = psutil.net_if_addrs()
        for nic in address_list.keys():
            ni.ifaddresses(nic)
            try:
                ip = ni.ifaddresses(nic)[ni.AF_INET][0]['addr']
                if ip not in ["127.0.0.1"]:
                    result.append(ip)
            except KeyError as err:
                pass
        return result

#MY_IP = '172.27.254.84'
MY_IP='192.168.3.10'
#MY_IP='192.168.0.99' #rkmtlab
#host = socket.gethostname()
#MY_IP = socket.gethostbyname(host)
#MY_IP = get_local_ip()[0]
PORT = 8000
eeg_fname = ''
eeg = []
tlist = []


# TCPIP
def tcpip_eeg_init():
    '''
    This function 
    '''
    global eeg_fname

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default=MY_IP, help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=PORT, help="The port to listen on")
    args = parser.parse_args()

    #This will call eeg_handler for any OSC messages starting with /EEG
    disp = dispatcher.Dispatcher()
    disp.map('/EEG', eeg_handler_focuscalm)

    server = osc_server.BlockingOSCUDPServer((args.ip, args.port),dispatcher)
    print(f"Serving on {server.server_address}")
    server.serve_forever()

    ## log file name
    now = datetime.datetime.now()
    myroot = 'data'
    os.makedirs(myroot, exist_ok=True)
    snow = now.strftime('eeg-%y%m%d-%H%M')
    eeg_fname = "%s/%s.csv" % (myroot, snow)

# Handler of focuscalm
def eeg_handler_focuscalm(addr, arg1, arg2):
    global eeg, eeg_fname,sio,tlist
    print(f"my data: {addr} {arg2} {arg1}")
    
    # make a time list (since focuscalm output 50 data every 200ms)
    arg2_list = arg2.split(' ')
    h,m,s = arg2_list[1].split(':')
    s, ms = s.split('.')
    timef = datetime.timedelta(hours = int(h),minutes = int(m), seconds = int(s), milliseconds = int(ms))
    period = datetime.timedelta(milliseconds=200/50)
    dt_now = datetime.datetime.now()
    for i in range(50):
        timen = timef + period

        # convert timedelta object to datetime object
        hours = timen.seconds//3600
        minutes = (timen.seconds - hours * 3600)//60
        seconds = timef.seconds - 3600 * hours - 60 * minutes
        tlist.append(datetime.datetime(year = dt_now.year, month = dt_now.month, day = dt_now.day, 
                    hour = hours, minute = minutes, second = seconds, microsecond = timen.microseconds))
    
    # write down data on log file
    arg1_list = arg1.split(';')
    with open(eeg_fname, "a") as f:
        for i in range(50):
            f.write(f"{tlist[i]},{arg1_list[i]}\n")

    eeg += arg1_list
    if len(eeg) > 1000:
        eeg = eeg[-1000:]
        tlist = tlist[-1000:]
    for i in range(50):
        sio.emit('my message', {'timestamp': tlist[i],'eeg':arg1_list[i]})