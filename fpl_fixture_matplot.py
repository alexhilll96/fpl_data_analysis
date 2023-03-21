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

# Connect to database
conn = psycopg2.connect("dbname='fpl.db.22.23' user='postgres' host='localhost' password=" + database_password)
fixture_info = pd.read_sql_query('SELECT * FROM fixture_info WHERE finished = false', con=conn)
team_info = pd.read_sql_query('SELECT * FROM team_info', con=conn)
fixture_info = fixture_info[['gameweek_id', 'home_team_id', 'away_team_id', 'team_h_difficulty', 'team_a_difficulty']]
save_path = r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs'


for x in range(1, 21):
    df1 = fixture_info[(fixture_info['home_team_id'] == x) | (fixture_info['away_team_id'] == x)] 
    df1['difficulty'] = np.where(df1['home_team_id'] == x, df1['team_h_difficulty'], df1['team_a_difficulty'])
    df1['opponent'] = np.where(df1['home_team_id'] == x, df1['away_team_id'], df1['home_team_id'])
    df1['H/A'] = np.where(df1['home_team_id'] == x, 'H', 'A')
    df1['team_id'] = x
    df1 = team_info.merge(df1,
                            how='inner',
                            left_on='team_id',
                            right_on='team_id')
    df1 = team_info.merge(df1,
                            how='inner',
                            left_on='team_id',
                            right_on='opponent')
    

    df1['opponent'] = df1['team_name_x']
    df1 = df1[['gameweek_id', 'team_name_y', 'difficulty', 'H/A', 'opponent']]
    team_name = df1['team_name_y'].values[0]
    team_path = os.path.join(save_path, team_name)
    df1_plt = df1.plot(x='opponent', y='difficulty', kind='line')
    plt.title(team_name)
    plt.ylabel('Difficulty')
    plt.tight_layout()
    plt.savefig(team_path + '\ ' + team_name + '_fixture_dificulty.pdf')
