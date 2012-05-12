#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Valder Gallo on 2012-05-05.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
from django.db import models


class Tweet(models.Model):
    status_id = models.BigIntegerField()
    text = models.TextField(blank=True)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-status_id',)
        
    def __unicode__(self):
        return self.text


class Account(models.Model):
    username = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.username
        
class ConnectionError(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.text