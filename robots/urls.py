from django.urls import path

from .views.create_robot import create_robot


urlpatterns = [
    # Endpoint for creating a robot
    path('create_robot', create_robot, name='create_robot'),
]
