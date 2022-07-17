import eventlet
import socketio
import datetime
import threading
import sys
from PyQt5 import QtWidgets, QtCore
from engineio.payload import Payload

# own module
import analysis_functions as af

# define maximum packets in payload
Payload.max_decode_packets = 50

eeg_flag = False
ecg_flag = False
eda_flag = False
emg_flag = False
vis_type = None
analysis_type = 'Cross Correlation'
port = 3030

# create plot area
app_qt = QtWidgets.QApplication(sys.argv)
plot_graph = af.PlotGraph()
timer = QtCore.QTimer()


def receive_forever():
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)

# serve in another thread
t_server = threading.Thread(target=receive_forever)

# dialog class
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(411, 260)
        self.checkBox_eeg = QtWidgets.QCheckBox(Form)
        self.checkBox_eeg.setGeometry(QtCore.QRect(30, 50, 86, 20))
        self.checkBox_eeg.setObjectName("checkBox_eeg")
        self.txt_signaltype = QtWidgets.QLabel(Form)
        self.txt_signaltype.setGeometry(QtCore.QRect(30, 30, 81, 16))
        self.txt_signaltype.setObjectName("txt_signaltype")
        self.checkBox_ecg = QtWidgets.QCheckBox(Form)
        self.checkBox_ecg.setGeometry(QtCore.QRect(30, 70, 86, 20))
        self.checkBox_ecg.setObjectName("checkBox_ecg")
        self.checkBox_eda = QtWidgets.QCheckBox(Form)
        self.checkBox_eda.setGeometry(QtCore.QRect(30, 90, 86, 20))
        self.checkBox_eda.setObjectName("checkBox_eda")
        self.checkBox_emg = QtWidgets.QCheckBox(Form)
        self.checkBox_emg.setGeometry(QtCore.QRect(30, 110, 86, 20))
        self.checkBox_emg.setObjectName("checkBox_emg")
        self.txt_visualization = QtWidgets.QLabel(Form)
        self.txt_visualization.setGeometry(QtCore.QRect(200, 30, 81, 16))
        self.txt_visualization.setObjectName("txt_visualization")
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(120, 200, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.radioButton_off = QtWidgets.QRadioButton(Form)
        self.radioButton_off.setGeometry(QtCore.QRect(200, 50, 99, 20))
        self.radioButton_off.setObjectName("radioButton_off")
        self.radioButton_raw = QtWidgets.QRadioButton(Form)
        self.radioButton_raw.setGeometry(QtCore.QRect(200, 70, 99, 20))
        self.radioButton_raw.setObjectName("radioButton_raw")
        self.radioButton_bar = QtWidgets.QRadioButton(Form)
        self.radioButton_bar.setGeometry(QtCore.QRect(200, 90, 161, 20))
        self.radioButton_bar.setObjectName("radioButton_bar")
        self.comboBox_analysis = QtWidgets.QComboBox(Form)
        self.comboBox_analysis.setEnabled(False)
        self.comboBox_analysis.setGeometry(QtCore.QRect(200, 110, 191, 32))
        self.comboBox_analysis.setAutoFillBackground(False)
        self.comboBox_analysis.setObjectName("comboBox_analysis")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.txt_port = QtWidgets.QLabel(Form)
        self.txt_port.setGeometry(QtCore.QRect(30, 150, 81, 16))
        self.txt_port.setObjectName("txt_port")
        self.port_no = QtWidgets.QLineEdit(Form)
        self.port_no.setGeometry(QtCore.QRect(30, 170, 113, 21))
        self.port_no.setFrame(True)
        self.port_no.setObjectName("port_no")

        self.retranslateUi(Form)
        self.radioButton_bar.toggled['bool'].connect(self.comboBox_analysis.setEnabled)
        self.buttonBox.rejected.connect(Form.close)
        self.checkBox_ecg.clicked['bool'].connect(Form.setECGflag)
        self.checkBox_eeg.clicked['bool'].connect(Form.setEEGflag)
        self.checkBox_eda.clicked['bool'].connect(Form.setEDAflag)
        self.checkBox_emg.clicked['bool'].connect(Form.setEMGflag)
        self.radioButton_off.toggled['bool'].connect(Form.setVis_off)
        self.radioButton_raw.toggled['bool'].connect(Form.setVis_raw)
        self.radioButton_bar.toggled['bool'].connect(Form.setVis_bar)
        self.port_no.textEdited['QString'].connect(Form.setPortNo)
        self.buttonBox.accepted.connect(Form.init)
        self.buttonBox.accepted.connect(Form.close)
        self.comboBox_analysis.currentIndexChanged['QString'].connect(Form.setAnalysis)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox_eeg.setText(_translate("Form", "EEG"))
        self.txt_signaltype.setText(_translate("Form", "Signal type"))
        self.checkBox_ecg.setText(_translate("Form", "ECG"))
        self.checkBox_eda.setText(_translate("Form", "EDA"))
        self.checkBox_emg.setText(_translate("Form", "EMG"))
        self.txt_visualization.setText(_translate("Form", "Visualization"))
        self.radioButton_off.setText(_translate("Form", "Off"))
        self.radioButton_raw.setText(_translate("Form", "Raw signal"))
        self.radioButton_bar.setText(_translate("Form", "Bar plot of synchrony"))
        self.comboBox_analysis.setItemText(0, _translate("Form", "Cross correlation"))
        self.comboBox_analysis.setItemText(1, _translate("Form", "Wavelet Transform Coherence"))
        self.txt_port.setText(_translate("Form", "Port"))
        self.port_no.setText(_translate("Form", "3030"))

# functions to implement when actions are taken in the dialog
class gui(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.app_qt = None
        self.plot_graph = None
        self.t_server = None

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
    
    def setVis_off(self):
        global vis_type
        vis_type = 'off'

    def setVis_raw(self):
        global vis_type
        vis_type = 'raw'

    def setVis_bar(self):
        global vis_type
        vis_type = 'bar'

    def setPortNo(self):
        global port
        port = int(str(self.ui.port_no.text()))

    def setAnalysis(self):
        global analysis_type
        analysis_type = str(self.ui.comboBox_analysis.currentText())
    
    def init(self):
        global vis_type, app_qt, plot_graph, timer, t_server, analysis_type
        global eeg_flag, ecg_flag, eda_flag, emg_flag
        plot_graph.set_parameters(eeg_flag, ecg_flag, eda_flag, emg_flag)
        if vis_type == 'off':
            pass
        elif vis_type == 'raw':
            plot_graph.raw_init()
        elif vis_type == 'bar':
            plot_graph.bar_init(analysis_type)
        t_server.start()

        if vis_type == 'raw':
            timer.timeout.connect(plot_graph.update_raw_graph)
            timer.start(50)
        elif vis_type == 'bar':
            timer.timeout.connect(plot_graph.update_bar_graph)
            timer.start(1000)

# create setting dialog
app_dialog = QtWidgets.QApplication(sys.argv)
window = gui()
window.show()

# create socket server
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

# called when a client is connected
@sio.event
def connect(sid, environ):
    print('connect ', sid)

# called when socketio receives data
@sio.on('my message')
def my_message(sid, data):
    global plot_graph
    idxp = 0
    idxs = 0

    timestamp_ux = data['timestamp']
    timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ux)
    if data['person'] == 'p1':
        idxp = 0
    if data['person'] == 'p2':
        idxp = 1
    for key in data:
        if key != 'timestamp' and key != 'person':
            if key == 'eeg':
                idxs = 0
            if key == 'ecg':
                idxs = 1
            if key == 'eda':
                idxs = 2
            if key == 'emg':
                idxs = 3
            plot_graph.signals[idxs][idxp].append(data[key])
            plot_graph.timelist[idxs][idxp].append(timestamp_ux)

            if len(plot_graph.signals[idxs][idxp]) > 1000:
                plot_graph.signals[idxs][idxp] = plot_graph.signals[idxs][idxp][-1000:]
                plot_graph.timelist[idxs][idxp] = plot_graph.timelist[idxs][idxp][-1000:]

# called when a client is disconnected
@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    app_dialog.exec()
    if vis_type != 'off':
        app_qt.exec()