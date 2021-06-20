from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect


def index(request):
    return redirect('/cloakingsite')