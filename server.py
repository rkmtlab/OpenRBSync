import eventlet
from matplotlib.pyplot import plot
import socketio
import datetime
import pyqtgraph as pg
import threading
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from engineio.payload import Payload
import scipy
import pandas as pd
from statistics import mean
import numpy as np
import scipy.signal as sig

# own module
import analysis_functions as af

# define maximum packets in payload
Payload.max_decode_packets = 50

app_qt = QtWidgets.QApplication(sys.argv)
plot_graph = af.PlotGraph()
plot_graph.bar_init()

# af.updates(plot_graph.update_raw_graph, 50)
# af.updates(plot_graph.update_bar_graph, 1000)

timer = QtCore.QTimer()
timer.timeout.connect(plot_graph.update_bar_graph)
timer.start(1000)

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


def receive_forever():
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3030)), app)


if __name__ == '__main__':
    # serve in another thread
    t_server = threading.Thread(target=receive_forever)
    t_server.start()

    app_qt.exec()