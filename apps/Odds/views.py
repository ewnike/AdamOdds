# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect, HttpResponse
from . models import *
import requests
import json, ast
from django.contrib import messages
from django.http import JsonResponse
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
from django.utils import timezone
import re
EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    # code below gets rid of "naive datetime warning but still does not solve timezone problem"
    today = timezone.now()
    tomorrow= today + timedelta(1)
######todays_sched filters expired games out of schedule########
    todays_sched = ScheduleMLB.objects.filter(match_time__date__gte=datetime.date(today))

    context={
        'schedule':ScheduleMLB.objects.all(),
        'odds':OddsMLB.objects.all(),
        'todays_sched': todays_sched,
    }
    # print context['todays_sched']
    schedules_filter = {}
    unique_schedules= []

#######This for loop filters games so games displayed in html are unique and not repeated####
    for schedules in todays_sched:
        key = schedules.api_id_key
        if key not in schedules_filter and len(key.strip()) > 0:
            schedules_filter[key] = True
            unique_schedules.append(schedules)

    context['schedule']=unique_schedules
    return render(request, 'Odds/index.html', context)


def show_odds(request,id):
    game=ScheduleMLB.objects.get(id=id)
    # away_team = ScheduleMLB.objects.filter(game.id = id)
    # print(away_team)
    game_odds=OddsMLB.objects.filter(schedule_id= game.id)
    context = {
        'games': game,
        'game_odds': game_odds,
        'away_team':ScheduleMLB.objects.get(id=id),
        'home_team':ScheduleMLB.objects.get(id=id),
        'match_time':ScheduleMLB.objects.get(id=id),
        'away_pitcher':ScheduleMLB.objects.get(id=id),
        'home_pitcher':ScheduleMLB.objects.get(id=id),
    }

    return render(request, 'Odds/odds.html', context)

def create_bets(request, id):
    game=ScheduleMLB.objects.get(id=id)
    game_odds=OddsMLB.objects.filter(schedule_id= game.id)
    user=User.objects.all()
    context = {
        'user': user,
        'games': game,
        'game_odds': game_odds,
        'away_team':ScheduleMLB.objects.get(id=id),
        'home_team':ScheduleMLB.objects.get(id=id),
        'match_time':ScheduleMLB.objects.get(id=id),
    }

    return render(request, 'Odds/create_bets.html', context)


def login_index(request):
    context = {}
    if 'invalid_login' in request.session:
        request.session.pop('invalid_login')
        context['login_messages'] = True
    elif 'invalid_registration' in request.session:
        request.session.pop('invalid_registration')
        context['registration_messages'] = True

    return render(request, 'Odds/login_index.html', context)

def registrate(request):
    return render(request, "Odds/register.html")


def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/registrate')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/login_index')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    print result.id
    return redirect('/success')

def success(request):
    try:
        request.session['user_id']
        print ['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    print context['user']
    return render(request, 'Odds/success.html', context)

def show_other_bets(request, id):
    # user=User.objects.get(id=id)
    game=ScheduleMLB.objects.get(id=id)
    betslip= BetSlip.objects.filter(event_odds_id=id)
    context={
    # 'users':user,
    'games': game,
    'away_team':ScheduleMLB.objects.get(id=id),
    'home_team':ScheduleMLB.objects.get(id=id),
    'match_time':ScheduleMLB.objects.get(id=id),
    'betslips':betslip,
    'money_line_away':BetSlip.objects.all(),
    'money_line_home':BetSlip.objects.all(),
    'over_line':BetSlip.objects.all(),
    'under_line':BetSlip.objects.all(),
    'point_spread_away_line':BetSlip.objects.all(),
    'point_spread_home_line':BetSlip.objects.all(),
    }

    return render(request, "Odds/show_other_bets.html", context)

def take_other_side(request, id):
    this_betslip= BetSlip.objects.get(id=id)
    this_game = ScheduleMLB.objects.filter(id = this_betslip.event_odds_id)
    this_test = ScheduleMLB.objects.filter(api_id_key = this_betslip.schedule_event_id)
    print(this_betslip.event_odds_id)
    print this_test
    # user=User.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    this_user = User.objects.filter(id = this_betslip.user_id)
    print this_user

    if this_user == user:
        print "hello"
    else:
        context = {
            'user': user,
            # 'game_odds': game_odds,
            'games': this_game,
            'betslips' : this_betslip,
            'test':this_test,
        }

    return render(request,'Odds/take_other_side.html', context)


def validate_proposition(request, id):
    game=ScheduleMLB.objects.get(id=id)
    event_odds=OddsMLB.objects.filter(schedule_id= game.id)
    # schedule_event_id=game.api_id_key

    print game.id

    if request.method == 'POST':
        amount = request.POST['amount']
        schedule_event_id= request.POST['api_id_key']
        print type(schedule_event_id)
        ##Deconstruct tuple created in create_bets.html###
        odds = [value.split('+') for value in request.POST.getlist('odds', None)]
        odds = ast.literal_eval(json.dumps(odds))
        apple = [['money_line_away', '0'], ['money_line_home', '0'], ['over_line', '0'], ['under_line', '0'], ['point_spread_away_line', '0'], ['point_spread_home_line', '0']]
        apple = ast.literal_eval(json.dumps(apple))
        for element in odds:
            if element not in apple:
                apple.append(element)

        #Turn Tuple into a dictionary##
        bet_selection = dict(apple)
        money_line_away = bet_selection["money_line_away"]
        money_line_home =  bet_selection["money_line_home"]
        over_line =  bet_selection["over_line"]
        under_line = bet_selection["under_line"]
        point_spread_away_line =  bet_selection["point_spread_away_line"]
        point_spread_home_line =  bet_selection["point_spread_home_line"]


    betslip = BetSlip.objects.create(amount = amount, money_line_away=money_line_away, money_line_home = money_line_home, over_line = over_line, under_line = under_line, point_spread_away_line = point_spread_away_line, point_spread_home_line=point_spread_home_line, user = User.objects.get(id=request.session['user_id']), event_odds_id=game.id)
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')
