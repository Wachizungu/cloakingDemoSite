from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import CaptchaTestForm


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

    return render(request, 'cloakingSite/simpleCaptcha.html', {'form': form, 'captcha_passed': captcha_passed, 'nbar': 'simple_captcha'})
