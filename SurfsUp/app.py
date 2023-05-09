# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify
import numpy as np
import datetime as dt


#################################################
# Database Setup
#################################################

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
# session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available Routes: <br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start_date<br>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Grab most recent date in measurement table
    latest_date = session.execute("SELECT MAX(date) FROM measurement;").fetchall()[0][0]
    # Convert str to datetime object
    datetime_object = dt.datetime.strptime(latest_date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.
    one_year_from_date = datetime_object - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    sql_statement = f"""
    SELECT
        date,
        prcp
    FROM
        measurement
    WHERE
        date BETWEEN '{one_year_from_date}' AND '{latest_date}'
    ORDER BY
        date;
    """

    data = session.execute(sql_statement)
    # session.close() # figure out why this fails

    ytd_data = []
    for date, pcrp in data:
        record_dict = {}
        record_dict['date'] = date
        record_dict['pcrp'] = pcrp
        ytd_data.append(record_dict)
    
    session.close()
    return jsonify(ytd_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    data = session.execute("SELECT station FROM station;").fetchall()
    session.close()
    station_list = list(np.ravel(data))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Find most recent data point in the database for the most active station 
    latest_date = session.execute("""
    SELECT
        MAX(date)
    FROM
        (
        SELECT
            *
        FROM
            measurement
        WHERE
            station = (
            SELECT
                station
            FROM
                (
                SELECT
                    station,
                    MAX(total)
                FROM
                    (
                    SELECT
                        DISTINCT station,
                        COUNT(*) OVER (PARTITION BY station) AS total
                    FROM
                        measurement))));
    """).fetchall()[0][0]

    # Convert str to datetime object
    datetime_object = dt.datetime.strptime(latest_date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.
    one_year_from_date = datetime_object - dt.timedelta(days=365)

    # Design a query to retrieve the last 12 months of precipitation data from the most active station
    sql_statement = f"""
    SELECT
        tobs
    FROM
        measurement
    WHERE
        station = (
        SELECT
            station
        FROM
            (
            SELECT
                station,
                MAX(total)
            FROM
                (
                SELECT
                    DISTINCT station,
                    COUNT(*) OVER (PARTITION BY station) AS total
                FROM
                    measurement)))
        AND Measurement.date BETWEEN '{one_year_from_date}' AND '{latest_date}'
    """
    data = session.execute(sql_statement).fetchall()
    session.close()

    tobs_list = list(np.ravel(data))
    return jsonify(tobs_list)

# http://127.0.0.1:5000/api/v1.0/2010-05-17
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    data = session.execute(f"""
    SELECT MIN(tobs), AVG(tobs), MAX(tobs)  
    FROM measurement
    WHERE date >= '{start}';
    """).fetchall()
    session.close()
    stats_temp = list(np.ravel(data))
    return jsonify(stats_temp)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    data = session.execute(f"""
        SELECT MIN(tobs), AVG(tobs), MAX(tobs) 
        FROM measurement
        WHERE date BETWEEN '{start}' AND '{end}'
        ORDER BY date;
    """).fetchall()
    session.close()
    stats_temp = list(np.ravel(data))
    return jsonify(stats_temp)

if __name__ == "__main__":
    app.run(debug=True)