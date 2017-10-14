# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
import re
import bcrypt
from django.contrib import messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class ScheduleManager(models.Manager):
    def get_or_create(self, api_id_key, away_pitcher,away_team,home_pitcher,home_team,match_time):
        try:
            return ScheduleMLB.objects.get(api_id_key=api_id_key.lower())
        except:
            return ScheduleMLB.objects.create(api_id_key.lower(),away_pitcher,away_team,home_pitcher,home_team,match_time)

# class OddsMLB(models.Manager):
#     def get_or_create(self, schedule, last_updated, money_line_away, money_line_home, odd_type, over_line, point_spread_away,point_spread_away_line,point_spread_home, point_spread_home_line, total_number, under_line):
#         try:
#             return OddsMLB.objects.get(schedule)
class UserManager(models.Manager):
    def validate_login(self, post_data):
        print "I am in the UserManager!!"
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email= post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=  post_data['email'])[0]
            if not bcrypt.checkpw( post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

class ScheduleMLB(models.Model):
    api_id_key=models.CharField(max_length=255)
    away_pitcher=models.CharField(max_length=25)
    away_rot=models.IntegerField()
    away_team=models.CharField(max_length=25)
    home_pitcher=models.CharField(max_length=25)
    home_rot=models.IntegerField()
    home_team=models.CharField(max_length=25)
    match_time=models.DateTimeField(blank = False)

class OddsMLB(models.Model):
    schedule = models.ForeignKey(ScheduleMLB, related_name='odds', null = True, blank = False)
    last_updated=models.DateTimeField(blank=False)
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    odd_type=models.CharField(max_length=25)
    over_line=models.IntegerField()
    point_spread_away=models.DecimalField(decimal_places=3,max_digits=5)
    point_spread_away_line=models.IntegerField()
    point_spread_home=models.DecimalField(decimal_places=3,max_digits=5)
    point_spread_home_line=models.IntegerField()
    total_number=models.DecimalField(decimal_places=3,max_digits=5)
    under_line=models.IntegerField()

class User(models.Model):
    first_name= models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.email

class BetSlip(models.Model):
    schedule_event = models.ForeignKey(ScheduleMLB, related_name = 'event', null= True, blank=True)
    event_odds = models.ForeignKey(OddsMLB, related_name = 'event_odds')
    user=models.ForeignKey(User, related_name="user", default = "user")
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    point_spread_away_line=models.IntegerField()
    point_spread_home_line=models.IntegerField()
    over_line=models.IntegerField()
    under_line=models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
