#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Valder Gallo on 2012-05-09.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from twitterbeat.models import Tweet
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        model=Tweet,
    )),
)