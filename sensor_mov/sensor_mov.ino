#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Your_Router_Name";
const char* password = "Your_WiFi_Password";

const char *host = "http://<replace with your server IP>/status/";

int people_counter = 0;
int test_number = 0;

bool wait_off = false;
bool light_on = false;
bool sensor_is_on = true;

int light = 13;                 // pin assigned for led
int sensor_one = 2;             // pin assigned for sensor one
//int sensor_one_state = LOW;     initial PIR sensor value - no movement
int sensor_one_status = LOW;      // variable to store one sensor status

int sensor_two = 4;
//int sensor_two_state = LOW;
int sensor_two_status = LOW;

void setup(){
    // Sets up WiFi connection
    pinMode(light, OUTPUT);
    pinMode(sensor_one, INPUT);
    pinMode(sensor_two, INPUT);
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

void light_status(){
    // Turns light on/off depending on people counter
    if (people_counter > 0){
        digitalWrite(light,HIGH);
        //delay(500);
        Serial.println((String)"People in the room: " + people_counter);
        //Serial.println(people_counter);
    }
    else {
        digitalWrite(light, LOW);
        //delay(500);
        Serial.println((String)"People in the room: " + people_counter);
        //Serial.println(people_counter);
    }
}

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

void sensor_one_true(){  
    // Stat Sensor 1 which remains on as long as there is a person being
    // detected on sensor 1
    Serial.println("State Sensor 1");
    while(sensor_one_status == HIGH){
        sensor_one_status = digitalRead(sensor_one);    //read sensor 1 val
        sensor_two_status = digitalRead(sensor_two);    //read sensor 2 val
        if(sensor_one_status == HIGH && sensor_two_status == HIGH){
            people_counter ++;
            wait_off = true;
            return; 
        }
        delay(1200);
    }
    Serial.println("Exits State Sensor 1");
}

void sensor_two_true(){
    // Stat Sensor 2 which remains on as long as there is a person being
    // detected on sensor 3
    Serial.println("Enters State Sensor 2");
    while(sensor_two_status == HIGH){
        sensor_one_status = digitalRead(sensor_one);    //read sensor 1 val
        sensor_two_status = digitalRead(sensor_two);    //read sensor 2 val
        if(sensor_one_status == HIGH && sensor_two_status == HIGH){
            people_counter --;
            if(people_counter < 0){
                people_counter = 0;
            }
            wait_off = true;
            return; 
        }
        delay(1200);
    }
    Serial.println("Exits State Sensor 2");
}

void wait_sensors_off(){
    // State which gives an extra control layer to the sensor
    // allows to avoid people counter until sensors are no longer
    // busy
    Serial.println("Enters wait off state");
    while(wait_off == true){
        sensor_one_status = digitalRead(sensor_one);    //read sensor 1 val
        sensor_two_status = digitalRead(sensor_two);    //read sensor 2 val
        if (sensor_one_status == LOW && sensor_two_status == LOW){
            wait_off = false;
        }
        delay(1200);
    }
    Serial.println("Exits wait off");
}

void loop(){
    if (wait_off == false){
        sensor_one_status = digitalRead(sensor_one); 
        sensor_two_status = digitalRead(sensor_two);
        if (sensor_one_status == HIGH){
            sensor_one_true();
            light_status();
            post_json();
        }
        else if(sensor_two_status== HIGH){
            sensor_two_true();
            light_status();
            post_json();
        }
    }
    else if (wait_off == true){
        wait_sensors_off();
    }
}
