from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.pro_profile, name="pro_profile"),
    path('accept_offer/<int:pk>/', views.accept_offer, name="accept_offer"),
    # path('my_meetings/', views.my_meetings, name="my_meetings"),
    path('video_chat/<int:pk>/', views.video_chat, name="video_chat"),
    path('create_feedback/<int:pk>/', views.create_feedback, name="create_feedback"),
]