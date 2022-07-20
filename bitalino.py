from pylsl import StreamInlet, resolve_stream, lost_error
import datetime
import os
import time

import timesync

bitalino_fname = ''
eeg =[]
ecg=[]
emg=[]
eda=[]

# Please update the channel number and sensor types (according to channel order)
channeln = 1

def bitalino_handler(sio, person, mac_address, eeg_flag, ecg_flag, eda_flag, emg_flag):
    global eeg, ecg, emg, eda, bitalino_fname

    channeloptions = ['eeg', 'ecg', 'eda', 'emg']
    channels = []
    i = 0

    for flag in [eeg_flag, ecg_flag, eda_flag, emg_flag]:
        if flag == True:
            channels.append(channeloptions[i])
        i += 1

    print("# Looking for an available OpenSignals stream from the specified device...")
    os_stream = resolve_stream("type", mac_address)

    # Create an inlet to receive signal samples from the stream
    inlet = StreamInlet(os_stream[0], recover = False)

    ## log file name
    now = datetime.datetime.now()
    myroot = 'data'
    os.makedirs(myroot, exist_ok=True)
    snow = now.strftime('bitalino-%y%m%d-%H%M')
    bitalino_fname = "%s/%s.csv" % (myroot, snow)

    # write sensor types as titles of each column
    channeltitlelist = ''
    channeltitlelist += 'timestamp,'
    for s in channels:
        channeltitle = "%s"%s
        if s != channels[-1]:
            channeltitlelist += channeltitle + ','
        else:
            channeltitlelist += channeltitle + '\n'
    with open(bitalino_fname, "a") as f:
        f.write(channeltitlelist)

    corrected = [0, 0, 0, 0]
    a = 0.8

    while True:
        channeldata = [None for i in channels]

        try:
            # Receive samples
            samples, timestamp = inlet.pull_sample()

            channeldatastrlist = ''
            timestamp = time.time()
            ntp_client = timesync.MyNTPClient('ntp.nict.jp')
            timestamp = ntp_client.get_nowtime()
            channeldata_send = {'person':person,'timestamp':timestamp}
            channeldatastrlist += '%s'%datetime.datetime.fromtimestamp(timestamp) + ','
            for s in channels:
                idx = channels.index(s)
                corrected[idx] = a * corrected[idx] + (1-a) * samples[idx+1]
                channeldata[idx] = corrected[idx]
                #channeldata[idx] = samples[idx+1]

                channeldatastr = '%s'%str(channeldata[idx])
                channeldata_send.update([(s,channeldata[idx])])
                if s != channels[-1]:
                    channeldatastrlist += channeldatastr + ','
                else:
                    channeldatastrlist += channeldatastr + '\n'
                
                if s == 'eeg':
                    eeg.append(channeldata[idx])
                elif s == 'ecg':
                    ecg.append(channeldata[idx])
                elif s == 'emg':
                    emg.append(channeldata[idx])
                elif s == 'eda':
                    eda.append(channeldata[idx])

            # write down data on log file
            with open(bitalino_fname, "a") as f:
                f.write(channeldatastrlist)

            #print(channeldata_send)

            if len(eeg) > 1000:
                eeg = eeg[-1000:]
            if len(ecg) > 1000:
                ecg = ecg[-1000:]
            if len(emg) > 1000:
                emg = emg[-1000:]
            if len(eda) > 1000:
                eda = eda[-1000:]
            
            sio.emit('my message', channeldata_send)
        except lost_error as e:
            os._exit(0)