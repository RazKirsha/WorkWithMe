from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.homepage, name='homepage'),
    path('send_email/', views.sendEmail, name="send_email"),
    path('profile/<int:pk>/', views.profile, name="profile"),
    path('edit_meeting/<int:pk>/', views.edit_meeting, name="edit_meeting"),
    path('delete_meeting/<int:pk>/', views.delete_meeting, name="delete_meeting"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)