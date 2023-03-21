import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import json

# setup the database password as var
with open(r'C:\Users\alexh\PycharmProjects\fpl_data_pull\pw.json') as f:
    config = json.load(f)
database_password = config['PASSWORDS']['DATABASE_PASSWORD']

# function to add value labels
def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.

# Connect to database
conn = psycopg2.connect("dbname='fpl.db.22.23' user='postgres' host='localhost' password=" + database_password)
player_info = pd.read_sql_query('SELECT * FROM "player_info"', con=conn)
player_gw_stats = pd.read_sql_query('SELECT * FROM player_gw_stats', con=conn)
# fixture_info = pd.read_sql_query('SELECT * FROM fixture_info WHERE finished = "false"', con=conn)
team_info = pd.read_sql_query('SELECT * FROM team_info', con=conn)
player_gw_stats = player_gw_stats.merge(player_info,
                                        how='inner',
                                        on='player_id')

# A chart to show the total number of goals scored of the top 10 goalscorers
# Create df for goals scored
goals = player_info[['second_name', 'goals_scored']]
# sort df from largest to smallest
goals = goals.sort_values(by=['goals_scored'], ascending=False)
# Reduce df to top 10
goals = goals.head(10)
# Plot df
goals_plt = goals.plot(x='second_name', y='goals_scored', kind='bar')
# Chart title
plt.title('Top Goal Scorers')
# x axis label
plt.xlabel('Players')
# y axis label
plt.ylabel('Goals Scored')
# Add labels to the bar chart
add_value_labels(goals_plt)
# Format the chart to show all labels
plt.tight_layout()
# Save chart
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\goals.pdf')
# plt.show()


# A chart to show the total number of assists provided of the top 10 assistants
# Create df for assists
assists = player_info[['second_name', 'assists']]
# Sort dataframe greatest to smallest
assists = assists.sort_values(by=['assists'], ascending=False)
# Reduce df to top 10
assists = assists.head(10)
# Plot df
assists_plt = assists.plot(x='second_name', y='assists', kind='bar')
# Chart title
plt.title('Top Assists')
# x axis label
plt.xlabel('Players')
# y label
plt.ylabel('Assists')
# Add lables to the bars
add_value_labels(assists_plt)
# Show chart
plt.tight_layout()
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\assists.pdf')
# plt.show()

# A chart to show the average number of points scored over the previous 5 games
# Create df for points scored for each gw
form_10 = player_gw_stats[['player_id', 'second_name', 'gameweek_id', 'points']]
# Create df for all gw
gw = player_gw_stats[['gameweek_id']]
# Create cutoff by subtracting 10 from total number of gameweeks
cutoff = gw.max() - 10
# Remove rows where gw is less than the cut off
form_10 = form_10[form_10['gameweek_id'] > int(cutoff)]
# Sum all points for each player and transpose
form_10_sum = form_10.groupby('second_name')['points'].sum().T
# Convert series to df
form_10_sum = form_10_sum.to_frame()
# Set df index to column named second_name
form_10_sum['second_name'] = form_10_sum.index
# Divide total points over the last 10 games by 10 provide an average
form_10_sum['form_10'] = form_10_sum['points'] / 10
# Sort df from largest to smallest
form_10_sum = form_10_sum.sort_values(by='points', ascending=False)
#  Reduce df to the top 10
form_10_sum = form_10_sum.head(10)
# Plot df
form_10_plt = form_10_sum.plot(x='second_name', y='form_10', kind='bar')
# Chart title
plt.title('Form Over Previous 10')
# x axis label
plt.xlabel('Average Points')
# y axis label
plt.ylabel('Player')
# Add labels to bars
add_value_labels(form_10_plt)
# Show chart
plt.tight_layout()
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\form_10.pdf')
# plt.show()


# A chart to show the average number of points scored over the previous 5 games
# Create df for points scored for each gw
form_5 = player_gw_stats[['player_id', 'second_name', 'gameweek_id', 'points']]
# Create df for all gw
gw = player_gw_stats[['gameweek_id']]
# Create cutoff by subtracting 5 from total number of gameweeks
cutoff = gw.max() - 5
# Remove rows where gw is less than the cut off
form_5 = form_5[form_5['gameweek_id'] > int(cutoff)]
# Sum all points for each player and transpose
form_5_sum = form_5.groupby('second_name')['points'].sum().T
# Convert series to df
form_5_sum = form_5_sum.to_frame()
# Set df index to column named second_name
form_5_sum['second_name'] = form_5_sum.index
# Divide total points over the last 5 games by 5 to provide an average
form_5_sum['form_5'] = form_5_sum['points'] / 5
# Sort df from largest to smallest
form_5_sum = form_5_sum.sort_values(by='points', ascending=False)
#  Reduce df to the top 10
form_5_sum = form_5_sum.head(10)
# Plot df
form_5_plt = form_5_sum.plot(x='second_name', y='form_5', kind='bar')
# Chart title
plt.title('Form Over Previous 5')
# x axis label
plt.xlabel('Average Points')
# y axis label
plt.ylabel('Player')
# Add lables to bars
add_value_labels(form_5_plt)
# Show chart
plt.tight_layout()
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\form_5.pdf')
# plt.show()

# A chart to show the average number of points scored over the previous 3 games
# Create df for points scored for each gw
form_3 = player_gw_stats[['player_id', 'second_name', 'gameweek_id', 'points']]
# Create df for all gw
gw = player_gw_stats[['gameweek_id']]
# Create cutoff by subtracting 3 from total number of gameweeks
cutoff = gw.max() - 3
# Remove rows where gw is less than the cut off
form_3 = form_3[form_3['gameweek_id'] > int(cutoff)]
# Sum all points for each player and transpose
form_3_sum = form_3.groupby('second_name')['points'].sum().T
# Convert series to df
form_3_sum = form_3_sum.to_frame()
# Set df index to column named second_name
form_3_sum['second_name'] = form_3_sum.index
# Divide total points over the last 3 games by 3 to provide an average
form_3_sum['form_3'] = form_3_sum['points'] / 3
# Sort df from largest to smallest
form_3_sum = form_3_sum.sort_values(by='points', ascending=False)
#  Reduce df to the top 10
form_3_sum = form_3_sum.head(10)
# Plot df
form_3_plt = form_3_sum.plot(x='second_name', y='form_3', kind='bar')
# Chart title
plt.title('Form Over Previous 3')
# x axis label
plt.xlabel('Average Points')
# y axis label
plt.ylabel('Player')
# Add lables to bars
add_value_labels(form_3_plt)
# Show chart
plt.tight_layout()
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\form_3.pdf')
# plt.show()

# A chart to show the average number of points scored over the previous 3 games
# Create df for points scored for each gw
points = player_gw_stats[['player_id', 'second_name', 'gameweek_id', 'points']]
# Create df for all gw
gw = player_gw_stats[['gameweek_id']]
# Sum all points by group by player id
total_points = points.groupby('player_id')['points'].sum().T
# Convert series to df
total_points = total_points.to_frame()

total_points = total_points.sort_values(by='points', ascending=False)
#  Reduce df to the top 10
total_points = total_points.head(20)
# Set df index to column named second_name
# total_points['player_id'] = total_points.index
points = total_points.merge(points,
                            how='inner',
                            left_on='player_id',
                            right_on='player_id')
points = points[['second_name', 'points_x']]
points.drop_duplicates(inplace=True, ignore_index=True)
points_plt = points.plot(x='second_name', y='points_x', kind='bar')
plt.title('Top Scoring FPL Assets')
plt.xlabel('Total Points')
plt.ylabel('Player')
add_value_labels(points_plt)
plt.tight_layout()
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\total_player_points.pdf')
# plt.show()

# A chart to show the top transfered in players
# Create a df for the transfers in for recent gw
transfers_in = player_gw_stats[['player_id', 'second_name', 'gameweek_id', 'transfers_in_x']]
# Create a df for all gws
gw = player_gw_stats[['gameweek_id']]
# Get the current gw
current_gw = gw.max()
# Filter df to only the current gw
transfers_in = transfers_in[transfers_in['gameweek_id'] == int(current_gw)]
# Sort df from most transfered in to least transfered in
transfers_in = transfers_in.sort_values(by=['transfers_in_x'], ascending=False)
# Reduce to the top 20
transfers_in = transfers_in.head(20)
# Plot df
transfers_in_plt = transfers_in.plot(x='second_name', y='transfers_in_x', kind='bar')
# Chart title
plt.title('Most Transfered In')
# x axis label
plt.xlabel('Players')
# y axis label
plt.ylabel('Transfers In')
# Format the chart to show all labels
plt.tight_layout()
# Save chart
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\transfers_in.pdf')
# plt.show()

# A chart to show the top transfered out players
# Create a df for the transfers out for recent gw
transfers_out = player_gw_stats[['player_id', 'second_name', 'gameweek_id', 'transfers_out_x']]
# Create a df for all gws
gw = player_gw_stats[['gameweek_id']]
# Get the current gw
current_gw = gw.max()
# Filter df to only the current gw
transfers_out = transfers_out[transfers_out['gameweek_id'] == int(current_gw)]
# Sort df from most transfered out to least transfered in
transfers_out = transfers_out.sort_values(by=['transfers_out_x'], ascending=False)
# Reduce to the top 20
transfers_out = transfers_out.head(20)
# Plot df
transfers_out_plt = transfers_out.plot(x='second_name', y='transfers_out_x', kind='bar')
# Chart title
plt.title('Most Transfered Out')
# x axis label
plt.xlabel('Players')
# y axis label
plt.ylabel('Transfers Out')
# Format the chart to show all labels
plt.tight_layout()
# Save chart
plt.savefig(r'C:\Users\alexh\OneDrive\Documents\Python\FPL Data\Graphs\transfers_out.pdf')
# plt.show()