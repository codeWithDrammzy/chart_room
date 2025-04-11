
from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('my-login/', views.my_login, name='my-login'),

    path('room/<int:pk>/', views.room, name='room'),
    path('create-room/', views.creatRoom, name='create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),
    path('register/', views.create_user, name="register"),
   
    path('my-logout', views.my_logout, name="my-logout"),
    path('profile/<str:pk>', views.user_profile, name="profile"),
    path('update-user', views.update_user, name="update-user")
   
]

