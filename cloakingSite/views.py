from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import CaptchaTestForm
from django.contrib.gis.geoip2 import GeoIP2
import requests
import json


def home(request):
    return render(request, 'cloakingSite/home.html', {'nbar': 'home'})


def simple_captcha(request):
    captcha_passed = None
    if request.POST:
        form = CaptchaTestForm(request.POST)

        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            captcha_passed = True
        else:
            captcha_passed = False

    else:
        form = CaptchaTestForm()

    return render(request, 'cloakingSite/simpleCaptcha.html',
                  {'form': form, 'captcha_passed': captcha_passed, 'nbar': 'simple_captcha'})


def geo_check(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip == '127.0.0.1':
        country_code = "BE"
    else:
        g = GeoIP2()
        country_code = g.country(ip)['country_code']

    if country_code == "BE":
        geo_check_passed = True
    else:
        geo_check_passed = False

    return render(request, 'cloakingSite/geo_check.html',
                  {'geo_check_passed': geo_check_passed, 'country_code': country_code, 'nbar': 'geo_check'})


def recaptchav2(request):
    captcha_passed = None
    if request.POST:
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {'secret': '6LcfLUobAAAAABmelnJnN-cqhNUv5BAMKF0xY-ui', 'response': request.POST.get("g-recaptcha-response")}
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            captcha_passed = json.loads(r.text)['success']
    return render(request, 'cloakingSite/recaptchav2.html', {'captcha_passed': captcha_passed, 'nbar': 'recaptchav2'})
