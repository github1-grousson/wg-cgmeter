# wg-cgmeter
A Raspberry/hx711 based CG Meter for RC planes

## Introduction
The goal is to use 3 Load Cells connected to raspberry pi through hx711 modules.
Just put the RC plane on the three load cells a read CG parameters on screen.

## Dependencies
* [gandalf15/HX711](https://github.com/gandalf15/HX711)
```bash
$pip install 'git+https://github.com/bytedisciple/HX711.git#egg=HX711&subdirectory=HX711_Python3'
```
* [github1-grousson/wgtinker](github1-grousson/wgtinker)
``` bash
~$ cd ~/wgkinter/
~/wgkinter$ pip install .
```
* PIL
```bash
$pip install pillow
if ImportError: cannot import name 'ImageTk' from 'PIL' (/usr/lib/python3/dist-packages/PIL/__init__.py)
then try :
$sudo pip3 install pillow --upgrade
```

## How to
### 1. Tare
First remove any weight on gauges and tare by pressing "Tare" button
### 2. Calibrate
Then calibrate gauges by pressing "Calibrate" button. A new window is displayed. There, enter the calibration weight and put it on the fisrt gauges and click on the button of the corresponding gauge.

<img src="https://user-images.githubusercontent.com/113672043/214118059-e3bc23e9-1267-47e0-8c17-c6180ecbd167.png" width="600">

> Calibration is not need each time as it is saved in the config file.

### 3. Read
To start reading weights, just click on "Start" button

<img src="https://user-images.githubusercontent.com/113672043/214119208-15f6e85a-f438-4e04-875d-d123878a3a2d.png" width="600">

## History
* 0.1.0 : main.py is a POC, it displays only weights of the load cells. Based on guizero (pip install guizero)
* 0.2.0 : new UI based on tkinter and wgkinter, shows the different weights
