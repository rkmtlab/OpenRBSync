from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from statistics import mean
import scipy.signal as sig
import numpy as np

class PlotGraph(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PlotGraph, self).__init__(*args, **kwargs)
        self.timelist = [[[],[]],[[],[]],[[],[]],[[],[]]]
        self.signals = [[[],[]],[[],[]],[[],[]],[[],[]]]

        self.plot = [None for i in range(4)]
        self.curve = [[None, None] for i in range(4)]
    
    # init func for raw signal plot
    def raw_init(self):
        self.win = pg.GraphicsLayoutWidget(show=True, title="Raw signals")
        self.win.resize(600, 800)
        self.win.setWindowTitle('Plotting')
        self.plot[0] = self.win.addPlot(title="Raw EEG")
        self.curve[0][0] = self.plot[0].plot(pen='b')
        self.curve[0][1] = self.plot[0].plot(pen='r')
        self.win.nextRow()
        self.plot[1] = self.win.addPlot(title="Raw ECG")
        self.curve[1][0] = self.plot[1].plot(pen='b')
        self.curve[1][1] = self.plot[1].plot(pen='r')
        self.win.nextRow()
        self.plot[2] = self.win.addPlot(title="Raw EDA")
        self.curve[2][0] = self.plot[2].plot(pen='b')
        self.curve[2][1] = self.plot[2].plot(pen='r')
        self.win.nextRow()
        self.plot[3] = self.win.addPlot(title="Raw EMG")
        self.curve[3][0] = self.plot[3].plot(pen='b')
        self.curve[3][1] = self.plot[3].plot(pen='r')

    # init func for bar graph plot
    def bar_init(self):
        # creating a plot window
        self.plot = pg.plot()
        self.plot.setYRange(0, 100)
        self.plot.setWindowTitle('Matching score (cross correlation)')
        
        self.x = range(4)
        self.corr = [0,0,0,0,0]

        # setting x labels    
        xlab = ['eeg','ecg','eda','emg']
        ticks=[]
        for i, item in enumerate(xlab):
            ticks.append( (self.x[i], item) )
        ticks = [ticks]

        ax = self.plot.getAxis('bottom')
        ax.setTicks(ticks)

        self.bargraph = pg.BarGraphItem(x = self.x, height = self.corr, width = 0.6, brush ='r')

        self.plot.addItem(self.bargraph)
        
    # update the graph
    def update_raw_graph(self):
        for i in range(4):
            for j in range(2):
                self.curve[i][j].setData(x=self.timelist[i][j], y=self.signals[i][j])
    
    def update_bar_graph(self):
        for i in range(4):
            self.corr[i] = 100 * cross_correlation(self.timelist[i][0], self.timelist[i][1], self.signals[i][0], self.signals[i][1])
        self.plot.removeItem(self.bargraph)
        self.bargraph = pg.BarGraphItem(x = self.x, height = self.corr, width = 0.6, brush ='r')
        self.plot.addItem(self.bargraph)


def aligntimerange (t1, t2, s1, s2):
    '''
    to align time range to the same in two sets of data
    '''

    t1_rev = []
    t2_rev = []
    s1_rev = []
    s2_rev = []
    indexs_1 = 0
    indexs_2 = 0
    index2 = 0

    if t1[0] < t2[0]:
        for i in range(len(t1)):
            if (t1[i] < t2[0]):
                continue
            elif (t1[i] >= t2[0] and indexs_1 == 0):
                indexs_1 = i
                t1_rev.append(t1[i])
                s1_rev.append(s1[i])
                t2_rev.append(t2[0])
                s2_rev.append(s2[0])
            else:
                index2 += 1
                if (index2 >= len(t2)):
                    break
                else:
                    t1_rev.append(t1[i])
                    s1_rev.append(s1[i])
                    t2_rev.append(t2[index2])
                    s2_rev.append(s2[index2])
    else:
        for i in range(len(t2)):
            if (t2[i] < t1[0]):
                continue
            elif (t2[i] >= t1[0] and indexs_2 == 0):
                indexs_2 = i
                t1_rev.append(t1[0])
                s1_rev.append(s1[0])
                t2_rev.append(t2[i])
                s2_rev.append(s2[i])
            else:
                index2 += 1
                if (index2 >= len(t1)):
                    break
                else:
                    t1_rev.append(t1[index2])
                    s1_rev.append(s1[index2])
                    t2_rev.append(t2[i])
                    s2_rev.append(s2[i])

    return t1_rev, t2_rev, s1_rev, s2_rev


# analysis functions

def cross_correlation (t1, t2, s1, s2):
    '''
    calculate cross correlation of two time series data
    t1, t2 - list of time for each person
    s1, s2 - list of signals for each person 
    '''
    if s1 != [] and s2 != []:
        t1, t2, s1, s2 = aligntimerange(t1, t2, s1, s2)
        s1_norm = [x - mean(s1) for x in s1] / np.std(s1)
        s2_norm = [x - mean(s2) for x in s2] / np.std(s2)
        corr = sig.correlate(s1_norm, s2_norm, mode = 'full') / min(len(s1), len(s2))
        corr_max = max(abs(corr))
        return corr_max
    else:
        return 0