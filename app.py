from flask import Flask, render_template, request
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components

app = Flask(__name__)

price_options = ['Close', 'Adjusted close', 'Open', 'Adjusted Open']

@app.route('/')
def index():
    
    code = request.args.get('code')
    if code == None:
        code = 'GOOG'
        
    price = request.args.get('price_option')
    if price == None:
        price = 'Open'
        
    price_search = {'Close': 'close',
             'Adjusted close': 'adj_close',
             'Open': 'open',
             'Adjusted Open': 'adj_open'
            }[price]
        
    api_key = '6LqqHDqZYZX4TaPdPnKR'
    
    quandl = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20170101&date.lt=20171231'
    quandl += '&ticker=' + code
    quandl += '&qopts.columns=date,' + price_search
    quandl += '&api_key=' + api_key
    
    json_file = requests.get(quandl).json()
    df = pd.DataFrame(json_file['datatable']['data'])
    df[0] = pd.DatetimeIndex(df[0])
    source = ColumnDataSource(data = {'0':df[0],'1':df[1]})

    p = figure(title = 'Price for '+ code,
               x_axis_label = 'Date',
               y_axis_label = 'Price ($)',
               x_axis_type = 'datetime'
               )

    p.y_range.start = min(df[1])
    p.y_range.end = max(df[1])

    p.line(x='0',y='1',source=source,color='blue',legend=None)
    script, div = components(p)
    
    return render_template("plot.html", script=script, div=div,
		price_options=price_options, current_code=code, 
         current_selected_price=price)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=33507)
