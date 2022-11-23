import datetime
import os
import serial
import sys

def arduino_handler (sio, person, eeg_flag, ecg_flag, eda_flag, emg_flag, portname, portno):
    arduino_fname = ''
    eeg =[]
    ecg=[]
    emg=[]
    eda=[]
    channeloptions = ['eeg', 'ecg', 'eda', 'emg']
    channels = []
    i = 0

    for flag in [eeg_flag, ecg_flag, eda_flag, emg_flag]:
        if flag == True:
            channels.append(channeloptions[i])
        i += 1

    ser_arduino = serial.Serial(portname, portno)

    ## log file name
    now = datetime.datetime.now()
    myroot = 'data'
    os.makedirs(myroot, exist_ok=True)
    snow = now.strftime('arduino-%y%m%d-%H%M')
    arduino_fname = "%s/%s.csv" % (myroot, snow)

    # write sensor types as titles of each column
    channeltitlelist = ''
    channeltitlelist += 'timestamp,'
    for s in channels:
        channeltitle = "%s"%s
        if s != channels[-1]:
            channeltitlelist += channeltitle + ','
        else:
            channeltitlelist += channeltitle + '\n'
    with open(arduino_fname, "a") as f:
        f.write(channeltitlelist)
    
    # a parameter of weighted moving average to smoothen signals
    weighted_avg_param = 0.8

    # a list of signals smoothened by a filter
    corrected = [0, 0, 0, 0]
    timestamp_dt = datetime.datetime.now()

    signal = [None for i in range(len(channels))]

    while True:
        for i in range(len(channels)):
            try:
                # read biosignal from the arduino serial
                signal_byte = ser_arduino.readline()
                signal_str = signal_byte.decode('utf-8')
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                signal_str = 'None'
            
            channeldata = [None for i in channels]

            channeldatastrlist = ''
            #timestamp = datetime.datetime.now().timestamp()
            #time.sleep(0.01)
            #print(timestamp_dt)
            timestamp_dt = datetime.datetime.now()
            timestamp = datetime.datetime.timestamp(timestamp_dt)
            channeldata_send = {'person':person,'timestamp':timestamp}
            channeldatastrlist += '%s'%datetime.datetime.fromtimestamp(timestamp) + ','

            # E - EEG, C - ECG, D - EDA, M - EMG
            if (signal_str[0] == 'E' or signal_str[0] == 'C' or signal_str[0] == 'D' or signal_str[0] == 'M'):
                if signal_str[0] == 'E':
                    idx = channels.index('eeg')
                    signal_float = float(signal_str.replace('E',''))
                elif signal_str[0] == 'C':
                    idx = channels.index('ecg')
                    signal_float = float(signal_str.replace('C',''))
                elif signal_str[0] == 'D':
                    idx = channels.index('eda')
                    signal_float = float(signal_str.replace('D',''))
                else:
                    idx = channels.index('emg')
                    signal_float = float(signal_str.replace('M',''))
                signal[idx] = signal_float

        for s in channels:
            idx = channels.index(s)
            channeldatastr = '%s'%str(signal[idx])
            channeldata_send.update([(s,signal[idx])])
            if s != channels[-1]:
                channeldatastrlist += channeldatastr + ','
            else:
                channeldatastrlist += channeldatastr + '\n'
            
            if s == 'eeg':
                eeg.append(signal[idx])
            elif s == 'ecg':
                ecg.append(signal[idx])
            elif s == 'emg':
                emg.append(signal[idx])
            elif s == 'eda':
                eda.append(signal[idx])

        # write down data on log file
        with open(arduino_fname, "a") as f:
            f.write(channeldatastrlist)

        if len(eeg) > 100:
            eeg = eeg[-100:]
        if len(ecg) > 100:
            ecg = ecg[-100:]
        if len(emg) > 100:
            emg = emg[-100:]
        if len(eda) > 100:
            eda = eda[-100:]
        
        try:
            sio.emit('my message', channeldata_send)
        except Exception:
            print('Cannot communicate with the server')
            os._exit(0)