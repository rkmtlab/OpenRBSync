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
channels = ['ecg','eda']

def bitalino_init(mac_address):
    '''
    mac_address - mac address of your bitalino device
    before using this function, please enable live streaming in OpenSignals setting
    '''
    global inlet, bitalino_fname, eeg, ecg, emg, eda
    # Resolve stream
    print("# Looking for an available OpenSignals stream from the specified device...")
    os_stream = resolve_stream("type", mac_address)

    # Create an inlet to receive signal samples from the stream
    inlet = StreamInlet(os_stream[0], recover = False)

    # Get information about the stream
    stream_info = inlet.info()

    # Get individual attributes
    stream_n_channels = stream_info.channel_count()

    # Store sensor channel info & units in dictionary
    stream_channels = dict()
    channels = stream_info.desc().child("channels").child("channel")

    # Loop through all available channels
    for i in range(stream_n_channels):
        # Get the channel number (e.g. 1)
        channel = i + 1

        # Get the channel type (e.g. ECG)
        sensor = channels.child_value("sensor")

        # Get the channel unit (e.g. mV)
        unit = channels.child_value("unit")

        # Store the information in the stream_channels dictionary
        stream_channels.update({channel: [sensor, unit]})
        channels = channels.next_sibling()

    #print(stream_n_channels,stream_channels, channels)

    ## log file name
    now = datetime.datetime.now()
    myroot = 'data'
    os.makedirs(myroot, exist_ok=True)
    snow = now.strftime('bitalino-%y%m%d-%H%M')
    bitalino_fname = "%s/%s.csv" % (myroot, snow)

def bitalino_handler(sio, person):
    global bitalino_fname, eeg, ecg, emg, eda, channels

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
                channeldata[idx] = samples[idx+1]
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

            print(channeldata_send)

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