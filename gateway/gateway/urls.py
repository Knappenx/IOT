from django.contrib import admin
from django.urls import path

# App views imports:
from sensor import views as sensor_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('status/', sensor_views.sensor_status, name='status'),
    path('actuator/<int:actuator_id>/', sensor_views.manual_update_actuator, name='actuator'),
]
