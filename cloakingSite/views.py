from django.http import HttpResponse, FileResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import CaptchaTestForm
from django.contrib.gis.geoip2 import GeoIP2
import requests
import json
from django.conf import settings
from cloakingSite.models import Fingerprint
from datetime import datetime


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
        payload = {'secret': settings.RECAPTCHAV2_SECRET_KEY, 'response': request.POST.get("g-recaptcha-response")}
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            captcha_passed = json.loads(r.text)['success']
            if captcha_passed and settings.EICAR_MODE:
                return FileResponse(open('cloakingSite/eicar.com', 'rb'))
    return render(request, 'cloakingSite/recaptchav2.html',
                  {'captcha_passed': captcha_passed, 'site_key': settings.RECAPTCHAV2_SITE_KEY, 'nbar': 'recaptchav2'})


def recaptchav3(request):
    return render(request, 'cloakingSite/recaptchav3.html',
                  {'site_key': settings.RECAPTCHAV3_SITE_KEY, 'nbar': 'recaptchav3'})


def recaptchav3content(request):
    captcha_passed = None
    score = None
    if request.POST:
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {'secret': settings.RECAPTCHAV3_SECRET_KEY, 'response': request.POST.get("token")}
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            response = json.loads(r.text)
            captcha_success = response['success']
            if captcha_success:
                score = response['score']
                if score > 0.5:
                    captcha_passed = True
            if captcha_passed and settings.EICAR_MODE:
                return FileResponse(open('cloakingSite/eicar.com', 'rb'))
    return render(request, 'cloakingSite/recaptchav3_content.html', {'captcha_passed': captcha_passed, 'score': score})


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
                  {'referrer_check_passed': referrer_check_passed, 'referrer': referrer, 'nbar': 'referrercheck'})


def fingerprintjs(request):
    return render(request, 'cloakingSite/fingerprintjs.html', {'nbar': 'fingerprintjs'})


def fingerprintjscontent(request):
    visits = 0
    if request.POST:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # set ip
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        hash = request.POST.get("hash")

        # Check if fingerprint already exists
        try:
            fingerprint = Fingerprint.objects.get(hash=hash)
        except Fingerprint.DoesNotExist:
            fingerprint = None

        # If fingerprint already exists increment visits, otherwise save new fingerprint
        if fingerprint:
            fingerprint.visits += 1
        else:
            fingerprint = Fingerprint(hash=hash, ip=ip, visits=1)
        fingerprint.save()
        visits = fingerprint.visits

    return render(request, 'cloakingSite/fingerprintjs_content.html', {'visits': visits})


def resetfingerprintjs(request):
    Fingerprint.objects.filter().delete()
    return redirect('/cloakingsite/fingerprintjs')


def useragent_check(request):
    referrer = None
    useragent = request.META.get('HTTP_USER_AGENT')
    if useragent == 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0':
        if settings.EICAR_MODE:
            return FileResponse(open('cloakingSite/eicar.com', 'rb'))
        else:
            useragent_check_passed = True
    else:
        useragent_check_passed = False
    return render(request, 'cloakingSite/useragent_check.html',
                  {'useragent_check_passed': useragent_check_passed, 'useragent': useragent, 'nbar': 'useragentcheck'})


def good(request):
    return render(request, 'cloakingSite/good.html')


def bad(request):
    if settings.EICAR_MODE:
        return FileResponse(open('cloakingSite/eicar.com', 'rb'))
    return render(request, 'cloakingSite/bad.html')


def alert(request):
    return render(request, 'cloakingSite/alert.html', {'nbar': 'alert'})


def webcam_check(request):
    return render(request, 'cloakingSite/webcam_check.html', {'nbar': 'webcamcheck'})


def microphone_check(request):
    return render(request, 'cloakingSite/microphone_check.html', {'nbar': 'microphonecheck'})


def speakers_check(request):
    return render(request, 'cloakingSite/speakers_check.html', {'nbar': 'speakerscheck'})


def immediate_browser_history_check(request):
    return render(request, 'cloakingSite/immediate_browser_history.html', {'nbar': 'immediatebrowserhistory'})


def date_check(request):
    return render(request, 'cloakingSite/date_check.html', {'nbar': 'datecheck'})


def date_check_content(request):
    date_check_passed = None
    if request.POST:
        now = datetime.now()
        date_received = request.POST.get("date")
        date_received_datetime = datetime.strptime(date_received, '%Y/%m/%d')
        date_diff = date_received_datetime - now

        if abs(date_diff.days) < 3:
            date_check_passed = True
        else:
            date_check_passed = False

    return render(request, 'cloakingSite/date_check_content.html',
                  {'date_check_passed': date_check_passed, 'date_received': date_received})


def opener_check_initial(request):
    uri = request.get_raw_uri()
    return render(request, 'cloakingSite/opener_check_initial.html', {'nbar': 'openercheck', 'uri': uri})


def opener_check(request):
    expected_opener = settings.HTTP_SCHEME + '://' + request.get_host() + '/cloakingsite/openercheckinitial'
    return render(request, 'cloakingSite/opener_check.html', {'expected_opener': expected_opener})


def sweetconfirm(request):
    return render(request, 'cloakingSite/sweetconfirm.html', {'nbar': 'sweetconfirm'})


def confirm(request):
    return render(request, 'cloakingSite/confirm.html', {'nbar': 'confirm'})


def beforeunload(request):
    return render(request, 'cloakingSite/beforeunload.html', {'nbar': 'beforeunload'})


def mousemove(request):
    return render(request, 'cloakingSite/mousemove.html', {'nbar': 'mousemove'})


def webcam_microphone_access_check(request):
    return render(request, 'cloakingSite/webcam_microphone_access.html', {'nbar': 'webcammicrophoneaccess'})


def notification(request):
    return render(request, 'cloakingSite/notification.html', {'nbar': 'notification'})


def geo_API(request):
    return render(request, 'cloakingSite/geolocation_API.html', {'nbar': 'geoAPI'})