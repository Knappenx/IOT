from django.contrib import admin

# My defined models:
from sensor.models import Sensor, Actuator

admin.site.register(Sensor)
admin.site.register(Actuator)