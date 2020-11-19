import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask setup
app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Weather API <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    precip = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['percipitation'] = prcp
        precip.append(prcp_dict)
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    result = session.query(Station.name).all()
    session.close()
    station_list = list(np.ravel(result))
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    temp_result =  session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter((Measurement.date > '2016-08-23'), (Measurement.station == "USC00519281")).all()
    session.close()
    temps = list(np.ravel(temp_result))
    return jsonify(temps)

@app.route('/api/v1.0/<start>')
def one_date(start):
    session = Session(engine)
    prcp_date = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(func.date(Measurement.date) > func.date(start)).group_by(Measurement.date).all()
    session.close()
    start_date = []
    for date, min_temp, max_temp, avg_temp in prcp_date: 
        start_dict = {}
        start_dict['min_temp'] = min_temp
        start_dict['max_temp'] = max_temp
        start_dict['avg_temp'] = avg_temp
        start_dict['date'] = date
        start_date.append(start_dict)
    return jsonify(start_date)

@app.route('/api/v1.0/<start>/<end>')
def two_date(start , end):
    session = Session(engine)
    temp_date = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(func.date(Measurement.date) > func.date(start)).filter(func.date(Measurement.date) <= func.date(end)).\
            group_by(Measurement.date).all()
    session.close()
    end_date = []
    for date, min_temp, max_temp, avg_temp in temp_date: 
        end_dict = {}
        end_dict['min_temp'] = min_temp
        end_dict['max_temp'] = max_temp
        end_dict['avg_temp'] = avg_temp
        end_dict['date'] = date
        end_date.append(end_dict)
    return jsonify(end_date)

if __name__ == '__main__':
    app.run(debug=True)
