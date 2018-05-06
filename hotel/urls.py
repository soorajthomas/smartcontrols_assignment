from django.urls import path
from . import views


app_name = 'hotel'
urlpatterns = [
    path('', views.index, name='homepage'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('listing', views.hotel_listing, name='listing'),
    path('api/hotel', views.GetHotels.as_view(), name='api_hotel'),
]
