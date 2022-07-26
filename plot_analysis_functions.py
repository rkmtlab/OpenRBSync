from PyQt5 import QtWidgets
import pyqtgraph as pg
from statistics import mean
import scipy.signal as sig
import numpy as np
import cmath
import queue
import sys
import copy
import os
import datetime
from pyrqa.analysis_type import Cross
from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation


class PlotGraph(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PlotGraph, self).__init__(*args, **kwargs)

    def set_parameters(self, eeg_flag, ecg_flag, eda_flag, emg_flag, timedelay_p1, timedelay_p2, embedding_dimension):
        self.channelnum = 0
        channeloptions = ['eeg', 'ecg', 'eda', 'emg']
        self.channellist = []
        self.channeltitlelist = 'timestamp,'
        i = 0

        for flag in [eeg_flag, ecg_flag, eda_flag, emg_flag]:
            if flag == True:
                self.channelnum += 1
                self.channellist.append(channeloptions[i])
            i += 1
        
        for j in range(len(self.channellist)):
            if j != len(self.channellist) - 1:
                self.channeltitlelist += self.channellist[j] + ' sync score,'
            else:
                self.channeltitlelist += self.channellist[j] + ' sync score'

        self.timelist = [[[],[]] for i in range(self.channelnum)]
        self.signals = [[[],[]] for i in range(self.channelnum)]

        self.plot = [None for i in range(self.channelnum)]
        self.curve = [[None, None] for i in range(self.channelnum)]
        self.eeg_flag = eeg_flag
        self.ecg_flag = ecg_flag
        self.eda_flag = eda_flag
        self.emg_flag = emg_flag

        self.timedelay_p1 = timedelay_p1
        self.timedelay_p2 = timedelay_p2
        self.embedding_dimension = embedding_dimension

        self.signal_queue = [[queue.Queue(30), queue.Queue(30)] for i in range(self.channelnum)]
        self.signal_sum = [[0, 0] for i in range(self.channelnum)]

    # init func for raw signal plot
    def raw_init(self):
        '''
        init function called when the visualization type is raw
        '''
        self.win = pg.GraphicsLayoutWidget(show=True, title="Raw signals")
        self.win.resize(800, 800)
        self.win.setWindowTitle('Plotting')
        self.win.setBackground('w')
        #self.win.close = self.close
        i = 0
        if self.eeg_flag == True:
            self.plot[i] = self.win.addPlot(title="Raw EEG")
            self.curve[i][0] = self.plot[i].plot(pen='b')
            self.curve[i][1] = self.plot[i].plot(pen='r')
            self.win.nextRow()
            i += 1
        if self.ecg_flag == True:
            self.plot[i] = self.win.addPlot(title="Raw ECG")
            self.curve[i][0] = self.plot[i].plot(pen='b')
            self.curve[i][1] = self.plot[i].plot(pen='r')
            self.win.nextRow()
            i += 1
        if self.eda_flag == True:
            self.plot[i] = self.win.addPlot(title="Raw EDA")
            self.curve[i][0] = self.plot[i].plot(pen='b')
            self.curve[i][1] = self.plot[i].plot(pen='r')
            self.win.nextRow()
            i += 1
        if self.emg_flag == True:
            self.plot[i] = self.win.addPlot(title="Raw EMG")
            self.curve[i][0] = self.plot[i].plot(pen='b')
            self.curve[i][1] = self.plot[i].plot(pen='r')

    # init func for bar graph plot
    def bar_init(self, analysis_type):
        '''
        init function called when the visualization type is bar
        '''

        self.analysis_type = analysis_type

        # creating a plot window
        self.plot = pg.plot()
        #self.plot.close = self.close
        self.plot.setYRange(0, 100)
        if analysis_type == 'Cross Correlation':
            self.plot.setWindowTitle('Matching score (cross correlation)')
        else:
            self.plot.setWindowTitle('Matching score (cross recurrence quantification analysis)')
        self.plot.setBackground('w')

        self.x = range(self.channelnum)
        self.corr = [0 for i in range(self.channelnum)]
        self.rr = [0 for i in range(self.channelnum)]
        self.det = [0 for i in range(self.channelnum)]
        self.plv = [0 for i in range(self.channelnum)]
        self.avg_phase = [0 for i in range(self.channelnum)]

        # setting x labels    
        ticks=[]
        for i, item in enumerate(self.channellist):
            ticks.append( (self.x[i], item) )
        ticks = [ticks]

        ax = self.plot.getAxis('bottom')
        ax.setTicks(ticks)

        self.bargraph = pg.BarGraphItem(x = self.x, height = self.corr, width = 0.6, brush ='r')

        self.plot.addItem(self.bargraph)

        ## log file name
        now = datetime.datetime.now()
        myroot = 'data-server'
        os.makedirs(myroot, exist_ok=True)
        if self.analysis_type == 'Cross Correlation':
            snow = now.strftime('sync-cc-%y%m%d-%H%M')
        elif self.analysis_type == "Cross Recurrence Quantification Analysis":
            snow = now.strftime('sync-crqa-%y%m%d-%H%M')
        elif self.analysis_type == "Phase Locking Value":
            snow = now.strftime('sync-plv-%y%m%d-%H%M')
        self.sync_fname = "%s/%s.csv" % (myroot, snow)

        if self.analysis_type == 'Cross Correlation':
            with open(self.sync_fname, "a") as f:
                f.write(self.channeltitlelist + '\n')
        elif self.analysis_type == "Cross Recurrence Quantification Analysis":
            with open(self.sync_fname, "a") as f:
                f.write(self.channeltitlelist + ',det\n')
        elif self.analysis_type == "Phase Locking Value":
            with open(self.sync_fname, "a") as f:
                for ch in self.channellist:
                    f.write(ch + ',')
                for i in range(len(self.channellist)):
                    if i != len(self.channellist) - 1:
                        f.write(self.channellist[i] + '-avg phase diff,')
                    else:
                        f.write(self.channellist[i] + '-avg phase diff' + '\n')
        
    # update the graph
    def update_raw_graph(self):
        t = copy.deepcopy(self.timelist)
        s = copy.deepcopy(self.signals)
        
        for i in range(self.channelnum):
            for j in range(2):
                self.curve[i][j].setData(x=t[i][j][-60:], y=s[i][j][-60:])
    
    def update_bar_graph(self):
        t = copy.deepcopy(self.timelist)
        s = copy.deepcopy(self.signals)
        tnow = datetime.datetime.now()
        record = str(tnow) + ','

        try:
            if len(t[0][0]) >= 100 and len(t[0][1]) >= 100:
                if self.analysis_type == 'Cross Correlation':
                    for i in range(self.channelnum):
                        self.corr[i] = 100 * cross_correlation(t[i][0][-80:], t[i][1][-80:], s[i][0][-80:], s[i][1][-80:])
                    corr_str = ','.join(map(str, self.corr))
                    with open(self.sync_fname, "a") as f:
                        f.write(record + corr_str + '\n')
                    self.plot.removeItem(self.bargraph)
                    self.bargraph = pg.BarGraphItem(x = self.x, height = self.corr, width = 0.6, brush ='r')
                    self.plot.addItem(self.bargraph)
                elif self.analysis_type == "Cross Recurrence Quantification Analysis":
                    for i in range(self.channelnum):
                        result = cross_recurrence(t[i][0], t[i][1], s[i][0], s[i][1], self.timedelay_p1, self.timedelay_p2, self.embedding_dimension)
                        self.rr[i] = float(result[0])
                        self.det[i] = float(result[1])
                    rr_str = ','.join(map(str, self.rr))
                    det_str = ','.join(map(str, self.det))
                    with open(self.sync_fname, "a") as f:
                        f.write(record + rr_str + ',' + det_str + '\n')
                    self.plot.removeItem(self.bargraph)
                    self.bargraph = pg.BarGraphItem(x = self.x, height = self.rr * 100, width = 0.6, brush ='r')
                    self.plot.addItem(self.bargraph)
                elif self.analysis_type == "Phase Locking Value":
                    for i in range(self.channelnum):
                        result = 100 * phase_locking_value(t[i][0], t[i][1], s[i][0], s[i][1])
                        self.avg_phase[i] = float(result[0])
                        self.plv[i] = float(result[1])
                    avg_phase_str = ','.join(map(str, self.avg_phase))
                    plv_str = ','.join(map(str, self.plv))
                    print(self.plv)
                    with open(self.sync_fname, "a") as f:
                        f.write(record + plv_str + ',' + avg_phase_str + '\n')
                    self.plot.removeItem(self.bargraph)
                    self.bargraph = pg.BarGraphItem(x = self.x, height = [self.plv[i] * 100 for i in range(len(self.plv))], width = 0.6, brush ='r')
                    self.plot.addItem(self.bargraph)
        except:
            print("Error: Signal type is not selected. Please quit and select again.")

    def close(self):
        sys.exit(0)

def aligntimerange (t1, t2, s1, s2):
    '''
    to align time range to the same in two sets of data
    '''

    t1_rev = []
    t2_rev = []
    s1_rev = []
    s2_rev = []
    s_flag = 0
    indexs_2 = 0
    index2 = 0

    if t1[0] < t2[0]:
        for i in range(len(t1)):
            if (t1[i] < t2[0]):
                continue
            elif (t1[i] >= t2[0] and s_flag == 0):
                s_flag = 1
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
        if np.std(s1) != 0:
            s1_norm = [x - mean(s1) for x in s1] / np.std(s1)
        else:
            s1_norm = [x - mean(s1) for x in s1]
        if np.std(s2) != 0:
            s2_norm = [x - mean(s2) for x in s2] / np.std(s2)
        else:
            s2_norm = [x - mean(s2) for x in s2]
        corr = sig.correlate(s1_norm, s2_norm, mode = 'full') / min(len(s1), len(s2))
        # max lag is 4 seconds
        if len(corr)>80:
            corr_max = max(abs(corr[40:79]))
        else:
            corr_max = max(abs(corr))
        return corr_max
    else:
        return 0

def cross_recurrence (t1, t2, s1, s2, timedelay_p1, timedelay_p2, embedding_dimension):
    '''
    conduct cross recurrence quantification analysis of two time series data
    t1, t2 - list of time for each person
    s1, s2 - list of signals for each person
    timedelay_p1, timedelay_p2 - time delay parameter to embed signals (default = 1)
    embedding_dimension - embedding dimension parameter to embed signals (default = 1)
    '''
    if s1 != [] and s2 != []:
        t1, t2, s1, s2 = aligntimerange(t1, t2, s1, s2)
        time_series_1 = TimeSeries(s1,
                           embedding_dimension=embedding_dimension,
                           time_delay=timedelay_p1)
        time_series_2 = TimeSeries(s2,
                           embedding_dimension=embedding_dimension,
                           time_delay=timedelay_p2)
        time_series = (time_series_1,
               time_series_2)
        settings = Settings(time_series,
                            analysis_type=Cross,
                            neighbourhood=FixedRadius(0.1),
                            similarity_measure=EuclideanMetric,
                            theiler_corrector=0)
        computation = RQAComputation.create(settings,
                                            verbose=True)
        result = computation.run()
        result.min_diagonal_line_length = 2
        result.min_vertical_line_length = 2
        result.min_white_vertical_line_length = 2
        return result.recurrence_rate, result.determinism
    else:
        return 0, 0

def phase_locking_value(t1, t2, s1, s2):
    '''
    calculate phase locking value of two time series data
    t1, t2 - list of time for each person
    s1, s2 - list of signals for each person
    '''
    if s1 != [] and s2 != []:
        t1, t2, s1, s2 = aligntimerange(t1, t2, s1, s2)
        sig1_hill=sig.hilbert(s1)
        sig2_hill=sig.hilbert(s2)
        phase_s1=np.angle(sig1_hill)
        phase_s2=np.angle(sig2_hill)
        Inst_phase_diff=phase_s1-phase_s2
        plv = complex(0,0)
        for i in range(len(Inst_phase_diff)):
            plv += cmath.exp(complex(0, Inst_phase_diff[i]))
        plv = abs(plv)/len(Inst_phase_diff)
        avg_phase=np.average(Inst_phase_diff)
        return avg_phase, plv
    else:
        return 0, 0
