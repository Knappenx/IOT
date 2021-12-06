# IoT Architecture prototype

## General description

An IOT project using web POST and GET requests to send information from a sensor to a server and
from the server to actuators. In this example I use an access control sensor in Arduino and an 
actuator using MicroPython to turn on/off a light.

## IoT Architecture

This project was designed to work as a 4 layered IoT architecture.

<Insert picture>

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

## Gateway
For this prototype a Jetson Nano was used as Gateway, though any other device capable of running Django will work for this purpose.

## Actuator

## Sensor
On the sensor setup function WiFi parameters and connection will be established. 
```arduino

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

```arduino
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
## UI

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
Open a web browser in the following path:
```
http://{Introduce your IP here}:8000/status/
```
## Demo Video

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