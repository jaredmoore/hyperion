import json

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import pandas as pd

temp_humidity_df = ""

def update_temp_humidity():
    # Run this function periodically and keep data persistent.
    global temp_humidity_df
    
    temp_humidity_df = pd.read_csv('/home/pi/logs/temp_humidity.csv')
   
    temp_humidity_df.time = pd.to_datetime(temp_humidity_df.time)

def get_temp_humidity():
    global temp_humidity_df
    
    #chart_data = temp_humidity_df.to_dict(orient='records')
    #chart_data = json.dumps(chart_data, indent=2, default=str)

    chart_data = temp_humidity_df.to_json(orient='records',date_format='iso')

    data = {'chart_data': chart_data}
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
