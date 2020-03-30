import urllib.request

print('Requesting Data')
urllib.request.urlretrieve('http://192.168.220.143:1234/get_stock?ticker=amd', 'images/image.png')


#urllib.request.urlretrieve('https://www.python.org/static/opengraph-icon-200x200.png', 'images/image.png')
print('Retreival Successful')
