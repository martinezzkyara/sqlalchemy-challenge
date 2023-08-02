# Import the dependencies.

from flask import Flask  # dont need to use jsonify because im using pandas to read my query, load in the data into a df, and convert it to a json object
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# '/'


@app.route('/')
def home():
    return (
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


# '/api/v1.0/precipitation'
@app.route("/api/v1.0/precipitation")
def precipitation():
    res = pd.read_sql(
        text("SELECT date, prcp FROM measurement WHERE date <= '2017-08-23' AND date >= '2016-08-23' "), connection)
    return res.to_json(orient='records')

# '/api/v1.0/stations'


@app.route("/api/v1.0/stations")
def stations():
    res = pd.read_sql(
        text("SELECT station FROM station"), connection)
    return res.to_json()

# '/api/v1.0/tobs'


@ app.route("/api/v1.0/tobs")
def tobs():
    res = pd.read_sql(
        text("SELECT m.date, m.tobs FROM measurement AS m WHERE m.station LIKE 'USC00519281' AND (m.date <= '2017-08-23' AND m.date >= '2016-08-23') "), connection)
    return res.to_json(orient='records')

# '/api/v1.0/<start>'


@ app.route("/api/v1.0/<start>")
def start(start):
    query_front = "SELECT m.tobs FROM measurement AS m WHERE m.date >= '"
    total_query = query_front + start + "'"
    df = pd.read_sql(
        text(total_query), connection)

    stats_df = df.describe().transpose()
    min_max_avg_df = stats_df[['min', 'max', 'mean']]

    return min_max_avg_df.to_json(orient='records')

# '/api/v1.0/<start>/<end>'


@ app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    query_front = "SELECT m.tobs FROM measurement AS m WHERE (m.date >= '"
    query_mid = "' AND m.date <= '"
    query_end = "' )"
    total_query = query_front + start + query_mid + end + query_end
    print(total_query)
    df = pd.read_sql(
        text(total_query), connection)
    print(df)

    stats_df = df.describe().transpose()
    min_max_avg_df = stats_df[['min', 'max', 'mean']]

    return min_max_avg_df.to_json(orient='records')


if __name__ == "__main__":
    app.run(debug=True)
