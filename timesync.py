import time
import os

def timesync():
    try:
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        print(response)
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
    except:
        print('Could not sync with time server.')

    print('Time synchronization done.')
