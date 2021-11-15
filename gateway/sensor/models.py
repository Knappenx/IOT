from django.db import models


class Sensor(models.Model):
    """
    Sensor model:
        Sensors are automatically added when doing a POST request
        the name should be unique, but there can be multiple sensors
        in a single location.
    """
    sensor_name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50)
    people_in_room = models.IntegerField()
    added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Sensor {self.sensor_name} at {self.location}'


class Actuator(models.Model):
    """
    Actuator model:
        Actuators should be added manually with a unique name.
        Information captured from the sensors will be updated on
        server and will only send on/off information on a GET
        request.
    """
    actuator_name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50)
    actuator_status = models.IntegerField()
    added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Sensor {self.actuator_name} at {self.location}'


