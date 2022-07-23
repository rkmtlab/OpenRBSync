import eventlet
import socketio
import datetime
import threading
import sys
from PyQt5 import QtWidgets, QtCore
from engineio.payload import Payload
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import os

# own module
import plot_analysis_functions as paf

port = 3030

p1_fname = ''
p2_fname = ''

# create plot area
app_qt = QtWidgets.QApplication(sys.argv)
plot_graph = paf.PlotGraph()
timer = QtCore.QTimer()

# create socket server
sio = socketio.Server(ping_interval=5, ping_timeout=1000)
app_soc = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

def receive_forever():
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app_soc)

# serve in another thread
t_server = threading.Thread(target=receive_forever)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(411, 323)
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
        self.buttonBox.setGeometry(QtCore.QRect(120, 260, 164, 32))
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
        self.lineedit_p1 = QtWidgets.QLineEdit(Form)
        self.lineedit_p1.setEnabled(True)
        self.lineedit_p1.setGeometry(QtCore.QRect(250, 170, 51, 21))
        self.lineedit_p1.setFrame(True)
        self.lineedit_p1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineedit_p1.setObjectName("lineedit_p1")
        self.lineedit_p1.setVisible(False)
        self.txt_timedelay = QtWidgets.QLabel(Form)
        self.txt_timedelay.setGeometry(QtCore.QRect(210, 150, 81, 16))
        self.txt_timedelay.setObjectName("txt_timedelay")
        self.txt_timedelay.setVisible(False)
        self.lineedit_p2 = QtWidgets.QLineEdit(Form)
        self.lineedit_p2.setEnabled(True)
        self.lineedit_p2.setGeometry(QtCore.QRect(340, 170, 51, 21))
        self.lineedit_p2.setFrame(True)
        self.lineedit_p2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineedit_p2.setObjectName("lineedit_p2")
        self.lineedit_p2.setVisible(False)
        self.txt_p1 = QtWidgets.QLabel(Form)
        self.txt_p1.setGeometry(QtCore.QRect(230, 170, 21, 16))
        self.txt_p1.setObjectName("txt_p1")
        self.txt_p1.setVisible(False)
        self.txt_p2 = QtWidgets.QLabel(Form)
        self.txt_p2.setGeometry(QtCore.QRect(320, 170, 21, 16))
        self.txt_p2.setObjectName("txt_p2")
        self.txt_p2.setVisible(False)
        self.txt_embeddingdimension = QtWidgets.QLabel(Form)
        self.txt_embeddingdimension.setGeometry(QtCore.QRect(210, 200, 141, 16))
        self.txt_embeddingdimension.setObjectName("txt_embeddingdimension")
        self.txt_embeddingdimension.setVisible(False)
        self.lineedit_embeddingdimension = QtWidgets.QLineEdit(Form)
        self.lineedit_embeddingdimension.setGeometry(QtCore.QRect(210, 220, 181, 21))
        self.lineedit_embeddingdimension.setFrame(True)
        self.lineedit_embeddingdimension.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineedit_embeddingdimension.setObjectName("lineedit_embeddingdimension")
        self.lineedit_embeddingdimension.setVisible(False)

        self.retranslateUi(Form)
        self.radioButton_bar.toggled['bool'].connect(self.comboBox_analysis.setEnabled)
        self.buttonBox.accepted.connect(Form.close)
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
        self.comboBox_analysis.currentIndexChanged['QString'].connect(Form.setAnalysis)
        self.comboBox_analysis.currentIndexChanged['QString'].connect(Form.showORhide)   
        self.comboBox_analysis.currentIndexChanged['QString'].connect(self.comboBox_analysis.show)
        self.lineedit_p1.textEdited['QString'].connect(Form.setP1delay)
        self.lineedit_p2.textEdited['QString'].connect(Form.setP2delay)
        self.lineedit_embeddingdimension.textEdited['QString'].connect(Form.setEmbeddingDimension)
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
        self.comboBox_analysis.setItemText(1, _translate("Form", "Cross Recurrence Quantification Analysis"))
        self.txt_port.setText(_translate("Form", "Port"))
        self.port_no.setText(_translate("Form", "3030"))
        self.lineedit_p1.setText(_translate("Form", "1"))
        self.txt_timedelay.setText(_translate("Form", "Time delay"))
        self.lineedit_p2.setText(_translate("Form", "1"))
        self.txt_p1.setText(_translate("Form", "p1"))
        self.txt_p2.setText(_translate("Form", "p2"))
        self.txt_embeddingdimension.setText(_translate("Form", "Embedding dimension"))
        self.lineedit_embeddingdimension.setText(_translate("Form", "1"))


# functions to implement when actions are taken in the dialog
class gui(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.app_qt = None
        self.plot_graph = None
        self.t_server = None
        self.eeg_flag = False
        self.ecg_flag = False
        self.eda_flag = False
        self.emg_flag = False
        self.vis_type = None
        self.analysis_type = 'Cross Correlation'
        self.timedelay_p1 = 1
        self.timedelay_p2 = 1
        self.embedding_dimension = 1

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
    
    def setVis_off(self):
        self.vis_type = 'off'

    def setVis_raw(self):
        self.vis_type = 'raw'

    def setVis_bar(self):
        self.vis_type = 'bar'

    def setPortNo(self):
        global port
        port = int(str(self.ui.port_no.text()))

    def setAnalysis(self):
        self.analysis_type = str(self.ui.comboBox_analysis.currentText())
    
    def showORhide(self):
        if str(self.ui.comboBox_analysis.currentText()) == 'Cross Recurrence Quantification Analysis':
            self.ui.txt_p1.setVisible(True)
            self.ui.txt_p2.setVisible(True)
            self.ui.lineedit_p1.setVisible(True)
            self.ui.lineedit_p2.setVisible(True)
            self.ui.txt_embeddingdimension.setVisible(True)
            self.ui.txt_timedelay.setVisible(True)
            self.ui.lineedit_embeddingdimension.setVisible(True)
        else:
            self.ui.txt_p1.setVisible(False)
            self.ui.txt_p2.setVisible(False)
            self.ui.lineedit_p1.setVisible(False)
            self.ui.lineedit_p2.setVisible(False)
            self.ui.txt_embeddingdimension.setVisible(False)
            self.ui.txt_timedelay.setVisible(False)
            self.ui.lineedit_embeddingdimension.setVisible(False)

    def setP1delay(self):
        self.timedelay_p1 = int(str(self.ui.lineedit_p1.text()))
    
    def setP2delay(self):
        global timedelay_p2
        timedelay_p2 = int(str(self.ui.lineedit_p2.text()))

    def setEmbeddingDimension(self):
        global embedding_dimension
        embedding_dimension = int(str(self.ui.lineedit_embeddingdimension.text()))

    def init(self):
        global plot_graph, timer, t_server
        plot_graph.set_parameters(self.eeg_flag, self.ecg_flag, self.eda_flag, self.emg_flag, self.timedelay_p1, self.timedelay_p2, self.embedding_dimension)
        if self.vis_type == 'off':
            pass
        elif self.vis_type == 'raw':
            plot_graph.raw_init()
        elif self.vis_type == 'bar':
            plot_graph.bar_init(self.analysis_type)
        t_server.start()

        if self.vis_type == 'raw':
            timer.timeout.connect(plot_graph.update_raw_graph)
            timer.start(50)
        elif self.vis_type == 'bar':
            timer.timeout.connect(plot_graph.update_bar_graph)
            timer.start(1000)

# called when a client is connected
@sio.event
def connect(sid, environ):
    global plot_graph, p1_fname, p2_fname
    print('connect ', sid)

    ## log file name
    now = datetime.datetime.now()
    myroot = 'data-server'
    os.makedirs(myroot, exist_ok=True)
    snow1 = now.strftime('p1-%y%m%d-%H%M')
    snow2 = now.strftime('p2-%y%m%d-%H%M')
    p1_fname = "%s/%s.csv" % (myroot, snow1)
    p2_fname = "%s/%s.csv" % (myroot, snow2)

    index = 'timestamp, person'
    for channel in plot_graph.channellist:
        index += ',' + channel
    index += '\n'

    with open(p1_fname, "a") as f1:
            f1.write(index)
    with open(p2_fname, "a") as f2:
            f2.write(index)

# called when socketio receives data
@sio.on('my message')
def my_message(sid, data):
    global plot_graph, p1_fname, p2_fname
    idxp = 0
    idxs = 0

    timestamp_ux = data['timestamp']
    timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ux)
    write_data = str(timestamp_dt)
    if data['person'] == 'p1':
        idxp = 0
    if data['person'] == 'p2':
        idxp = 1
    for key in data:
        if key == 'eeg' or key == 'ecg' or key == 'eda' or key == 'emg':
            idxs = plot_graph.channellist.index(key)
            plot_graph.signals[idxs][idxp].append(data[key])
            plot_graph.timelist[idxs][idxp].append(timestamp_ux)

            if len(plot_graph.signals[idxs][idxp]) > 500:
                plot_graph.signals[idxs][idxp] = plot_graph.signals[idxs][idxp][-500:]
            if len(plot_graph.timelist[idxs][idxp]) > 500:
                plot_graph.timelist[idxs][idxp] = plot_graph.timelist[idxs][idxp][-500:]
        if key != 'timestamp':
            write_data += ',' + str(data[key])
    write_data += '\n'
    if idxp == 0:
        with open(p1_fname, "a") as f1:
            f1.write(write_data)
    elif idxp == 1:
        with open(p2_fname, "a") as f2:
            f2.write(write_data)

# called when a client is disconnected
@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    # create setting dialog
    app_pg = pg.mkQApp("Plotting Example")
    window = gui()
    window.show()

    # define maximum packets in payload
    Payload.max_decode_packets = 50
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()