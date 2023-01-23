# wg-cgmeter
A Raspberry/hx711 based CG Meter for RC planes

## Introduction
The goal is to use 3 Load Cells connected to raspberry pi through hx711 modules.
Just put the RC plane on the three load cells a read CG parameters on screen.

## Dependencies
* [gandalf15/HX711](gandalf15/HX711)
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

## History
* 0.1.0 : main.py is a POC, it displays only weights of the load cells. Based on guizero (pip install guizero)
* 0.2.0 : new UI based on tkinter and wgkinter, shows the different weights
* 0.3.0 : Add CG calculation and display from leading edge of the wing
