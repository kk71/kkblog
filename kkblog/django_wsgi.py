#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys
import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' #the django setting module
application = django.core.handlers.wsgi.WSGIHandler()
