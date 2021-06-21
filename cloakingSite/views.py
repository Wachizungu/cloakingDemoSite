from django.http import HttpResponse, FileResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import CaptchaTestForm
from django.contrib.gis.geoip2 import GeoIP2
import requests
import json
from django.conf import settings


def home(request):
    return render(request, 'cloakingSite/home.html', {'nbar': 'home'})


def simple_captcha(request):
    captcha_passed = None
    if request.POST:
        form = CaptchaTestForm(request.POST)

        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            if settings.EICAR_MODE:
                return FileResponse(open('cloakingSite/eicar.com', 'rb'))
            else:
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
        if settings.EICAR_MODE:
            return FileResponse(open('cloakingSite/eicar.com', 'rb'))
        else:
            geo_check_passed = True
    else:
        geo_check_passed = False

    return render(request, 'cloakingSite/geo_check.html',
                  {'geo_check_passed': geo_check_passed, 'country_code': country_code, 'nbar': 'geo_check'})


def recaptchav2(request):
    captcha_passed = None
    if request.POST:
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {'secret': settings.RECAPTCHA_SECRET, 'response': request.POST.get("g-recaptcha-response")}
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            captcha_passed = json.loads(r.text)['success']
            if captcha_passed and settings.EICAR_MODE:
                return FileResponse(open('cloakingSite/eicar.com', 'rb'))
    return render(request, 'cloakingSite/recaptchav2.html', {'captcha_passed': captcha_passed, 'nbar': 'recaptchav2'})


def referrer_check(request):
    referrer = None
    if 'HTTP_REFERER' in request.META:
        referrer = request.META['HTTP_REFERER']
        if referrer == 'https://www.google.com/':
            if settings.EICAR_MODE:
                return FileResponse(open('cloakingSite/eicar.com', 'rb'))
            else:
                referrer_check_passed = True
        else:
            referrer_check_passed = False
    else:
        referrer_check_passed = None
    return render(request, 'cloakingSite/referer_check.html',
                  {'referrer_check_passed': referrer_check_passed, 'referrer': referrer, 'nbar': 'referercheck'})
