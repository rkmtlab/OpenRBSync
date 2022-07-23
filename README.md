# OpenRBSync

A toolkit to collect physiological data from two remote devices, save it to a csv file with synchronized timestamps, send it to a server, and visualize its time-windowed raw data/its synchronicity.


# Getting Started

## Prerequisits
### Sensors
Our current version only supports [BITalino](https://www.pluxbiosignals.com/collections/shop/products/bitalino-revolution-plugged-kit-ble-bt) (eeg, ecg, eda, emg) as a sensor to use.
We plan to increase the options of sensors in the near future.

### Software
BITalino needs [OpenSignals](https://support.pluxbiosignals.com/knowledge-base/introducing-opensignals-revolution/), an official software to acquire signals from BITalino via Bluetooth. Please install this software beforehand.

## Installing
Run the following command and install OpenRBSync.
```
git clone https://github.com/rkmtlab/OpenRBSync.git
```

## Running the program

### Running a server
In a server PC, run server.py.
```
cd OpenRBSync
python server.py
```
* In a GUI dialog, set appropriate parameters.
    * Signals to receive from clients
    * Port number to serve
    * A Visualization method
    * An analysis method
* Default parameters are set for port number and cross recurrence quantification analysis, but you can change them as you want.

[![Image from Gyazo](https://i.gyazo.com/8caf1e56f8684ccecd9a3bd0a463dd85.gif)](https://gyazo.com/8caf1e56f8684ccecd9a3bd0a463dd85)

* Open another terminal window, and run ngrok command.
```
ngrok http [port number you set in the gui dialog (default is 3030)]
```

* Ngrok window will be showed up, so copy the link displayed. You should not close this ngrok window by the end of the data acquisition.

[![Image from Gyazo](https://i.gyazo.com/0e7eaa59cdb6a9e50e86b3e79160f9f5.gif)](https://gyazo.com/0e7eaa59cdb6a9e50e86b3e79160f9f5)

### Running a client
In each client PC, open OpenSignals and set up your BITalino.
* Open System preferences of your computer, go to Bluetooth preference and connect your BITalino device via Bluetooth.

* Launch OpenSignals, find your BITalino device, and enable it.

[![Image from Gyazo](https://i.gyazo.com/7a59c2a177f324d7823d66ad3e482d05.gif)](https://gyazo.com/7a59c2a177f324d7823d66ad3e482d05)

* Click on the box and configure parameters.

[![Image from Gyazo](https://i.gyazo.com/c7fe8e0f0abdb3f015d5dca109997bdb.gif)](https://gyazo.com/c7fe8e0f0abdb3f015d5dca109997bdb)

* Click on the setting icon, go to the INTEGRATION tab, and enable Lab Streaming Layer.

[![Image from Gyazo](https://i.gyazo.com/f00d35b0041f19150f9e148006e90149.gif)](https://gyazo.com/f00d35b0041f19150f9e148006e90149)

* Click the red button and start data acquisition.

Then, open terminal on your computer and run client.py.
```
python client.py
```
* In a GUI dialog, set appropriate parameters.
    * MAC address of your BITalino device you have selected on OpenSignals. (Written in the back side of the device / OpenSignals)
    * Signal types to send
    * Host link you get by ngrok command on your server computer
    
[![Image from Gyazo](https://i.gyazo.com/f4a0607344fff04fcd2c468187fcf215.gif)](https://gyazo.com/f4a0607344fff04fcd2c468187fcf215)

# System configurations

## server.py
Receive data from clients and visualize signals.

### visualize options

1. Raw signal plot

[![Image from Gyazo](https://i.gyazo.com/1c097c94e6f75fc26e98f9a1de58ce7e.png)](https://gyazo.com/1c097c94e6f75fc26e98f9a1de58ce7e)

2. Bar graph of synchronicity
* Calculate cross correlations of the past 500 signals and display the maximum correlation among time shifted correlations (multiplied by a hundred).
* Conduct Cross Recurrence Quantification Analysis and display recurrence rate multiplied by a hundred. Determinism is also saved in a csv file.

[![Image from Gyazo](https://i.gyazo.com/b74ae6556e894ab959565cbc83863d9e.png)](https://gyazo.com/b74ae6556e894ab959565cbc83863d9e)

## client.py / client2.py
Receive data from sensors and send it to the server.

### sensor options

1. bitalino (eeg, ecg, eda, emg)

### Authors
Yuna Watanabe, Kotaro Omori (The University of Tokyo)