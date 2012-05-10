#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by Valder Gallo on 2012-05-05.
Copyright (c) 2012 valdergallo. All rights reserved.
"""

from django.contrib import admin
from twitterbeat.models import Tweet, Account, ConnectionError

admin.site.register(Tweet)
admin.site.register(Account)
admin.site.register(ConnectionError)