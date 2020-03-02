import sys
import os

from pandas_datareader import data as pdr

from termcolor import colored

class tcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

print(tcolors.WARNING + 'Reading data...' + tcolors.ENDC)

# Simple retrieval of stock data and deposit in 'data/output.csv'

stock_data = pdr.get_data_yahoo('SPY', start='2017-01-01', end='2017-04-30')

print(colored('Data retrieved.', 'green'))

f = open('data/output.csv', 'a')
f.write(str(stock_data))
f.close

print ('Done.')
