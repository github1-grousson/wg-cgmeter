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
### 1. Initialization
When launching, let the initialization procces with nothing on gauges.
<img src="https://user-images.githubusercontent.com/113672043/218427688-0b5dded0-8e99-4444-8a0f-500f3f34c516.png" width="600">

### 2. Tare
First remove any weights on gauges and tare by pressing "Tare" button
<img src="https://user-images.githubusercontent.com/113672043/218429639-4cfc3ba8-c12b-4bcc-8647-89ea2bc96099.png" width="600">

Click OK when done

<img src="https://user-images.githubusercontent.com/113672043/218429855-bc46334e-15f0-440b-9259-37e9080f1756.png" width="600">

### 3. Calibrate
If needed, calibrate gauges by pressing "Calibrate" button. A new window is displayed.

<img src="https://user-images.githubusercontent.com/113672043/218431891-6a1a90ac-d498-4d74-9ae4-e7a071fe9dd5.png" width="600">

Then, enter the calibration weight and put it on the fisrt gauge and click on the button of the corresponding gauge.

<img src="https://user-images.githubusercontent.com/113672043/218432219-ee25fa4e-74c6-44cb-b5d3-8e9b7f4328db.png" width="600">

> Calibration is not need each time as it is saved in the config file.

### 4. Read
To start reading weights and CG position, just click on "Start" button
<img src="https://user-images.githubusercontent.com/113672043/218433726-831ed466-5346-4845-853e-e1e62bcdb315.png" width="600">

If CG position is out of the wanted CG (blue rectangle), then the CG position is a red point and value is displayed also in red at the top-middle for the X-axis position and at the left-center for the Y-axis position.
Adjust CG by adding or removing waights in the plane. When CG is in range, point and valus becomes green:

<img src="https://user-images.githubusercontent.com/113672043/218436327-8a729003-556c-49f7-a29e-997cb903a4e3.png" width="600">

### 5. Configuration
Configuration is stored in the file `planes.json` located in the `config` directory. For the moment, only the first plane is loaded.
The plane config is formed like this :
```
[
    {
        "name": "MXS",
        "wheelbase": 810,
        "wheeltrack": 277,
        "edge2mainwheels": -10,
        "edge2cgxrange": [
            89,
            101
        ],
        "origin2cgyrange": [
            -20,
            20
        ]
    }
]
```
- **name** : name of the plane, it will be displayed at top rigth of the screen
- **wheelbase** : distance in mm between front wheels and tail wheel
- **wheeltrack** : distance in mm between the two front wheels
- **edge2mainwheels** : distance in mm between the leading edge wing and the front wheels. Value should be negative if wheels are in front of leading edge wing.
- **edge2cgxrange** : range in mm, starting from leading edge wing of the wanted CG position. This is the X-axis CG position.
- **origin2cgyrange** : range in mm from the roll axis of the plane. This is the Y-axis CG position.

## History
* 0.1.0 : main.py is a POC, it displays only weights of the load cells. Based on guizero (pip install guizero)
* 0.2.0 : new UI based on tkinter and wgkinter, shows the different weights
* 0.3.0 : display the CG position in X and Y axis based on 
