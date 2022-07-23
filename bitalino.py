from pylsl import StreamInlet, resolve_stream, lost_error
import datetime
import os

import timesync_nict

# ntp server to request timestamp. Please update the link if you are in another timezone.
ntp_server_host = 'ntp.nict.jp'

def bitalino_handler(sio, person, mac_address, eeg_flag, ecg_flag, eda_flag, emg_flag):
    global ntp_server_host
    
    bitalino_fname = ''
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
    
    # a parameter of weighted moving average to smoothen signals
    weighted_avg_param = 0.8

    # a list of signals smoothened by a filter
    corrected = [0, 0, 0, 0]

    while True:
        channeldata = [None for i in channels]

        try:
            # Receive samples
            samples, timestamp = inlet.pull_sample()
        
        except lost_error as e:
            print('Connection from the BITalino device is lost')
            os._exit(0)

        channeldatastrlist = ''
        timestamp = datetime.datetime.now().timestamp()
        ntp_client = timesync_nict.MyNTPClient(ntp_server_host)
        timestamp = ntp_client.get_nowtime()
        channeldata_send = {'person':person,'timestamp':timestamp}
        channeldatastrlist += '%s'%datetime.datetime.fromtimestamp(timestamp) + ','
        for s in channels:
            idx = channels.index(s)
            corrected[idx] = weighted_avg_param * corrected[idx] + (1-weighted_avg_param) * samples[idx+1]
            channeldata[idx] = corrected[idx]

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

        if len(eeg) > 1000:
            eeg = eeg[-1000:]
        if len(ecg) > 1000:
            ecg = ecg[-1000:]
        if len(emg) > 1000:
            emg = emg[-1000:]
        if len(eda) > 1000:
            eda = eda[-1000:]
        
        try:
            sio.emit('my message', channeldata_send)
        except Exception:
            print('Cannot communicate with the server')
            os._exit(0)