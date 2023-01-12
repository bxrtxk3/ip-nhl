import pandas as pd
import re
from termcolor import colored as color

season = input("Pick a season (e.g. '20222023'): ")
season = season if season != '' else '20222023'

try:
    df = pd.read_csv('csv/hockey_players_{}.csv'.format(season))
except:
    season = '20222023'
    df = pd.read_csv('csv/hockey_players_{}.csv'.format(season))

string = input("Search for (phrase): ")

df = df.where(df["Full Name"].str.contains(string, flags=re.IGNORECASE, regex=True)
              | df["Club"].str.contains(string, flags=re.IGNORECASE, regex=True))

df = df.dropna()

print("\nSort parameters:")
print("- Goals")
print("- Games")
print("- goalAvg\n")

sortby = input("Sort by (case sensitive!): ")

try:
    df.sort_values(by=sortby, ascending=False, inplace=True)
except:
    df.sort_values(by="Goals", ascending=False, inplace=True)

df.reset_index(drop=True, inplace=True)

print("\n", df, "\n")

player_index = int(input("Player index: "))
player_goalAvg = df.iloc[player_index]['goalAvg']
player_name = df.iloc[player_index]['Full Name']
implied_odds_yes = float(input("Will score (odds): "))
implied_odds_no = float(input("Will not score (odds): "))
implied_probability_yes = 100 / implied_odds_yes
implied_probability_no = 100 / implied_odds_no
true_probability_yes = round(player_goalAvg * 100 / 2, 2)
true_probability_no = 100 - true_probability_yes
true_odds_yes = round(100 / true_probability_yes, 2)
true_odds_no = round(100 / true_probability_no, 2)
print("\n\n----- Scoring a goal by", player_name, "({} goal average) -----\n\nYES:".format(player_goalAvg), "\n\nImplied odds are:", implied_odds_yes, "(", round(implied_probability_yes,
      2), "%).", "\nTrue odds are:", true_odds_yes, "(", true_probability_yes, "%).\n\nIs Value Bet:", "{}\nMargin: ~{}{}".format(color("YES", 'green'), color(int(100 * round(implied_odds_yes / true_odds_yes, 2) - 100), 'green'), color("%", "green")) if (true_odds_yes < implied_odds_yes) else color("NO", "red"), "\n\n--------------------------------------------------------------\n\nNO:", "\n\nImplied odds are:", implied_odds_no, "(", round(implied_probability_no,
      2), "%).", "\nTrue odds are:", true_odds_no, "(", true_probability_no, "%).\n\nIs Value Bet:", "{}\nMargin: ~{}{}".format(color("YES", 'green'), color(int(100 * round(implied_odds_no / true_odds_no, 2) - 100), 'green'), color("%", "green")) if (true_odds_no < implied_odds_no) else color("NO", "red"))
