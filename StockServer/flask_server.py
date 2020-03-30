from flask import Flask
from flask import send_file
from flask import request

import stonks

app = Flask(__name__)

@app.route('/get_stock')
def get_image():
    stock_name = request.args.get('ticker')
   
    print(stock_name)

    #stonks.set_stock_image(stock_name, '2019-01-01', 'today')
    stonks.set_stock_image(stock_name, 1, 'today')
    
    filename = 'images/graph.png'

    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    host_file = open('host_ip.txt', 'r')
    host = str(host_file.read())
    host_file.close()

    port = 1234
    app.run(host=host, port=port)
