import sys
import ntplib
import time

class MyNTPClient(object):
    def __init__(self, ntp_server_host):
        self.ntp_client = ntplib.NTPClient()
        self.ntp_server_host = ntp_server_host

    def get_nowtime(self):
        try:
            res = self.ntp_client.request(self.ntp_server_host)
            #nowtime = datetime.datetime.strptime(ctime(res.tx_time), "%a %b %d %H:%M:%S %Y")
            #return nowtime.strftime(timeformat)
            return res.tx_time
        except Exception as e:
            return time.time()

def main():
    ntp_client = MyNTPClient('ntp.nict.jp')
    print(ntp_client.get_nowtime())

if __name__ == "__main__":
    main()