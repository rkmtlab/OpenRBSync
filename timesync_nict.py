import ntplib
import time

ntp_server_host = 'ntp.nict.jp'

class MyNTPClient(object):
    def __init__(self, ntp_server_host):
        self.ntp_client = ntplib.NTPClient()
        self.ntp_server_host = ntp_server_host

    def get_nowtime(self):
        try:
            res = self.ntp_client.request(self.ntp_server_host)
            return res.tx_time
        except Exception as e:
            print('The NTP server does not respond. time.time() is used instead.')
            return time.time()

def main():
    global ntp_server_host
    ntp_client = MyNTPClient(ntp_server_host)
    print(ntp_client.get_nowtime())

if __name__ == "__main__":
    main()