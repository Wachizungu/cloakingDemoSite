from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='cloakingSite_home'),
    path('simplecaptcha', views.simple_captcha, name='cloakingSite_simple_captcha'),
    path('geocheck', views.geo_check, name='cloakingSite_geo_check'),
    path('referercheck', views.referrer_check, name='cloakingSite_referrer_check'),
    path('useragentcheck', views.useragent_check, name='cloakingSite_useragent_check'),
    path('recaptchav2', views.recaptchav2, name='cloakingSite_recaptchav2'),
    path('recaptchav3', views.recaptchav3, name='cloakingSite_recaptchav3'),
    path('recaptchav3content', views.recaptchav3content, name='cloakingSite_recaptchav3content'),
    path('fingerprintjs', views.fingerprintjs, name='cloakingSite_fingerprintjs'),
    path('fingerprintjscontent', views.fingerprintjscontent, name='cloakingSite_fingerprintjscontent'),
    path('resetfingerprintjs', views.resetfingerprintjs, name='cloakingSite_resetfingerprintjs'),
    path('good', views.good, name='cloakingSite_good'),
    path('bad', views.bad, name='cloakingSite_bad'),
    path('alert', views.alert, name='cloakingSite_alert'),
    path('webcamcheck', views.webcam_check, name='cloakingSite_webcamcheck'),
    path('speakerscheck', views.speakers_check, name='cloakingSite_speakerscheck'),
    path('microphonecheck', views.microphone_check, name='cloakingSite_microphonecheck'),
    path('browserhistorycheck', views.immediate_browser_history_check, name='cloakingSite_browserhistorycheck'),
    path('datecheck', views.date_check, name='cloakingSite_datecheck'),
    path('datecheckcontent', views.date_check_content, name='cloakingSite_datecheckcontent'),
    path('openercheck', views.opener_check, name='cloakingSite_openercheck'),
    path('openercheckinitial', views.opener_check_initial, name='cloakingSite_openercheckinitial'),
    path('sweetconfirm', views.sweetconfirm, name='cloakingSite_sweetconfirm'),
]
