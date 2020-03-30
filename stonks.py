import sys
import os
import re
from datetime import datetime

import plotly.graph_objects as pgo

from pandas_datareader import data as pdr
import pandas as pd

class tcolors:
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def validate_input(stock_name, stock_start_date, stock_end_date):
    try:
        if (len(re.search("([A-Z]{5})|(([A-Z]{4})(\.[A-Z]|\-[A-Z]|))|(([A-Z]{3})(\.[A-Z]|\-[A-Z]|))|(([A-Z]{2})(\.[A-Z]|\-[A-Z]|))|(([A-Z]{1})(\.[A-Z]|\-[A-Z]|))", stock_name).group()) < 1):
            print('Failed stock name.\n')
            return False
        if (len(re.search("([0-9]{4}-[0-9]{2}-[0-9]{2})", stock_start_date).group()) != 10):
            print('Failed start date.\n')
            return False
        if (len(re.search("([0-9]{4}-[0-9]{2}-[0-9]{2})", stock_end_date).group()) != 10):
            print('Failed end date.\n')
            return False

    except:
        print(tcolors.WARNING + 'Invalid data.\n' + tcolors.END)
        return False
    else:
        print(tcolors.GREEN + 'Data is Valid.\n' + tcolors.END)
        return True

def get_user_input():
    print(tcolors.BLUE + 'Enter data manually.\n' + tcolors.END)
    stock_name = input('Enter stock name (Ex. XYZ): ')
    stock_start_date = input('Enter start date (Ex. 0000-00-00): ')
    stock_end_date = input('Enter end date (Ex. 0000-00-00): ')
    
    if (validate_input(stock_name, stock_start_date, stock_end_date) == False):
        return get_user_input()
    else:
        return [stock_name, stock_start_date, stock_end_date]

# Initialized variables
valid_input = False
user_input = []
stock_name = ""
stock_start_date = ""
stock_end_date = ""
curr_date = datetime.now().strftime('%Y-%m-%d')

print('\nNumber of arguments: ' + str(len(sys.argv)))
print('Today\'s date: ' + curr_date + '\n')

# Validate command line arguments
if (len(sys.argv) == 4):
    stock_name = str(sys.argv[1]).upper()
    stock_start_date = str(sys.argv[2])
    stock_end_date = str(sys.argv[3])

    if (stock_end_date == "today"):
        stock_end_date = curr_date

    valid_input = validate_input(stock_name, stock_start_date, stock_end_date)

# Acquire user data if args are not given or invalid
if (valid_input != True):
    user_input = get_user_input()
else:
    user_input = [stock_name, stock_start_date, stock_end_date]

# Import stock data and save to file
print('Acquiring  data...')
pdr.DataReader(user_input[0], 'yahoo', user_input[1], user_input[2]).to_csv('data/output_' + stock_name + '_' + curr_date + '.csv')
print('Data acquired.\n')

# Example input
# pdr.DataReader('TSLA', 'yahoo', '2017-01-01', '2018-01-01').to_csv('data/output2.csv')

# Read saved csv file
print('Reading csv data...')
stock_csv = pd.read_csv('data/output_' + stock_name + '_' + curr_date + '.csv')
print('Data read success.\n')

# Graph stock data using Plotly
fig = pgo.Figure(data=[pgo.Candlestick(x=stock_csv['Date'],
    open=stock_csv['Open'],
    high=stock_csv['High'],
    low=stock_csv['Low'],
    close=stock_csv['Close'])
])

# print('Close Data: ' + stock_csv['Close'])

# Bollinger Calculations
# rolling_avg = stock_csv['Close'].rolling(window=20).mean()
# std_dev = stock_csv['Close'].rolling(window=20).std()

# upper_band = rolling_avg + (2 * std_dev)
# lower_band = rolling_avg - (2 * std_dev)

# print('Rolling Average: ' + rolling_avg)

# print('Standard Deviation ' + std_dev)

# print('Upper Band: ' + upper_band)
# print('Lower Band: ' + lower_band)

'''
fig.add_trace(
    pgo.Figure(x=upper_band, name='Upper Band')
)

fig.update_layout(
    title="Stock Data for " + stock_name,
    xaxis_title="Date",
    yaxis_title="Value"
)
'''

print('Launching graph...')
fig.show()
print('Graph launch success.\n')

# Save graph as png
print('Saving graph to file \'images/graph.png\'...')
fig.write_image('images/graph_' + stock_name + '_' + curr_date + '.png')
print('Graph saved to file.\n')

print('Done.')
