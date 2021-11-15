# IOT System
## Description
An IOT project using web POST and GET requests to send information from a sensor to a server and
from the server to actuators. In this example I use an access control sensor in Arduino and an 
actuator using MicroPython to turn on/off a light.

## Table of Contents (Optional)
If your README is long, add a table of contents to make it easy for users to find what they need.
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Credits](#credits)
- [Licence](#license)

## Technologies
Project was created with:
* Python 3.9.6
** Django 3.2.9
** Requests 2.26.0
* Arduino 1.8.15
* Mu 1.1.0


## Setup
In a Terminal, located in our project's folder we're going to create a virtual environment:
```
virtualenv venv
```
After creating it, we will proceed to activate it.
Linux/Mac:
```
source venv/bin/activate
```
Windows:
```
venv/Scripts/activate
```
Once our virtual environment is active we will install Django and requests:
```
pip install Django==3.2.9
pip install requests==2.26.0
```

## Usage
Update in the Arduino Code your WiFi's network information and introdue your server's IP
where needed. Afterwards upload the code into an NodeMCU board for the sensor to work.

On Mu update the actuator's WiFi's network information and upload to another NodeMCU board
for the actuator to run. Read the IP from the actuator as you'll need to update this in 
```sensor/views.py``` in function ```actuator_get_request_update```. 

NOTE: You're free to modify the models if needed for scalability if you need to add 
more Actuators.

On a terminal run ```ipconfig``` or ```ip a``` to know your computer's IP address which
we will use to update the ```ALLOWED HOSTS``` in ```gateway/gateway/setting.py```.

Run Django's server on the device you wish to use as server using its IP
```
python .\manage.py runserver {Introduce your IP here}:8000
```
Open a webbrowser in the following path:
```
http://{Introduce your IP here}:8000/status/
```



## Credits
Vecteezy.com and santima suksawat for background image used for the /status/ site

## License
MIT License

Copyright (c) [2021 [Xavier Nahim Abugannam Monteagudo]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
