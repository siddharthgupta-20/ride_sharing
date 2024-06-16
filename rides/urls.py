from django.urls import path
from .views import CreateRideView

urlpatterns = [
    path('register', CreateRideView.as_view())
    ]