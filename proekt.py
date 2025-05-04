

import json
import kagglehub  
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler  

path = kagglehub.dataset_download("sumitrodatta/nba-aba-baa-stats")
df = pd.read_csv("Player Totals.csv")

df_tot = df[df['tm'] == 'TOT']
df_non_tot = df[~df['player'].isin(df_tot['player'])]
df_clean = pd.concat([df_tot, df_non_tot])
df_clean = df_clean.drop_duplicates(subset=['season', 'player'], keep='first')

mvp_winners = {
    1980: "Kareem Abdul-Jabbar", 1981: "Julius Erving", 1982: "Moses Malone",
    1983: "Moses Malone", 1984: "Larry Bird", 1985: "Larry Bird",
    1986: "Larry Bird", 1987: "Magic Johnson", 1988: "Michael Jordan",
    1989: "Magic Johnson", 1990: "Magic Johnson", 1991: "Michael Jordan",
    1992: "Michael Jordan", 1993: "Charles Barkley", 1994: "Hakeem Olajuwon",
    1995: "David Robinson", 1996: "Michael Jordan", 1997: "Karl Malone",
    1998: "Michael Jordan", 1999: "Karl Malone", 2000: "Shaquille O'Neal",
    2001: "Allen Iverson", 2002: "Tim Duncan", 2003: "Tim Duncan",
    2004: "Kevin Garnett", 2005: "Steve Nash", 2006: "Steve Nash",
    2007: "Dirk Nowitzki", 2008: "Kobe Bryant", 2009: "LeBron James",
    2010: "LeBron James", 2011: "Derrick Rose", 2012: "LeBron James",
    2013: "LeBron James", 2014: "Kevin Durant", 2015: "Stephen Curry",
    2016: "Stephen Curry", 2017: "Russell Westbrook", 2018: "James Harden",
    2019: "Giannis Antetokounmpo", 2020: "Giannis Antetokounmpo",
    2021: "Nikola Jokic", 2022: "Nikola Jokic", 2023: "Joel Embiid"
}

dpoy_winners = {
    1983: "Sidney Moncrief", 1984: "Sidney Moncrief", 1985: "Mark Eaton", 
    1986: "Alvin Robertson", 1987: "Michael Cooper", 1988: "Michael Jordan", 
    1989: "Dennis Rodman", 1990: "Dennis Rodman", 1991: "David Robinson", 
    1992: "David Robinson", 1993: "Hakeem Olajuwon", 1994: "Hakeem Olajuwon", 
    1995: "Dikembe Mutombo", 1996: "Gary Payton", 1997: "Dikembe Mutombo", 
    1998: "Dikembe Mutombo", 1999: "Alonzo Mourning", 2000: "Alonzo Mourning", 
    2001: "Dikembe Mutombo", 2002: "Ben Wallace", 2003: "Ben Wallace", 
    2004: "Ron Artest", 2005: "Ben Wallace", 2006: "Ben Wallace", 
    2007: "Marcus Camby", 2008: "Kevin Garnett", 2009: "Dwight Howard", 
    2010: "Dwight Howard", 2011: "Dwight Howard", 2012: "Tyson Chandler", 
    2013: "Marc Gasol", 2014: "Joakim Noah", 2015: "Kawhi Leonard", 
    2016: "Kawhi Leonard", 2017: "Draymond Green", 2018: "Rudy Gobert", 
    2019: "Rudy Gobert", 2020: "Giannis Antetokounmpo", 2021: "Rudy Gobert", 
    2022: "Marcus Smart", 2023: "Jaren Jackson Jr."
}

seasons_with_both_awards = set(mvp_winners.keys()).intersection(set(dpoy_winners.keys()))
df_clean = df_clean[df_clean['season'].isin(seasons_with_both_awards)]

mvp_features = ['g', 'gs', 'mp', 'fg', 'fga', 'fg_percent', 'x3p', 'x3pa', 'x3p_percent',
            'x2p', 'x2pa', 'x2p_percent', 'e_fg_percent', 'ft', 'fta', 'ft_percent',
            'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']

dpoy_features = [
    'g', 'gs', 'mp', 'drb', 'trb', 'stl', 'blk', 'pf', 'pts', 'ast', 'orb'
]

df_clean['mpg'] = df_clean['mp'] / df_clean['g'] 
df_clean['bpg'] = df_clean['blk'] / df_clean['g'] 
df_clean['spg'] = df_clean['stl'] / df_clean['g']  
df_clean['rpg'] = df_clean['trb'] / df_clean['g'] 
df_clean['dpg'] = df_clean['drb'] / df_clean['g']  

dpoy_features.extend(['mpg', 'bpg', 'spg', 'rpg', 'dpg'])

df_model = df_clean[['season', 'player', 'tm'] + list(set(mvp_features + dpoy_features))].dropna()

mvp_predictions = []
dpoy_predictions = []

def get_qualified_players(season_df):

    min_games = 41  
    qualified = season_df[season_df['g'] >= min_games].copy()
    return qualified

for season in sorted(df_model['season'].unique()):
    if season not in seasons_with_both_awards:
        continue
        
    season_df = df_model[df_model['season'] == season].copy()
    qualified_players = get_qualified_players(season_df)
    
 
    mvp_scaler = StandardScaler()
    season_df_mvp = qualified_players.copy()
 
    mvp_numeric_features = [f for f in mvp_features if season_df_mvp[f].dtype in [np.int64, np.float64]]
    season_df_mvp[mvp_numeric_features] = mvp_scaler.fit_transform(season_df_mvp[mvp_numeric_features])
 
    season_df_mvp['mvp_score'] = season_df_mvp[mvp_numeric_features].sum(axis=1)
    top_mvp_player = season_df_mvp.sort_values('mvp_score', ascending=False).iloc[0]
    
    mvp_predictions.append({
        'season': int(season),
        'shouldBeMvp': top_mvp_player['player'],
        'actualMvp': mvp_winners[season],
        'match': top_mvp_player['player'] == mvp_winners[season]
    })
 
    dpoy_scaler = StandardScaler()
    season_df_dpoy = qualified_players.copy()
    
    dpoy_numeric_features = [f for f in dpoy_features if season_df_dpoy[f].dtype in [np.int64, np.float64]]
    season_df_dpoy[dpoy_numeric_features] = dpoy_scaler.fit_transform(season_df_dpoy[dpoy_numeric_features])

    season_df_dpoy['defensive_score'] = (
        season_df_dpoy['mpg'] * 0.1 +        
        season_df_dpoy['bpg'] * 2.5 +        
        season_df_dpoy['spg'] * 2.5 +        
        season_df_dpoy['dpg'] * 1.5 +       
        season_df_dpoy['rpg'] * 0.5 -        
        season_df_dpoy['pf'] * 0.5           
    )
    
    top_defensive_player = season_df_dpoy.sort_values('defensive_score', ascending=False).iloc[0]
    
    dpoy_predictions.append({
        'season': int(season),
        'shouldBeDpoy': top_defensive_player['player'],
        'actualDpoy': dpoy_winners[season],
        'match': top_defensive_player['player'] == dpoy_winners[season],
        'score': float(top_defensive_player['defensive_score'])
    })

mvp_correct = sum(p['match'] for p in mvp_predictions)
mvp_total = len(mvp_predictions)
mvp_accuracy = mvp_correct / mvp_total if mvp_total > 0 else 0

dpoy_correct = sum(p['match'] for p in dpoy_predictions)
dpoy_total = len(dpoy_predictions)
dpoy_accuracy = dpoy_correct / dpoy_total if dpoy_total > 0 else 0

mvp_predictions.sort(key=lambda x: x['season'])
dpoy_predictions.sort(key=lambda x: x['season'])

mvp_export_data = {
    'accuracy': mvp_accuracy,
    'totalSeasons': mvp_total,
    'correctPredictions': mvp_correct,
    'predictions': mvp_predictions,
    'features': [
        'Games Played (g)', 'Games Started (gs)', 'Minutes Played (mp)', 
        'Field Goals (fg)', 'Field Goal Attempts (fga)', 'Field Goal Percentage (fg_percent)',
        '3-Point Field Goals (x3p)', '3-Point Field Goal Attempts (x3pa)', 
        '3-Point Field Goal Percentage (x3p_percent)', '2-Point Field Goals (x2p)',
        '2-Point Field Goal Attempts (x2pa)', '2-Point Field Goal Percentage (x2p_percent)',
        'Effective Field Goal Percentage (e_fg_percent)', 'Free Throws (ft)',
        'Free Throw Attempts (fta)', 'Free Throw Percentage (ft_percent)',
        'Offensive Rebounds (orb)', 'Defensive Rebounds (drb)', 'Total Rebounds (trb)',
        'Assists (ast)', 'Steals (stl)', 'Blocks (blk)', 'Turnovers (tov)',
        'Personal Fouls (pf)', 'Points (pts)'
    ]
}
dpoy_export_data = {
    'accuracy': dpoy_accuracy,
    'totalSeasons': dpoy_total,
    'correctPredictions': dpoy_correct,
    'predictions': dpoy_predictions,
    'features': [
        'Games Played (g)', 'Games Started (gs)', 'Minutes Played (mp)',
        'Defensive Rebounds (drb)', 'Total Rebounds (trb)',
        'Steals (stl)', 'Blocks (blk)', 'Personal Fouls (pf)', 'Points (pts)',
        'Minutes Per Game (mpg)', 'Blocks Per Game (bpg)', 'Steals Per Game (spg)',
        'Rebounds Per Game (rpg)', 'Defensive Rebounds Per Game (dpg)'
    ]
}
print("DPOY Predictions:")
for pred in dpoy_predictions:
    print(f"Season: {pred['season']}, Predicted: {pred['shouldBeDpoy']}, Actual: {pred['actualDpoy']}, Match: {pred['match']}")

with open("mvp_predictions_data.json", "w") as file:
    json.dump(mvp_export_data, file, default=str)

with open("dpoy_predictions_data.json", "w") as file:
    json.dump(dpoy_export_data, file, default=str)

print(f"Finished. MVP accuracy: {mvp_accuracy:.2f}, DPOY accuracy: {dpoy_accuracy:.2f}")