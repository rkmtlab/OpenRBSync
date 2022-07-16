import sys
import ntplib

__author__ = "oomori"
__version__ = "1.2.0"

class MyNTPClient(object):
    def __init__(self, ntp_server_host):
        self.ntp_client = ntplib.NTPClient()
        self.ntp_server_host = ntp_server_host

    def get_nowtime(self, timeformat = '%Y/%m/%d %H:%M:%S'):
        try:
            res = self.ntp_client.request(self.ntp_server_host)
            #nowtime = datetime.datetime.strptime(ctime(res.tx_time), "%a %b %d %H:%M:%S %Y")
            #return nowtime.strftime(timeformat)
            return res.tx_time
        except Exception as e:
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            sys.exit(1)

def main():
    ntp_client = MyNTPClient('ntp.nict.jp')
    print(ntp_client.get_nowtime())

if __name__ == "__main__":
    main()