import socketio
import threading

import eeg
import bitalino

sio = socketio.Client()
#hostip = '10.209.30.44'
#hostip = '172.27.254.84'
hostip = '192.168.3.10'
hostaddr = 3030

# signal flags
ecg_flag = False
eeg_flag = False
eda_flag = False
emg_flag = False
focuscalm_flag = False
bitalino_flag = False


# Define the MAC-address of the acquisition device used in OpenSignals
mac_address = "98:D3:B1:FD:3E:1B"

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print('disconnected from server')

def init():
    global ecg_flag, eeg_flag, eda_flag, emg_flag, focuscalm_flag, bitalino_flag

    signaltypes = input("Select the signals types to be used and enter them separated by commas. (ecg,eeg,eda,emg)")
    signaltypes = signaltypes.split(',')
    sensortypes = input("Select the sensors to be used and enter them separated by commas. (focuscalm, bitalino)")
    sensortypes = sensortypes.split(',')

    if 'ecg' in signaltypes:
        ecg_flag = True
    if 'eeg' in signaltypes:
        eeg_flag = True
    if 'eda' in signaltypes:
        eda_flag = True
    if 'emg' in signaltypes:
        emg_flag = True
    
    if 'focuscalm' in sensortypes:
        focuscalm_flag = True
    if 'bitalino' in sensortypes:
        bitalino_flag = True

    sio.connect('http://' + str(hostip) + ':'+ str(hostaddr))

if __name__ == '__main__':
    
    init()

    if focuscalm_flag == True:
        t1 = threading.Thread(target=eeg.tcpip_eeg_init)
        t1.start()
    if bitalino_flag == True:
        bitalino.bitalino_init(mac_address)
        t2 = threading.Thread(target = bitalino.bitalino_handler, args = (sio,'p2'))
        t2.start()