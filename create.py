import pandas as pd
from urllib.request import urlopen
import json
from progress import *
import shutil
import os
from datetime import date, timedelta

if not os.path.exists('./csv'): 
    os.makedirs('./csv')

season = input("Current season (e.g. '20222023'): ")
season = season if season != '' else '20222023'

last = input("How many last seasons would you like to create files for (e.g. '5'): ")
last = last if last != '' else '5'

for x in range(int(last)):
    general = "https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats"
    team_stats = "https://statsapi.web.nhl.com/api/v1/standings?season={}".format(season)

    response = urlopen(url=general)

    data_json = json.loads(response.read())

    nhl = []
    pts = []

    for i in data_json['teams']:
        nhl.append(i['name'])
        pts.append(i['teamStats'][0]['splits'][0]['stat']['pts'])

    response = urlopen(url=team_stats)

    data_json = json.loads(response.read())

    games_played = []
    wins = []
    losses = []
    ot = []
    goals_for = []
    goals_against = []
    win_streak = []
    points = []

    progress = 0

    for i in data_json['records']:
        for x in i['teamRecords']:
            games_played.append(x['gamesPlayed'])
            wins.append(x['leagueRecord']['wins'])
            losses.append(x['leagueRecord']['losses'])
            ot.append(x['leagueRecord']['ot'])
            goals_for.append(x['goalsScored'])
            goals_against.append(x['goalsAgainst'])
            win_streak.append(x['streak']['streakNumber'])
            points.append(x['points'])
        progress = progress + 1
        percentageProgress(progress, len(data_json['records']))

    df_standings = pd.DataFrame()
    df_standings["NHL"] = nhl
    df_standings["Points"] = pts
    df_standings["Points"] = df_standings["Points"].astype('Int64')


    df_team_stats = pd.DataFrame()
    df_team_stats['Games Played'] = games_played
    df_team_stats['Games Played'] = df_team_stats['Games Played'].astype('Int64')
    df_team_stats['Wins'] = wins
    df_team_stats['Wins'] = df_team_stats['Wins'].astype('Int64')
    df_team_stats['Losses'] = losses
    df_team_stats['Losses'] = df_team_stats['Losses'].astype('Int64')
    df_team_stats['Overtime'] = ot
    df_team_stats['Overtime'] = df_team_stats['Overtime'].astype('Int64')
    df_team_stats['Win Ratio'] = round(100 * df_team_stats['Wins'] / df_team_stats['Games Played'], 2)
    df_team_stats['Goals For'] = goals_for
    df_team_stats['Goals For'] = df_team_stats['Goals For'].astype('Int64')
    df_team_stats['Goals Against'] = goals_against
    df_team_stats['Goals Against'] = df_team_stats['Goals Against'].astype('Int64')
    df_team_stats['Goal Differential'] = df_team_stats['Goals For'] - df_team_stats['Goals Against']
    df_team_stats['GF Average'] = round(df_team_stats['Goals For'] / df_team_stats['Games Played'], 2)
    df_team_stats['GA Average'] = round(df_team_stats['Goals Against'] / df_team_stats['Games Played'], 2)
    df_team_stats['GIG Average'] = round((df_team_stats['Goals For'] + df_team_stats['Goals Against']) / df_team_stats['Games Played'], 2)
    df_team_stats['Win Streak'] = win_streak
    df_team_stats['Win Streak'] = df_team_stats['Win Streak'].astype('Int64')

    df_team_stats['Points'] = points
    df_team_stats['Points'] = df_team_stats['Points'].astype('Int64')

    df_standings.sort_values(by="Points", inplace=True, ascending=False)
    df_standings.reset_index(drop=True, inplace=True)

    df_team_stats.sort_values(by="Points", inplace=True, ascending=False)
    df_team_stats = df_team_stats.drop('Points', axis=1)
    df_team_stats.reset_index(drop=True, inplace=True)


    df = pd.concat([df_standings, df_team_stats], axis=1)

    df = df[~df.index.duplicated(keep='first')]

    df.reset_index(drop=True, inplace=True)

    df.to_csv("standings_{}.csv".format(season), index=False)

    try:
        os.remove('csv/' + "standings_{}.csv".format(season))
    except:
        True
    shutil.move("standings_{}.csv".format(season), 'csv')

    schedule = "https://statsapi.web.nhl.com/api/v1/schedule?season={}".format(season)

    response = urlopen(url=schedule)

    data_json = json.loads(response.read())

    away = []
    home = []
    score_away = []
    score_home = []
    mdate = []

    progress = 0

    for i in data_json['dates']:
        match_date = i['date']
        for x in i['games']:
            away.append(x['teams']['away']['team']['name'])
            home.append(x['teams']['home']['team']['name'])
            score_away.append(x['teams']['away']['score'])
            score_home.append(x['teams']['home']['score'])
            mdate.append(match_date)
        progress = progress + 1
        percentageProgress(progress, len(data_json['dates']))

    df = pd.DataFrame()

    df["Date"] = mdate
    df["Home"] = home
    df["HS"] = score_home
    df["AS"] = score_away
    df["Away"] = away

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    df["HS"] = df["HS"].astype(int)
    df["AS"] = df["AS"].astype(int)

    df.to_csv("goals_{}.csv".format(season), index=False)

    try:
        os.remove('csv/' + "goals_{}.csv".format(season))
    except:
        True
    shutil.move("goals_{}.csv".format(season), 'csv')

    df = pd.read_csv('csv/goals_{}.csv'.format(season))
    standings = pd.read_csv('csv/standings_{}.csv'.format(season))

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df["HS"] = df["HS"].astype('Int64')
    df["AS"] = df["AS"].astype('Int64')
    df = df.loc[df["Date"].dt.date < date.today() - timedelta(days = 1)]

    teams = []
    home_wins = []
    away_wins = []

    for index, row in standings.iterrows():
        teams.append(row['NHL'])
        tmp_df1 = df.where(df["Home"].str.contains(row['NHL'])).dropna()
        tmp_df2 = df.where(df["Away"].str.contains(row['NHL'])).dropna()
        hwins = 0
        awins = 0
        for index, row in tmp_df1.iterrows():
            if row["HS"] > row["AS"]:
                hwins += 1
        for index, row in tmp_df2.iterrows():
            if row["HS"] < row["AS"]:
                awins += 1
        home_wins.append(hwins)
        away_wins.append(awins)

    standings['Home Wins'] = home_wins
    standings['Away Wins'] = away_wins
    standings['Home Wins %'] = round(home_wins / (standings['Home Wins'] + standings['Away Wins']) * 100, 2)
    standings['Away Wins %'] = round(away_wins / (standings['Home Wins'] + standings['Away Wins']) * 100, 2)
    standings["Home Wins"] = pd.to_numeric(standings["Home Wins"])
    standings["Away Wins"] = pd.to_numeric(standings["Away Wins"])
    standings["Home Wins %"] = pd.to_numeric(standings["Home Wins %"])
    standings["Away Wins %"] = pd.to_numeric(standings["Away Wins %"])

    standings.reset_index(drop=True, inplace=True)

    standings.to_csv("standings_{}.csv".format(season), index=False)

    try:
        os.remove('csv/' + "standings_{}.csv".format(season))
    except:
        True
    shutil.move("standings_{}.csv".format(season), 'csv')

    season = str(int(season) - 10001)

try:
    os.system('clear')
except:
    os.system('cls')
    
print('\n')