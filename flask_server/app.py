import json

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import pandas as pd

app = Flask(__name__)
Bootstrap(app)

def get_temp_humidity():
    df = pd.read_csv('/home/pi/logs/temp_humidity.csv')
   
    df.time = pd.to_datetime(df.time)

    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2, default=str)

    chart_data = df.to_json(orient='records',date_format='iso')

    data = {'chart_data': chart_data}
    return data

@app.route("/")
def index():
    df = pd.read_csv('/home/pi/logs/temp_humidity.csv')
   
    df.time = pd.to_datetime(df.time)

    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2, default=str)

    chart_data = df.to_json(orient='records',date_format='iso')

    data = {'chart_data': chart_data}
    return render_template("index.html", data=data)

@app.route("/bootstrap/")
def bootstrap_index():
    data = get_temp_humidity()
    return render_template("bootstrap_index.html", data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
