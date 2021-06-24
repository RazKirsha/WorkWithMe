from django.urls import path
from . import views

urlpatterns = [
    path('make_offer/', views.make_offer, name="make_offer"),
    path('all_pros/', views.all_pros, name="all_pros"),
]
