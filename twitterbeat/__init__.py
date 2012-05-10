#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Valder Gallo on 2012-05-05.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
import threading
import time
import re
import sys
from datetime import datetime

import twitter
import feedparser

from django.conf import settings
from twitterbeat.models import Account, Tweet, ConectionError

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

_Thread = threading.Thread
_Event = threading._Event


class Event(_Event):
    # Event from Celery
    if not hasattr(threading._Event, "is_set"):
        is_set = _Event.isSet


class Thread(_Thread):
    # Thread from Celery
    if not hasattr(_Thread, "is_alive"):  # pragma: no cover
        is_alive = _Thread.isAlive

    if not hasattr(_Thread, "daemon"):    # pragma: no cover
        daemon = property(_Thread.isDaemon, _Thread.setDaemon)

    if not hasattr(_Thread, "name"):      # pragma: no cover
        name = property(_Thread.getName, _Thread.setName)


class TwitterBeat(Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._is_shutdown = Event()
        self._is_stopped = Event()
        self.KeepAlive = True
        self.count_runner = 0
        self.daemon = True
        
        user_id  = getattr(settings, 'TWITTER_USER_ID', 
                            Account.objects.filter(active=True).latest('id').id)
                            
        self.twitter_user = Account.objects.get(id=user_id, active=True)
        self.twitter_rss = 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=%s' \
                       % self.twitter_user.username

    def stop(self):
        self.KeepAlive = False 
        self._is_shutdown.set()
        #self._is_stopped.wait()
        sys.stdout.write('STOOPED \n')
        if self.is_alive():
            sys.stdout.write('IS ALIVE \n')
            self.join(1e100)

    @staticmethod
    def _get_status_id_from_link(link):
        item = re.findall(r'/(\d+)', link)
        if len(item):
            return item.pop()
        else:
            return None
            
    @staticmethod
    def _convert_datetime(created_at_string):
        """Convert string to datetime
        """
        fmt = '%a %b %d %H:%M:%S +0000 %Y' #Tue Apr 26 08:57:55 +0000 2011
        return datetime.strptime(created_at_string, fmt)
        
    def _passe_rss(self):
        """
        In [12]: p.entries[0]
        Out[12]: 
        {'guidislink': True,
         'id': u'http://twitter.com/valdergallo/statuses/198914864721309696',
         'link': u'http://twitter.com/valdergallo/statuses/198914864721309696',
         'links': [{'href': u'http://twitter.com/valdergallo/statuses/198914864721309696',
           'rel': u'alternate',
           'type': u'text/html'}],
         'published': u'Sat, 05 May 2012 23:19:34 +0000',
         'published_parsed': time.struct_time(tm_year=2012, tm_mon=5, tm_mday=5, tm_hour=23, tm_min=19, tm_sec=34, tm_wday=5, tm_yday=126, tm_isdst=0),
         'summary': u'valdergallo: Algu\xe9m \xe9 cliente HSBC para comprar para mim ? - Unisonic Very Special Guest: Gotthard: http://t.co/B5TXnbyg',
         'summary_detail': {'base': u'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=valdergallo',
          'language': None,
          'type': u'text/html',
          'value': u'valdergallo: Algu\xe9m \xe9 cliente HSBC para comprar para mim ? - Unisonic Very Special Guest: Gotthard: http://t.co/B5TXnbyg'},
         'title': u'valdergallo: Algu\xe9m \xe9 cliente HSBC para comprar para mim ? - Unisonic Very Special Guest: Gotthard: http://t.co/B5TXnbyg',
         'title_detail': {'base': u'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=valdergallo',
          'language': None,
          'type': u'text/plain',
          'value': u'valdergallo: Algu\xe9m \xe9 cliente HSBC para comprar para mim ? - Unisonic Very Special Guest: Gotthard: http://t.co/B5TXnbyg'},
         u'twitter_place': u'',
         u'twitter_source': u'<a href="http://twitter.com/tweetbutton" rel="nofollow">Tweet Button</a>'}
        
        #fields
            t.entries[0].published_parsed #created_at
            t.entries[0].link #urls
            t.entries[0].id #id - need parse
            t.entries[0].summary #text
            t.entries[0].title #title
        """
        tweets = feedparser.parse(self.twitter_rss)
        parsed = []
        for tweet in tweets.entries:
            parsed.append({
            'created_at': tweet.published_parsed,
            'link': tweet.link,
            'text': tweet.summary.replace('%s:' % self.twitter_user.username, ''),
            'status_id': self._get_status_id_from_link(tweet.link),
            })
        return parsed
    
    def _parse_tweet(self):
        """
        In [25]: tweets[0].__dict__
        Out[25]: 
        {'_contributors': None,
         '_coordinates': None,
         '_created_at': u'Sat May 05 23:19:34 +0000 2012',
         '_favorited': False,
         '_geo': None,
         '_id': 198914864721309696,
         '_in_reply_to_screen_name': None,
         '_in_reply_to_status_id': None,
         '_in_reply_to_user_id': None,
         '_location': None,
         '_now': None,
         '_place': None,
         '_retweet_count': 0,
         '_retweeted': False,
         '_retweeted_status': None,
         '_source': u'<a href="http://twitter.com/tweetbutton" rel="nofollow">Tweet Button</a>',
         '_text': u'Algu\xe9m \xe9 cliente HSBC para comprar para mim ? - Unisonic Very Special Guest: Gotthard: http://t.co/B5TXnbyg',
         '_truncated': False,
         '_user': <twitter.User at 0x10c321ed0>,
         'hashtags': None,
         'urls': None,
         'user_mentions': None}
        
         #fields 
            tweet.text
            tweet.created_at
            tweet.urls
            tweet.user.name
            tweet.id
        """
        api = twitter.Api()
        try:
            tweets = api.GetUserTimeline(self.twitter_user, count=10)
        except Exception, e:
            ConectionError.objects.create(text=e)

        parsed = []
        for tweet in tweets:
            parsed.append({
            'created_at': self._convert_datetime(tweet.created_at),
            'link': "https://twitter.com/#!/%s/status/%s" % (tweet.user.name, tweet.id),
            'text': tweet.text,
            'status_id': tweet.id,
            })
        return parsed
    
    def run(self):
        sys.stdout.write('Getting Twitter \n')
        shutdown = self._is_shutdown
        tweets = self._parse_tweet()
        
        for tweet in tweets:
            tw , created = Tweet.objects.get_or_create(**tweet)
            if created:
                LogEntry.objects.log_action(
                    user_id         = self.twitter_user.pk, 
                    content_type_id = ContentType.objects.get_for_model(Tweet).pk,
                    object_repr     = 'twitterbeat', 
                    object_id       = tw.pk,
                    action_flag     = ADDITION
                )
            
        time.sleep(60) # 60 seconds
        
        if self.twitter_user.active and self.KeepAlive and not shutdown.is_set():
            self.count_runner += 1
            self.run()
        else:
            self.stop()
            raise SystemExit()


if __name__ == "__main__":
    beat = TwitterBeat()
    beat.start()
