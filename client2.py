import socketio
import threading
from PyQt5 import QtCore, QtWidgets
import sys

import bitalino
import timesync

sio = socketio.Client()
hostlink = ''

# signal flags
ecg_flag = False
eeg_flag = False
eda_flag = False
emg_flag = False
vis_type = ''
analysis_type = ''

# Define the MAC-address of the acquisition device used in OpenSignals
mac_address = ''

def socket_connect():
    global sio, hostlink
    sio.connect(hostlink)

t1 = threading.Thread(target = socket_connect)

app = QtWidgets.QApplication(sys.argv)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 405)
        self.sensortype = QtWidgets.QLabel(Form)
        self.sensortype.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.sensortype.setObjectName("sensortype")
        self.signaltype = QtWidgets.QLabel(Form)
        self.signaltype.setGeometry(QtCore.QRect(30, 160, 81, 16))
        self.signaltype.setObjectName("signaltype")
        self.checkBox_eeg = QtWidgets.QCheckBox(Form)
        self.checkBox_eeg.setGeometry(QtCore.QRect(30, 180, 86, 20))
        self.checkBox_eeg.setObjectName("checkBox_eeg")
        self.checkBox_ecg = QtWidgets.QCheckBox(Form)
        self.checkBox_ecg.setGeometry(QtCore.QRect(30, 200, 86, 20))
        self.checkBox_ecg.setObjectName("checkBox_ecg")
        self.checkBox_eda = QtWidgets.QCheckBox(Form)
        self.checkBox_eda.setGeometry(QtCore.QRect(30, 220, 86, 20))
        self.checkBox_eda.setObjectName("checkBox_eda")
        self.checkBox_emg = QtWidgets.QCheckBox(Form)
        self.checkBox_emg.setGeometry(QtCore.QRect(30, 240, 86, 20))
        self.checkBox_emg.setObjectName("checkBox_emg")
        self.MACaddress = QtWidgets.QLabel(Form)
        self.MACaddress.setEnabled(True)
        self.MACaddress.setGeometry(QtCore.QRect(30, 100, 151, 16))
        self.MACaddress.setObjectName("MACaddress")
        self.lineEdit_MACaddress = QtWidgets.QLineEdit(Form)
        self.lineEdit_MACaddress.setEnabled(True)
        self.lineEdit_MACaddress.setGeometry(QtCore.QRect(30, 120, 181, 21))
        self.lineEdit_MACaddress.setText("")
        self.lineEdit_MACaddress.setObjectName("lineEdit_MACaddress")
        self.BITalino = QtWidgets.QLabel(Form)
        self.BITalino.setGeometry(QtCore.QRect(30, 40, 101, 30))
        self.BITalino.setObjectName("BITalino")
        self.HostLink = QtWidgets.QLabel(Form)
        self.HostLink.setGeometry(QtCore.QRect(30, 280, 81, 16))
        self.HostLink.setObjectName("HostLink")
        self.lineEdit_link = QtWidgets.QLineEdit(Form)
        self.lineEdit_link.setGeometry(QtCore.QRect(30, 300, 181, 21))
        self.lineEdit_link.setText("")
        self.lineEdit_link.setObjectName("lineEdit_ip")
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(110, 350, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Form)
        self.lineEdit_MACaddress.textEdited['QString'].connect(Form.setMACaddress)
        self.checkBox_eeg.clicked['bool'].connect(Form.setEEGflag)
        self.checkBox_ecg.clicked['bool'].connect(Form.setECGflag)
        self.checkBox_eda.clicked['bool'].connect(Form.setEDAflag)
        self.checkBox_emg.clicked['bool'].connect(Form.setEMGflag)
        self.lineEdit_link.textEdited['QString'].connect(Form.setHostLink)
        self.buttonBox.accepted.connect(Form.close)
        self.buttonBox.accepted.connect(Form.init)
        self.buttonBox.rejected.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sensortype.setText(_translate("Form", "Sensor type"))
        self.signaltype.setText(_translate("Form", "Signal type"))
        self.checkBox_eeg.setText(_translate("Form", "EEG"))
        self.checkBox_ecg.setText(_translate("Form", "ECG"))
        self.checkBox_eda.setText(_translate("Form", "EDA"))
        self.checkBox_emg.setText(_translate("Form", "EMG"))
        self.MACaddress.setText(_translate("Form", "MAC address of BITalino"))
        self.BITalino.setText(_translate("Form", "BITalino"))
        self.HostLink.setText(_translate("Form", "Host Link"))

class gui(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)     

    def setMACaddress(self):
        global mac_address
        mac_address = str(self.ui.lineEdit_MACaddress.text())

    def setEEGflag(self):
        global eeg_flag
        if eeg_flag == False:
            eeg_flag = True
        else:
            eeg_flag = False

    def setECGflag(self):
        global ecg_flag
        if ecg_flag == False:
            ecg_flag = True
        else:
            ecg_flag = False

    def setEDAflag(self):
        global eda_flag
        if eda_flag == False:
            eda_flag = True
        else:
            eda_flag = False

    def setEMGflag(self):
        global emg_flag
        if emg_flag == False:
            emg_flag = True
        else:
            emg_flag = False

    def setHostLink(self):
        global hostlink
        hostlink = str(self.ui.lineEdit_link.text())

    def init(self):
        global sio, t1, mac_address
        timesync.timesync()
        
        t1.start()

        t2= threading.Thread(target = bitalino.bitalino_handler, args = (sio,'p2', mac_address, eeg_flag, ecg_flag, eda_flag, emg_flag))
        t2.start()

window = gui()
window.show()

@sio.event
def connect():
    print('connection established')

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == '__main__':
    app.exec()