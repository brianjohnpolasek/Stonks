import sys
import os
import re

import plotly.graph_objects as pgo

from pandas_datareader import data as pdr
import pandas as pd

def validate_input(stock_name, stock_start_date, stock_end_date):
    try:
        if (len(re.search("(([A-Z]{4})(\.[A-Z]|\-[A-Z]|))|(([A-Z]{3})(\.[A-Z]|\-[A-Z]|))|(([A-Z]{2})(\.[A-Z]|\-[A-Z]|))|(([A-Z]{1})(\.[A-Z]|\-[A-Z]|))", stock_name).group()) < 1):
            print('Failed stock name.\n')
            return False
        if (len(re.search("([0-9]{4}-[0-9]{2}-[0-9]{2})", stock_start_date).group()) != 10):
            print('Failed start date.\n')
            return False
        if (len(re.search("([0-9]{4}-[0-9]{2}-[0-9]{2})", stock_end_date).group()) != 10):
            print('Failed end date.\n')
            return False

    except:
        print('Invalid data.\n')
        return False
    else:
        print('Data is Valid.\n')
        return True

def get_user_input():
    print('Enter data manually.\n')
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

print('Number of arguments: ' + str(len(sys.argv)) + '\n')

# Validate command line arguments
if (len(sys.argv) == 4):
    stock_name = str(sys.argv[1])
    stock_start_date = str(sys.argv[2])
    stock_end_date = str(sys.argv[3])

    valid_input = validate_input(stock_name, stock_start_date, stock_end_date)

# Acquire user data if args are not given or invalid
if (valid_input != True):
    user_input = get_user_input()
else:
    user_input = [stock_name, stock_start_date, stock_end_date]

# Import stock data and save to file
print('Reading data...')
pdr.DataReader(user_input[0], 'yahoo', user_input[1], user_input[2]).to_csv('data/output2.csv')
print('Data acquired.\n')

# Example input
# pdr.DataReader('TSLA', 'yahoo', '2017-01-01', '2018-01-01').to_csv('data/output2.csv')

# Read saved csv file
print('Reading csv data...')
stock_csv = pd.read_csv('data/output2.csv')
print('Data read success.\n')

# Graph stock data using Plotly
fig = pgo.Figure(data=[pgo.Candlestick(x=stock_csv['Date'],
    open=stock_csv['Open'],
    high=stock_csv['High'],
    low=stock_csv['Low'],
    close=stock_csv['Close'])
    ])

fig.update_layout(
    title="Stock Data for " + stock_name,
    xaxis_title="Date",
    yaxis_title="Value"
)

print('Launching graph...')
fig.show()
print('Graph launch success.')

# Save graph as png
print('Saving graph to file \'images/graph.png\'...')
fig.write_image('images/graph.png')
print('Graph saved to file.\n')

print('Done.')
