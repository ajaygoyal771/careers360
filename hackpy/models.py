# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.urlresolvers import reverse
from django_comments.models import Comment
import datetime

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    bio = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)

class LinkVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCountManager, self).get_query_set().annotate(
                votes=Count('vote')).order_by('-votes')

class Link(models.Model):
    title = models.CharField("Headline",max_length=100)
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    rank_score = models.FloatField(default=0.0)
    url = models.URLField("URL",max_length=250,blank=True)
    description = models.TextField(blank=True)
    with_votes = LinkVoteCountManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": str(self.id)})

def create_link(title,submitter,url,description='',submitted_on=datetime.datetime.now(),rank_score=0):
    Link.objects.create(title=title,submitter=submitter,submitted_on=submitted_on,rank_score=rank_score,url=url,description=description)

def create_user(username):
    if User.objects.filter(username=username):
        return User.objects.filter(username=username)[0]
    user = User.objects.create_user(username=username,
                                 email='jlennon@beatles.com',
                                 password='glass onion')
    return user

class Vote(models.Model):
    voter = models.ForeignKey(User)
    link =models.ForeignKey(Link)

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.link.title)