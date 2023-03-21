import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import os
import json

# setup the database password as var
with open(r'C:\Users\alexh\PycharmProjects\fpl_data_pull\pw.json') as f:
    config = json.load(f)
database_password = config['PASSWORDS']['DATABASE_PASSWORD']

def create_initial_column(df, name_column, value_column):
  # Create a new column called 'full_name'
  df['full_name'] = ''

  # Iterate through each row of the dataframe
  for index, row in df.iterrows():
    # Get the first initial of the name
    first_initial = row[name_column][0]
    # Get the value
    value = row[value_column]
    # Join the first initial and the value with a period and assign it to the 'initial' column
    df.at[index, 'full_name'] = f'{first_initial}. {value}'

base_path = r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs'

# Connect to database
conn = psycopg2.connect("dbname='fpl.db.22.23' user='postgres' host='localhost' password=" + database_password)
player_info = pd.read_sql_query('SELECT * FROM "player_info"', con=conn)
player_gw_stats = pd.read_sql_query('SELECT * FROM player_gw_stats', con=conn)
team_info = pd.read_sql_query('SELECT * FROM team_info', con=conn)
# fixture_info = pd.read_sql_query('SELECT * FROM fixture_info WHERE finished = "false"', con=conn)
team_info = pd.read_sql_query('SELECT * FROM team_info', con=conn)
player_gw_stats = player_gw_stats.merge(player_info,
                                        how='inner',
                                        on='player_id')
player_gw_stats = player_gw_stats.merge(team_info,
                                         how='inner',
                                        left_on='team_id',
                                        right_on='team_id')

create_initial_column(player_gw_stats, 'first_name', 'second_name')  

for col in player_gw_stats.columns:
   print(col)

players = player_gw_stats[['player_id']]
players_cutoff = players.max()
players = (int(players_cutoff))

for i in range(1, players):
    # A chart to show the points earned each gw by a player
    # Create df for points scored for each gw
    form = player_gw_stats[['player_id', 'second_name', 'full_name', 'gameweek_id', 'points', 'team_name']]
    # Remove rows where gw is less than the cut off
    form = form[form['player_id'] == i]
    # Get team name
    team = form['team_name'].values[0]
    # Get player name and initial
    player_initial_name = form['full_name'].values[0]
    # Plot df
    form_plt = form.plot(x='gameweek_id', y='points', kind='line')
    # Chart title
    plt.title('Form')
    # x axis label
    plt.xlabel('Gameweek')
    # y axis label
    plt.ylabel('Points')
    # Add labels to bars
    # add_value_labels(form_10_plt)
    # Show chart
    plt.tight_layout()
    path = os.path.join(base_path, team, player_initial_name)
    plt.savefig(path + '\season_form.pdf')
    # plt.show()
    plt.close()
