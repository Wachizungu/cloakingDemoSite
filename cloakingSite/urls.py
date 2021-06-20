from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='cloakingSite_home'),
    path('simplecaptcha', views.simple_captcha, name='cloakingSite_simple_captcha'),
    path('geocheck', views.geo_check, name='cloakingSite_geo_check'),
]
