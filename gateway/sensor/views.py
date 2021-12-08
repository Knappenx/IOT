from django.shortcuts import redirect, render
from sensor.models import Sensor, Actuator
from django.views.decorators.csrf import csrf_exempt
import json, requests


def sensor_input_database(request):
    """
    Allows to read the information sent by sensors through POST messages,
    add the sensor to data base if it doesn't exist or update in case it does.
    After updating it will send sensors data to be processed by the 
    auto_update_actuator.
    """
    if request.method == 'POST':
        # if sensor exists update else add
        data = json.loads(request.body)
        sensor_name = data['sensor_name']
        people_in_room = data['ppl_in_room']
        location = data['room_name']
        sensor_query = Sensor.objects.filter(sensor_name=sensor_name)
        if len(sensor_query) == 0:
            add_sensor = Sensor(
                sensor_name = sensor_name,
                people_in_room = people_in_room,
                location = location
            )
            add_sensor.save()
            print("Adding sensor to DB")
            auto_update_actuator(data)
            return data
        else:
            sensor_query.update(people_in_room=int(people_in_room))
            print("Updating sensor in DB")
            auto_update_actuator(data)
            return data


def auto_update_actuator(related_sensor):
    """
    Will analyze sensor data and look for actuator that match with same 
    location. If there is a location match, it will update the status of
    related actuators in data base adn proceed to sen a GET request to
    update the related devices.

    Note: Designed for an access control sensor
    """
    if related_sensor:
        actuator_query = Actuator.objects.filter(location=related_sensor['room_name'])
        if len(actuator_query) != 0:
            print(actuator_query)
            for actuator in actuator_query:
                if int(related_sensor['ppl_in_room']) > 0:
                    status = 'on'
                    actuator_query.update(actuator_status=1)
                    actuator_get_request_update(status)
                elif int(related_sensor['ppl_in_room']) == 0:
                    status = 'off'
                    actuator_query.update(actuator_status=0)
                    actuator_get_request_update(status)
   
   
def actuator_get_request_update(status):
    """
    Sends a status ON or OFF on a GET message to the actuator.

    TODO: IP address should be a variable for each device, to control
        them individually.
    """
    actuator_url = f'http://192.168.0.28/actuator={status}'
    requests.get(
            actuator_url, 
            headers = {'Content-Type': 'text/html'}
        )


def manual_update_actuator(request, actuator_id):
    """
    Allows to manually override actuator's ON/OFF status from UI
    """
    actuator = Actuator.objects.get(id=actuator_id)
    if actuator.actuator_status == 1:
        actuator.actuator_status = 0
        actuator.save()
        status = 'off'
        actuator_get_request_update(status)
    else:
        actuator.actuator_status = 1
        actuator.save()
        status = 'on'
        actuator_get_request_update(status)
    return redirect('/status/')


@csrf_exempt
def sensor_status(request):
    """
    Main function which renders the website. 
    Has a csrf_exempt since sensor's POST request is not validated.
    """
    status = ""
    sensor_data = sensor_input_database(request)
    #auto_update_actuator(sensor_data)
    context = {
        'sensors': Sensor.objects.all(),
        'actuators': Actuator.objects.all(),
    }
    return render(request, 'status.html', context)
