import sys
# sys.path.append('/yfinance')

import os

import yfinance as yf

from pandas_datareader import data as pdr

tsla = yf.Ticker("TSLA")
yf.pdr_override()

f = open("output.json", "a")
f.write("tsla.major_holders")
f.close()

print "Done."

# os.system("fx %s" % (tsla.info))

# print tsla.earnings
