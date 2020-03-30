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

def set_stock_image(stock_name, start_date, end_date):
    # Initialized variables
    curr_date = datetime.now().strftime('%Y-%m-%d')
    stock_name = stock_name.upper()

    if (isinstance(start_date, int)):
        years = max(1, start_date)
        years = min(50, start_date)
        start_year = int(datetime.now().strftime('%Y')) - years
        start_date = str(start_year) + '-01-01'

    if (end_date == 'today'):
        end_date = curr_date

    print(tcolors.BLUE + 'Stock: ' + stock_name + tcolors.END)
    print(tcolors.BLUE + 'Start: ' + start_date + tcolors.END)
    print(tcolors.BLUE + 'End: ' + end_date + '\n' +  tcolors.END)

    if (validate_input(stock_name, start_date, end_date) == False):
        print('Setting Error Image')
        os.system('cp images/error.png images/graph.png')
    
    else:
        # Import stock data and save to file
        print('Acquiring  data...')
        pdr.DataReader(stock_name, 'yahoo', start_date, end_date).to_csv('data/output_' + stock_name + '_' + curr_date + '.csv')
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

        #print('Launching graph...')
        #fig.show()
        #print('Graph launch success.\n')

        # Save graph as png
        print('Saving graph to file \'images/graph.png\'...')
        fig.write_image('images/graph.png')
        print('Graph saved to file.\n')

        print('Done.')
