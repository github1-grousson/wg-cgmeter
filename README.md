# wg-cgmeter
A Raspberry/hx711 based CG Meter for RC planes

## Introduction
The goal is to use 3 Load Cells connected to raspberry pi through hx711 modules.
Just put the RC plane on the three load cells a read CG parameters on screen.

## Dependencies
* [gandalf15/HX711](gandalf15/HX711)
```bash
pip3 install 'git+https://github.com/bytedisciple/HX711.git#egg=HX711&subdirectory=HX711_Python3'
```

## History
* 0.1.0 : main.py is a POC, it displays only weights of the load cells. Based on guizero (pip install guizero)
* 0.2.0 : new UI based on tkinter abd wgkinter
