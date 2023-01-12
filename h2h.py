import pandas as pd
from datetime import date, timedelta
import re
import os
from IPython.display import clear_output
from termcolor import colored

season = input("Current season (e.g. '20222023'): ")
season = season if season != '' else '20222023'

tmp_season = season
df = pd.DataFrame()

last = input("How many last seasons would you like to include in H2H statistics (e.g. '1'): ")
last = last if last != '' else '1'

print('Collecting data from seasons:')

for x in range(int(last)):
    try:
        tmp = pd.read_csv(f'csv/goals_{tmp_season}.csv')
        df = pd.concat([df, tmp])
        print('- {}/{}'.format(tmp_season[:4], tmp_season[4:]))
    except:
        break
    tmp_season = str(int(tmp_season) - 10001)


df["HS"] = df["HS"].astype('Int64')
df["AS"] = df["AS"].astype('Int64')

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

df = df.loc[df["Date"].dt.date < date.today() - timedelta(days = 1)]

team1 = input("Team 1: ")
team2 = input("Team 2: ")

standings = pd.read_csv('csv/standings_{}.csv'.format(season))

team1_df = standings.where(standings["NHL"].str.contains(team1, flags=re.IGNORECASE, regex=True))
team2_df = standings.where(standings["NHL"].str.contains(team2, flags=re.IGNORECASE, regex=True))
team1_df = team1_df.dropna()
team2_df = team2_df.dropna()
team1_pos = team1_df.index[0] + 1
team2_pos = team2_df.index[0] + 1
team1 = team1_df.iloc[0]["NHL"]
team2 = team2_df.iloc[0]["NHL"]

df = df.sort_values(by="Date", ascending=False)
df = df.where((df["Home"].str.contains(team1, flags=re.IGNORECASE, regex=True) | df["Away"].str.contains(team1, flags=re.IGNORECASE, regex=True)) & (df["Home"].str.contains(team2, flags=re.IGNORECASE, regex=True) | df["Away"].str.contains(team2, flags=re.IGNORECASE, regex=True)))
df = df.dropna()
df.reset_index(drop=True, inplace=True)

total_team1_goals = df['HS'].where(df["Home"].str.contains(team1, flags=re.IGNORECASE, regex=True)).sum()
total_team1_goals += df['AS'].where(df["Away"].str.contains(team1, flags=re.IGNORECASE, regex=True)).sum()
total_team2_goals = df['HS'].where(df["Home"].str.contains(team2, flags=re.IGNORECASE, regex=True)).sum()
total_team2_goals += df['AS'].where(df["Away"].str.contains(team2, flags=re.IGNORECASE, regex=True)).sum()

total_team1_wins = 0
total_team2_wins = 0
home_wins = 0
away_wins = 0

for index, row in df.iterrows():
    if row["HS"] > row["AS"]:
        if team1.lower() in row["Home"].lower():
            total_team1_wins += 1
            home_wins += 1
        else:
            total_team2_wins += 1
            home_wins += 1
    else:
        if team1.lower() in row["Home"].lower():
            total_team2_wins += 1
            away_wins += 1
        else :
            total_team1_wins += 1
            away_wins += 1

total_goals = int(total_team1_goals + total_team2_goals)


clear_output()
os.system('clear')

print("\n----- H2H -----\n")
print("- {}".format(team1))
print("- {}\n".format(team2))
print(df)

print("\nStatistics until {}/{}\n".format(season[:4], season[4:]))

print("Current {} position in NHL: {}".format(colored(team1, 'blue'), team1_pos))
print("Current {} position in NHL: {}\n".format(colored(team2, 'red'), team2_pos))

try:
    average_goals = round((total_goals) / len(df), 2)
    print("H2H Total goals scored:", total_goals, "\nH2H Games played:", len(df), "\nH2H Average of", average_goals, "goals per game\n")
    print("H2H avg. {} goals: {}".format(colored(team1, 'blue'), round(total_team1_goals / len(df), 2)))
    print("H2H avg. {} goals: {}".format(colored(team2, 'red'), round(total_team2_goals / len(df), 2)))
    print("H2H {} wins: {}".format(colored(team1, 'blue'), total_team1_wins))
    print("H2H {} wins: {}\n".format(colored(team2, 'red'), total_team2_wins))
    print("H2H Home wins: {}".format(home_wins))
    print("H2H Away wins: {}".format(away_wins))
except:
    print("\nNot enough data")


standings = standings.sort_values(by=['Home Wins %'], ascending=False)
df1 = standings.where(standings["NHL"].str.contains(team1, flags=re.IGNORECASE, regex=True)).dropna()
df2 = standings.where(standings["NHL"].str.contains(team2, flags=re.IGNORECASE, regex=True)).dropna()
df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)

print("\n\n")
print("Points:", colored(df1["NHL"][0], 'blue') if df1["Points"][0] > df2["Points"][0] else colored(df2["NHL"][0], 'red') if df1["Points"][0] < df2["Points"][0] else colored("Equal", 'yellow'))
print("Wins:", colored(df1["NHL"][0], 'blue') if df1["Wins"][0] > df2["Wins"][0] else colored(df2["NHL"][0], 'red') if df1["Wins"][0] < df2["Wins"][0] else colored("Equal", 'yellow'))
print("Losses:", colored(df1["NHL"][0], 'blue') if df1["Losses"][0] < df2["Losses"][0] else colored(df2["NHL"][0], 'red') if df1["Losses"][0] > df2["Losses"][0] else colored("Equal", 'yellow'))
print("Win Ratio:", colored(df1["NHL"][0], 'blue') if df1["Win Ratio"][0] > df2["Win Ratio"][0] else colored(df2["NHL"][0], 'red') if df1["Win Ratio"][0] < df2["Win Ratio"][0] else colored("Equal", 'yellow'))
print("Goals For:", colored(df1["NHL"][0], 'blue') if df1["Goals For"][0] > df2["Goals For"][0] else colored(df2["NHL"][0], 'red') if df1["Goals For"][0] < df2["Goals For"][0] else colored("Equal", 'yellow'))
print("Goals Against:", colored(df1["NHL"][0], 'blue') if df1["Goals Against"][0] < df2["Goals Against"][0] else colored(df2["NHL"][0], 'red') if df1["Goals Against"][0] > df2["Goals Against"][0] else colored("Equal", 'yellow'))
print("Goal Differential:", colored(df1["NHL"][0], 'blue') if df1["Goal Differential"][0] > df2["Goal Differential"][0] else colored(df2["NHL"][0], 'red') if df1["Goal Differential"][0] < df2["Goal Differential"][0] else colored("Equal", 'yellow'))
print("GF Average:", colored(df1["NHL"][0], 'blue') if df1["GF Average"][0] > df2["GF Average"][0] else colored(df2["NHL"][0], 'red') if df1["GF Average"][0] < df2["GF Average"][0] else colored("Equal", 'yellow'))
print("GA Average:", colored(df1["NHL"][0], 'blue') if df1["GA Average"][0] < df2["GA Average"][0] else colored(df2["NHL"][0], 'red') if df1["GA Average"][0] > df2["GA Average"][0] else colored("Equal", 'yellow'))
print("Home Wins:", colored(df1["NHL"][0], 'blue') if df1["Home Wins"][0] > df2["Home Wins"][0] else colored(df2["NHL"][0], 'red') if df1["Home Wins"][0] < df2["Home Wins"][0] else colored("Equal", 'yellow'))
print("Away Wins:", colored(df1["NHL"][0], 'blue') if df1["Away Wins"][0] > df2["Away Wins"][0] else colored(df2["NHL"][0], 'red') if df1["Away Wins"][0] < df2["Away Wins"][0] else colored("Equal", 'yellow'))
print("Home Wins %:", colored(df1["NHL"][0], 'blue') if df1["Home Wins %"][0] > df2["Home Wins %"][0] else colored(df2["NHL"][0], 'red') if df1["Home Wins %"][0] < df2["Home Wins %"][0] else colored("Equal", 'yellow'))
print("Away Wins %:", colored(df1["NHL"][0], 'blue') if df1["Away Wins %"][0] > df2["Away Wins %"][0] else colored(df2["NHL"][0], 'red') if df1["Away Wins %"][0] < df2["Away Wins %"][0] else colored("Equal", 'yellow'))