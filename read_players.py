import pandas as pd
import re

season = input("Pick a season (e.g. '20222023'): ")
season = season if season != '' else '20222023'

try:
    df = pd.read_csv('csv/hockey_players_{}.csv'.format(season))
except:
    season = '20222023'
    df = pd.read_csv('csv/hockey_players_{}.csv'.format(season))

string = input("Search for: ")

df = df.where(df["Full Name"].str.contains(string, flags=re.IGNORECASE, regex=True) | df["Club"].str.contains(string, flags=re.IGNORECASE, regex=True))

df = df.dropna()

df.sort_values(by="Goals", ascending=False, inplace=True)

df.reset_index(drop=True, inplace=True)

print(df)
