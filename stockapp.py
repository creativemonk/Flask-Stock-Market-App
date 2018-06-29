import requests
import pandas
import simplejson as json
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session
from bokeh.resources import INLINE



app = Flask(__name__)

app.vars={}


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST', 'GET'])
def graph():
    if request.method == 'POST':
        app.vars['ticker'] = request.form['ticker']
        app.vars['startdate'] = request.form['startdate']
        app.vars['enddate'] = request.form['enddate']
        print(app.vars['startdate'], app.vars['enddate'])

        #api_url = 'https://www.quandl.com/api/v3/datasets/NSE/%s.json?api_key=ENTER API KEY' % app.vars['ticker']
        api_url = 'https://www.quandl.com/api/v3/datasets/NSE/%s.json?column_index=5&api_key=ENTER API KEY&start_date=%s&end_date=%s' % (app.vars['ticker'], app.vars['startdate'], app.vars['enddate']) 
        #api_url = 'https://www.quandl.com/api/v3/datasets/NSE/%s.json?api_key=ENTER API KEY&start_date=%s&end_date=%s' % (app.vars['ticker'], app.vars['startdate'], app.vars['enddate']) 
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
        print(type(raw_data))
        a = raw_data.json()
        print(a)
        df = pandas.DataFrame(a['dataset']['data'])
        print (df)
        
        x1 = df[0].astype('datetime64[D]')
        x2 = df[1]
        print (x1)
        print (x2)
        #output_file("line.html")

        p = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label= 'Date', x_axis_type='datetime',
                y_axis_label= 'Close', plot_width=400, plot_height=400)
            
        p.line(x1, x2, legend= 'Price Movement', line_width = 2, color='red')
        show(p)

        
        
        
        resources = INLINE.render()

        script, div = components(p)
        return render_template('graph.html', script=script, div=div, resources=resources)









if __name__ == '__main__':
    app.run(port=33507, debug =True)
