# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index (request):
    return render (request, 'login_registration/index.html')

def success (request):
    return render (request, 'login_registration/success.html')

def register (request):
    errors = User.objects.regValidator(request.POST)

    if errors[0]:
        print '-----> THERE ARE ERRORS IN REGISTRATION FORM', errors
        print '-----> ERRORS[0]:', errors[0]
        print '-----> ERRORS[1]:', errors[1]
        for error in errors[1]:
            messages.error(request, error)
        return redirect ('/')
    else:
        print '-----> NO ERRORS IN REGISTRATION FORM'
        request.session['id']=errors[1]
        print '-----> ERRORS[1]:', errors[1]
        request.session['name']=User.objects.get(id=errors[1]).first_name
        request.session['created_user']=True
        return redirect ('/success/')

def login (request):
    errors = User.objects.logValidator(request.POST)

    if errors[0]:
        print '-----> THERE ARE ERRORS', errors
        for error in errors[1]:
            messages.error(request, error)
        return redirect ('/')
    else:
        print '-----> NO ERRORS'
        request.session['id']=errors[1]
        request.session['name']=User.objects.get(id=errors[1]).first_name
        return redirect ('/success/')

    