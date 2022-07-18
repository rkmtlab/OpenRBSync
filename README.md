# sync-tool

## server.py
receive data from clients and visualize signals

### visualize options

1. raw signal plot
2. bar graph of cross-correlations
- calculate cross correlations of the past 1000 signals
- display the maximum correlation among time shifted correlations

## client.py / client2.py
receive data from sensors and send it to the server

### sensor options

1. bitalino (eeg, ecg, eda, emg)
2. FocusCalm (eeg)
