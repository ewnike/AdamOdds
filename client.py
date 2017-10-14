import json, requests
from pprint import pprint
import django
from apps.Odds.models import *
import sqlite3

API_BASE = "https://jsonodds.com/api/"
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

DEFAULT_HEADER = {'JsonOdds-API-Key': API_KEY}
ENDPOINT_SCHEDULE="odds/{}"
ENDPOINT_ODDS_BYGAMES = "/odds/bygames"
ENDPOINT_RESULTS_BYLEAGUE = "results/{}"
ENDPOINTS_RESULTS_GETBYEVENTID = "results/getbyeventid/{}"



def get_data(url):
    response = requests.get(url, headers=DEFAULT_HEADER)
    return json.loads(response.text)

def post_data(url, payload):
    response = requests.post(url, headers=DEFAULT_HEADER, data=payload)
    print(response.status_code)
    return json.loads(response.text)

def get_schedule(sport):
    return get_data(API_BASE + ENDPOINT_SCHEDULE.format(sport))

def post_odds(game_id, sport):
    payload= {'GameIDs': game_id, 'sport': sport }
    print("I'm in post_odds!!")
    return post_data(API_BASE + ENDPOINT_ODDS_BYGAMES, payload)

def get_results_byid(game_id):
    return get_data(API_BASE + ENDPOINTS_RESULTS_GETBYEVENTID.format(game_id))

def get_results_sport(sport):
    return get_data(API_BASE + ENDPOINT_RESULTS_BYLEAGUE.format(sport))

def print_sport(sport):
    for schedule in get_schedule(sport):
        schedule_mlb = ScheduleMLB()
        schedule_mlb.api_id_key = schedule['ID']
        schedule_mlb.away_pitcher = schedule['AwayPitcher']
        schedule_mlb.away_rot = int(schedule['AwayROT'])
        schedule_mlb.away_team = schedule['AwayTeam']
        schedule_mlb.home_pitcher = schedule['HomePitcher']
        schedule_mlb.home_rot = int(schedule['HomeROT'])
        schedule_mlb.home_team = schedule['HomeTeam']
        schedule_mlb.match_time = schedule['MatchTime']
        schedule_mlb.save()
        for odds in schedule['Odds']:
            odds_list = post_odds(odds['EventID'], sport)
            for item in odds_list:
                for event_odd in item['Odds']:
                    # print 'EventID:', event_odd['EventID']
                    # print 'LastUpdated:', event_odd['LastUpdated']
                    # print 'MoneyLineAway:', event_odd['MoneyLineAway']
                    # print 'MoneyLineHome:', event_odd['MoneyLineHome']
                    # print 'OddType:', event_odd['OddType']
                    # print 'OverLine:', event_odd['OverLine']
                    # print 'PointSpreadAway:', event_odd['PointSpreadAway']
                    # print 'PointSpreadAwayLine:', event_odd['PointSpreadAwayLine']
                    # print 'PointSpreadHome:', event_odd['PointSpreadHome']
                    # print 'PointSpreadHomeLine:', event_odd['PointSpreadHomeLine']
                    # print 'TotalNumber:', event_odd['TotalNumber']
                    # print 'UnderLine:', event_odd['UnderLine']

                    game_odd = OddsMLB()
                    game_odd.api_event_key = event_odd['EventID']
                    game_odd.last_updated = (event_odd['LastUpdated'])
                    game_odd.money_line_home = int(event_odd['MoneyLineHome'])
                    game_odd.money_line_away = int(event_odd['MoneyLineAway'])
                    game_odd.odd_type = (event_odd['OddType'])
                    game_odd.over_line = int(event_odd['OverLine'])
                    game_odd.point_spread_away =  float(event_odd['PointSpreadAway'])
                    game_odd.point_spread_away_line =  int(event_odd['PointSpreadAwayLine'])
                    game_odd.point_spread_home = float(event_odd['PointSpreadHome'])
                    game_odd.point_spread_home_line = int(event_odd['PointSpreadHomeLine'])
                    game_odd.total_number = float(event_odd['TotalNumber'])
                    game_odd.under_line = int(event_odd['UnderLine'])
                    game_odd.schedule = schedule_mlb
                    game_odd.save()






    print("-----------------------------------")

print_sport('MLB')
# pprint(get_schedule("mlb"))
# pprint(post_odds("cb2946f4-c245-4284-9a70-63144e5bf63c", "mlb" ))
# pprint(get_results_sport("mlb"))
# pprint(get_results_byid("fc659489-1871-4f9e-a8a9-b919c0575bb4"))
