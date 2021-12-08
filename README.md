# IoT Architecture prototype

## Table of Contents
If your README is long, add a table of contents to make it easy for users to find what they need.
- [IoT Architecture prototype](#iot-architecture-prototype)
  - [Table of Contents](#table-of-contents)
  - [IoT Architecture](#iot-architecture)
  - [Technologies](#technologies)
  - [Hardware](#hardware)
  - [Gateway](#gateway)
    - [Setup](#setup)
    - [Django Settings](#django-settings)
    - [Django Views](#django-views)
  - [Actuator](#actuator)
  - [Sensor](#sensor)
  - [User Interface](#user-interface)
  - [Usage](#usage)
  - [Demo Video](#demo-video)
  - [Credits](#credits)
  - [License](#license)

## IoT Architecture
An IoT project using web POST and GET requests to send information from a sensor to a server and
from the server to actuators. In this example I use an access control sensor in Arduino and an 
actuator using MicroPython to turn on/off a light.

This project was designed to work as a 4 layered IoT architecture.

![4 layerd IoT architecture](https://github.com/Knappenx/IOT/blob/main/resources/images/IoT_arq.PNG)

- **Physical layer**: Sensors and actuators.
  - *Sensor*: An occupancy sensor which sends information through an HTTP request to the Gateway's server every time it senses a person going in or out of a room.
  - *Actuator*: The actuator is just a simple LED on/off. It is updated through a ```GET``` request sent by the server if certain criteria is met, like having more than one person in the room will turn it on, having no people will turn it off  or if the user decides to activate it directly using the User Interface or UI.

- **Communication and connectivity layer**:
  - *Communication*: All communication is done using HTTP protocol, specifically with ```POST``` and ```GET``` requests.
  - *Connectivity*: The connectivity of all devices and applications is being done through a Jetson Nano with a Django server application.

- **Data and security layer**:
  - Data is stored and managed with Django's ORM in SQLite3. This data is used to execute the action described on the physical layer.

- **Application layer**:
  - The UI allows to display and interact with registered sensors and actuators.

## Technologies
This project was created with:
* Python 3.9.6
  * Django 3.2.9
  * Requests 2.26.0
* Arduino 1.8.15
* Mu 1.1.0

## Hardware
* 2x  PIR sensors
* 2x  NodeMCU circuit board
* 1x  LED

## Gateway
For this prototype a Jetson Nano was used as Gateway, though any other device capable of running Django will work for this purpose.

### Setup
In a Terminal, located in our project's folder it is recommended to create a virtual environment:
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
### Django Settings
On a terminal run ```ipconfig``` or ```ip a``` to know your computer's IP address which
we will use to update the ```ALLOWED HOSTS``` in ```gateway/gateway/setting.py```.
```python
ALLOWED_HOSTS = ['localhost', '<Insert your gateway/computer IP>']
```

### Django Views
We need to update the actuator's IP value. For now it only allows for a single actuator, though in the future this funtion will allow to make these changes automatically by implementing variable queries from Database.

``` python
def actuator_get_request_update(status):
    actuator_url = f"http://<enter actuator's IP>/actuator={status}"
    # Example: actuator_url = f"http://192.168.1.100/actuator={status}"
    requests.get(
            actuator_url, 
            headers = {'Content-Type': 'text/html'}
        )
```
**NOTE:** You're free to modify the models if needed for scalability if you need to add 
more Actuators.


## Actuator
The actuator was programmed in mycropython, using Mu as IDE to upload the program. 

First we need to capture our Networ's name and password for the sensor to connect. 
```python
ssid = "Your WiFi network name" 
password = "Your Wifi network password"
```

This request.find reading relates to the **```GET```** message sent by the Gateway, where ON/OFF were part of the request message as ```status```
```python
if request.find('/actuator=on') == 6:
        print('Actuator ON')
        actuator.value(1)
    if request.find('/actuator=off') == 6:
        print('Actuator OFF')
        actuator.value(0)
    response = "OK"
```

## Sensor

On the sensor setup function WiFi parameters and connection will be established. We need to introduce networ's name and password.
```cpp

const char* ssid = "Your_Router_Name";
const char* password = "Your_WiFi_Password";

void setup(){
    Serial.begin(115200);
    Serial.println("\nWiFi station setting");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.print("Connecting");
    while (WiFi.status() != WL_CONNECTED){
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connection established");
    Serial.print("Device ip address: ");
    Serial.println(WiFi.localIP());
}
```
Using ```WiFi.mode(WIFI_STA)``` will set the sensor as a station to allow us to both send and receive information, though in this case the sensor will only send information to the server. To send information I created the ```post_json``` function. The information will be sent to the defined host. Lastly we call ```post_json``` function whenever we want to register information on our server, which will be made through an http **```POST```** request. 

```cpp

const char *host = "http://<replace with your server's IP>/status/";

void post_json(){
    // Configures, prepares and sends a POST message with sensor's data
    WiFiClient client;
    HTTPClient http;

    String sensor_name = "Access Counter Sensor";
    String room = "Main Room";
    String ppl_in_room = String(people_counter);

    String postData;
    postData = "{\"sensor_name\": \"" + sensor_name + "\",\"ppl_in_room\": \"" + ppl_in_room + "\",\"room_name\": \"" + room + "\"}";

    Serial.print("Request Link:");
    Serial.println(host);

    Serial.print("Post Data:");
    Serial.println(postData);

    http.begin(client, host);
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST(postData);
    String payload = http.getString();

    Serial.print("Response Code:");
    Serial.println(httpCode);
    Serial.print("Returned data from Server: ");
    Serial.println(payload);
    http.end();
    delay(5000);
}
```
## User Interface
This is a preview of what the USer Interface looks like. From here we can visualize sensor's data and actuator's status. You can intercat with actuators from here as well.

![IoT User Interface](https://github.com/Knappenx/IOT/blob/main/resources/images/ui.PNG)

## Usage

Run Django's server on the device you wish to use as server using its IP
```
python .\manage.py runserver {Introduce your IP here}:8000
```
Open a web browser in the following path:
```
http://{Introduce your IP here}:8000/status/
```
Sensors and actuators will be related by their location, this means that if both of them share the same location i.e. **"Kitchen"**, the action that will come up from the sensor's data will trigger an action in actuators sharing the same location **"Kitchen"**.

Sensors can be automatically added to database on their first **```POST```**, but actuators do need to be added via shell commands or using the admin panel.


## Demo Video
Video demonstration available [here](https://youtu.be/uvCQJizTpLY 'Four layered IoT application')

## Credits
Vecteezy.com and Santima Suksawat for background image used for ```/status/``` site`template.

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
