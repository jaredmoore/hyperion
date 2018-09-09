import json

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import pandas as pd

temp_humidity_df = "" # Keep track of historical data.
last_temp_humidity = "" # Keep track of the last data value recorded.

def update_temp_humidity():
    # Run this function periodically and keep data persistent.
    global temp_humidity_df, last_temp_humidity
    
    temp_humidity_df = pd.read_csv('/home/pi/logs/temp_humidity.csv')
   
    temp_humidity_df.time = pd.to_datetime(temp_humidity_df.time)

    # Get the most recent temp and humidity
    last_temp_humidity = temp_humidity_df.iloc[temp_humidity_df['time'].idxmax()]

def get_temp_humidity():
    global temp_humidity_df, last_temp_humidity
    
    chart_data = temp_humidity_df.to_json(orient='records',date_format='iso')

    data = {'chart_data': chart_data, 'last_data': last_temp_humidity.to_json(date_format='iso')}
    return data

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_temp_humidity,'interval',minutes=10)
sched.start()

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
@app.route("/bootstrap/")
def bootstrap_index():
    data = get_temp_humidity()
    return render_template("bootstrap_index.html", data=data)

if __name__ == "__main__":
    # Run the first request for data.
    update_temp_humidity()
    app.run(host='0.0.0.0')
