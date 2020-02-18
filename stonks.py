import sys
# sys.path.append('/yfinance')

import os

import json

import yfinance as yf
yf.pdr_override()

from pandas_datareader import data as pdr

data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")


# tsla = yf.Ticker("TSLA")

# data = tsla.info

'''
f = open("data/output.json", "a")
f.write(json.dumps(str(data)))
f.close()
'''

f = open("data/output.csv", "a")
f.write(str(data))
f.close()

print "Done."

# os.system("fx %s" % (tsla.info))

# print tsla.earnings
