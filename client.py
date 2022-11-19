import socketio
import threading
from PyQt5 import QtCore, QtWidgets
import sys
import os

import bitalino
import arduino

sio = socketio.Client()
hostlink = ''

def socket_connect():
    global sio, hostlink
    hostlink = 'http://localhost:3030'
    sio.connect(hostlink)

t1 = threading.Thread(target = socket_connect)

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
        self.MACaddress.setVisible(False)
        self.lineEdit_MACaddress = QtWidgets.QLineEdit(Form)
        self.lineEdit_MACaddress.setEnabled(True)
        self.lineEdit_MACaddress.setGeometry(QtCore.QRect(30, 120, 181, 21))
        self.lineEdit_MACaddress.setText("")
        self.lineEdit_MACaddress.setObjectName("lineEdit_MACaddress")
        self.lineEdit_MACaddress.setVisible(False)
        self.portname = QtWidgets.QLabel(Form)
        self.portname.setEnabled(True)
        self.portname.setGeometry(QtCore.QRect(30, 100, 151, 16))
        self.portname.setObjectName("portname")
        self.portname.setVisible(False)
        self.lineEdit_portname = QtWidgets.QLineEdit(Form)
        self.lineEdit_portname.setEnabled(True)
        self.lineEdit_portname.setGeometry(QtCore.QRect(30, 120, 181, 21))
        self.lineEdit_portname.setText("")
        self.lineEdit_portname.setObjectName("lineEdit_portname")
        self.lineEdit_portname.setVisible(False)
        self.freq = QtWidgets.QLabel(Form)
        self.freq.setEnabled(True)
        self.freq.setGeometry(QtCore.QRect(250, 100, 151, 16))
        self.freq.setObjectName("frequency")
        self.freq.setVisible(False)
        self.lineEdit_freq = QtWidgets.QLineEdit(Form)
        self.lineEdit_freq.setEnabled(True)
        self.lineEdit_freq.setGeometry(QtCore.QRect(250, 120, 100, 21))
        self.lineEdit_freq.setText("")
        self.lineEdit_freq.setFrame(True)
        self.lineEdit_freq.setObjectName("lineEdit_frequency")
        self.lineEdit_freq.setVisible(False)
        self.portno = QtWidgets.QLabel(Form)
        self.portno.setEnabled(True)
        self.portno.setGeometry(QtCore.QRect(250, 100, 151, 16))
        self.portno.setObjectName("portno")
        self.portno.setVisible(False)
        self.lineEdit_portno = QtWidgets.QLineEdit(Form)
        self.lineEdit_portno.setEnabled(True)
        self.lineEdit_portno.setGeometry(QtCore.QRect(250, 120, 100, 21))
        self.lineEdit_portno.setText("")
        self.lineEdit_portno.setFrame(True)
        self.lineEdit_portno.setObjectName("lineEdit_portno")
        self.lineEdit_portno.setVisible(False)
        self.BITalino = QtWidgets.QRadioButton(Form)
        self.BITalino.setGeometry(QtCore.QRect(30, 40, 101, 30))
        self.BITalino.setObjectName("BITalino")
        self.arduino = QtWidgets.QRadioButton(Form)
        self.arduino.setGeometry(QtCore.QRect(30, 60, 101, 30))
        self.arduino.setObjectName("arduino")
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
        self.lineEdit_freq.textEdited['QString'].connect(Form.setFreq)
        self.checkBox_eeg.clicked['bool'].connect(Form.setEEGflag)
        self.checkBox_ecg.clicked['bool'].connect(Form.setECGflag)
        self.checkBox_eda.clicked['bool'].connect(Form.setEDAflag)
        self.checkBox_emg.clicked['bool'].connect(Form.setEMGflag)
        self.BITalino.clicked['bool'].connect(Form.setBITALINOflag)
        self.arduino.clicked['bool'].connect(Form.setARDUINOflag)
        self.lineEdit_link.textEdited['QString'].connect(Form.setHostLink)
        self.lineEdit_portname.textEdited['QString'].connect(Form.setPortName)
        self.lineEdit_portno.textEdited['QString'].connect(Form.setPortNo)
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
        self.BITalino.setText(_translate("Form", "BITalino"))
        self.arduino.setText(_translate("Form", "Arduino"))
        self.MACaddress.setText(_translate("Form", "MAC address of BITalino"))
        self.portname.setText(_translate("Form", "Port name of the Arduino"))
        self.portno.setText(_translate("Form", "Port Number"))
        self.freq.setText(_translate("Form", "Frequency"))
        self.BITalino.setText(_translate("Form", "BITalino"))
        self.HostLink.setText(_translate("Form", "Host Link"))
        
class gui(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self) 
        self.ecg_flag = False
        self.eeg_flag = False
        self.eda_flag = False
        self.emg_flag = False 
        self.bit_flag = False
        self.ard_flag = False
        self.mac_address = ''   
        self.portname = ''
        self.portno = 0
        self.freq = 100  

    def setMACaddress(self):
        self.mac_address = str(self.ui.lineEdit_MACaddress.text())

    def setFreq(self):
        try:
            self.freq = int(str(self.ui.lineEdit_freq.text()))
        except:
            pass

    def setEEGflag(self):
        if self.eeg_flag == False:
            self.eeg_flag = True
        else:
            self.eeg_flag = False

    def setECGflag(self):
        if self.ecg_flag == False:
            self.ecg_flag = True
        else:
            self.ecg_flag = False

    def setEDAflag(self):
        if self.eda_flag == False:
            self.eda_flag = True
        else:
            self.eda_flag = False

    def setEMGflag(self):
        if self.emg_flag == False:
            self.emg_flag = True
        else:
            self.emg_flag = False

    def setBITALINOflag(self):
        if self.bit_flag == False:
            self.bit_flag = True
            self.ard_flag = False
            self.ui.MACaddress.setVisible(True)
            self.ui.lineEdit_MACaddress.setVisible(True)
            self.ui.freq.setVisible(True)
            self.ui.lineEdit_freq.setVisible(True)
            self.ui.portname.setVisible(False)
            self.ui.lineEdit_portname.setVisible(False)
            self.ui.portno.setVisible(False)
            self.ui.lineEdit_portno.setVisible(False)
    
    def setARDUINOflag(self):
        if self.ard_flag == False:
            self.ard_flag = True
            self.bit_flag = False
            self.ui.portname.setVisible(True)
            self.ui.lineEdit_portname.setVisible(True)
            self.ui.portno.setVisible(True)
            self.ui.lineEdit_portno.setVisible(True)
            self.ui.MACaddress.setVisible(False)
            self.ui.lineEdit_MACaddress.setVisible(False)
            self.ui.freq.setVisible(False)
            self.ui.lineEdit_freq.setVisible(False)

    def setPortName(self):
        try:
            self.portname = str(self.ui.lineEdit_portname.text())
        except:
            pass
    
    def setPortNo(self):
        try:
            self.portno = int(str(self.ui.lineEdit_portno.text()))
        except:
            pass

    def setHostLink(self):
        global hostlink
        hostlink = str(self.ui.lineEdit_link.text())

    def init(self):
        global sio, t1
        
        t1.start()

        if self.bit_flag == True:
            t2= threading.Thread(target = bitalino.bitalino_handler, args = (sio,'p1', self.mac_address, self.eeg_flag, self.ecg_flag, self.eda_flag, self.emg_flag, self.freq))
        elif self.ard_flag == True:
            t2 = threading.Thread(target = arduino.arduino_handler, args = (sio,'p1', self.eeg_flag, self.ecg_flag, self.eda_flag, self.emg_flag, self.portname, self.portno))
        else:
            print("Please select the sensor type")
            os._exit(0)
        t2.start()

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
    app = QtWidgets.QApplication(sys.argv)
    window = gui()
    window.show()
    app.exec()