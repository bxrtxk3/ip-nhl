import pandas as pd
from datetime import date, timedelta
import re

season = input("Pick a season (e.g. '20222023'): ")
season = season if season != '' else '20222023'

try:
    df = pd.read_csv('csv/goals_{}.csv'.format(season))
except:
    season = '20222023'
    df = pd.read_csv('csv/goals_{}.csv'.format(season))

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

df = df.loc[df["Date"].dt.date < date.today() - timedelta(days = 1)]

df.reset_index(drop=True, inplace=True)


print("Filter by:")
print("1) Calculate average goals")
print("2) Show team's games")

string = input("Index: ")

if string == '1':
    total_goals = df["HS"].sum() + df["AS"].sum()
    average_goals = round(total_goals / len(df), 2)

    print(df.head())
    print("Statistics for season {}/{}\n".format(season[:4], season[4:]))
    print("Total goals scored:", total_goals, "\nGames played:", len(df), "\nAverage of", average_goals, "per game")
elif string == '2':
    team_name = input("Team: ")

    df = df.where(df["Home"].str.contains(team_name, flags=re.IGNORECASE, regex=True) | df["Away"].str.contains(team_name, flags=re.IGNORECASE, regex=True))
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)
    print(df)
