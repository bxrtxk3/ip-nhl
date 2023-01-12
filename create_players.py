import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
from progress import percentageProgress
import shutil
import time
import os

season = input("Pick a season (e.g. '20222023'): ")
season = season if season != '' else '20222023'

team_roster = "https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster"

response = urlopen(url=team_roster)

data_json = json.loads(response.read())

player_link = []
player_name = []
player_club = []
player_goals = []
player_games = []

for i in data_json['teams']:
    for x in i['roster']['roster']:
        player_link.append(x['person']['link'])
        player_name.append(x['person']['fullName'])
        player_club.append(i['name'])


progress = 0

for i in player_link:
    player_info = "https://statsapi.web.nhl.com/{}/stats?stats=statsSingleSeason&season={}".format(
        i, season)
    response = urlopen(url=player_info)
    player_data_json = json.load(response)
    try:
        player_goals.append(
            int(player_data_json['stats'][0]['splits'][0]['stat']['goals']))
        player_games.append(
            int(player_data_json['stats'][0]['splits'][0]['stat']['games']))
    except:
        player_goals.append(np.nan)
        player_games.append(np.nan)
    progress = progress + 1
    percentageProgress(progress, len(
        player_link), "Getting players data from season {}/{}".format(season[:4], season[4:]))
    time.sleep(0.2)

df = pd.DataFrame()

df["Full Name"] = player_name
df["Club"] = player_club
df["Goals"] = player_goals
df["Games"] = player_games
df["goalAvg"] = round(df["Goals"] / df["Games"], 2)

df["Goals"] = df["Goals"].astype('Int64')
df["Games"] = df["Games"].astype('Int64')

df.sort_values(inplace=True, ascending=False, by="Goals")
df = df.dropna()
df.reset_index(drop=True, inplace=True)
df.index = df.index + 1


df.to_csv("hockey_players_{}.csv".format(season), index=False)

print(df.head())

while True:
    ans = input("Move file to /csv ? (y/n): ")
    if ans == 'y':
        try:
            os.remove('csv/' + "hockey_players_{}.csv".format(season))
        except:
            True
        shutil.move("hockey_players_{}.csv".format(season), 'csv')
        break
    if ans == 'n':
        break
