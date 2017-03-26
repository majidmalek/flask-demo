from flask import Flask, render_template, request, redirect
import quandl
import os
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import output_notebook
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.embed import components
from datetime import datetime

# read qualdl API key from file
#api_file = open('quandl_api_key','r')
# read first 20 characters to avoid reading newline character
#quandl.ApiConfig.api_key = api_file.read(20)

# store API key in Heroku environment variable
quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    # it is a POST

    # basic error handling if no ticker or invalid ticker entered: blank plot will display
    if len(request.form['ticker']) == 0:
      app.vars['ticker'] = 'NO TICKER SYMBOL ENTERED'
    else:  
      app.vars['ticker'] = request.form['ticker']

    # error handling for dates
    # quandl gracefully handles dates that are before or after the data set by truncating the response
    # probably a more graceful way to do it than brute forcing past and future dates in
    if len(request.form['start_date']) == 0:
      app.vars['start_date'] = '1800-01-01'
    else:
      app.vars['start_date'] = request.form['start_date']
    if len(request.form['end_date']) == 0: 
      app.vars['end_date'] = '2200-01-01'
    else:      
      app.vars['end_date'] = request.form['end_date']

    # defaulted checkbox to adj_close in index.html to avoid issue if no radio button slected
    app.vars['quote_type'] = request.form['features']

    return redirect('/showGraph')

@app.route('/showGraph')
def showGraph():
    # code to generate graph here

    # assign shome shorter names to user input variables for readability
    ticker = app.vars['ticker']
    start_date = app.vars['start_date'] 
    end_date = app.vars['end_date']
    quote_type = app.vars['quote_type']
    figure_title_string = ticker + ' ' + quote_type

    # fetch data from quandl
    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', quote_type] }, ticker = [ticker], date = { 'gte': start_date, 'lte': end_date})
    x = data['date'].astype(datetime)
    y = data[quote_type]
    p = figure(title=figure_title_string.upper(), x_axis_type='datetime', x_axis_label='Date', y_axis_label=quote_type)
    p.line(x, y, legend=ticker.upper(), line_width=2)

    # code to render HTML with embedded bokeh plot

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'bokeh_template.html',
        ticker=ticker.upper(),
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

if __name__ == '__main__':
  app.run(port=33507,debug=False)

