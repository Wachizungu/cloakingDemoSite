from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='cloakingSite_home'),
    path('simplecaptcha', views.simple_captcha, name='cloakingSite_simple_captcha'),
    path('geocheck', views.geo_check, name='cloakingSite_geo_check'),
    path('referercheck', views.referrer_check, name='cloakingSite_referrer_check'),
    path('recaptchav2', views.recaptchav2, name='cloakingSite_recaptchav2'),
    path('recaptchav3', views.recaptchav3, name='cloakingSite_recaptchav3'),
    path('recaptchav3content', views.recaptchav3content, name='cloakingSite_recaptchav3content'),
]
