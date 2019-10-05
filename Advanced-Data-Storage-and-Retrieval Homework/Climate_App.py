import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)


@app.route("/")
def home():
    
    return (f"Surfs Up API<br/>"
            f"* Please enter one of the available routes:<br/>"
            f"* Where it says :start, enter a start date (YYYY-MM-DD):<br/>"
            f"* Where it says :start/end enter a start and end date (YYYY-MM-DD/YYYY-MM-DD):<br/>"
            f"_________________________________________________________________________<br/>"
            f"1. For a list of measurement that include date and prcp, enter route:"
            f"<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"<br/>"
            f"2. For a list of available stations, enter route:"
            f"<br/>"
            f" /api/v1.0/stations<br/>"
            f"<br/>"
            f"3. For a list of temperature observations, enter route:"
            f"<br/>"
            f"/api/v1.0/tobs<br/>"
            f"<br/>"
            f"4. For a list of min temperature, avg temperature amd max temperature for a given year, enter route:  "
            f"<br/>"
            f"/api/v1.0/:start<br/>"
            f"<br/>"
            f"5.  For a list of min temperature, avg temperature amd max temperature between two dates, enter route:"   
            f"<br/>"
            f"/api/v1.0/:start/end<br/>"
            f"<br/>"
            f"_________________________________________________________________________<br/>"
       
 )

#minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


#-------------------------------------------------------------------------

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= a_year_ago).\
                    order_by(Measurement.date).all()
   
    
    thing_to_jsonify=[]
    for (a,b) in precipitation_data:
        precipitaton_Dict = {a:b}
        thing_to_jsonify.append(precipitaton_Dict)

    return jsonify(thing_to_jsonify)

#-------------------------------------------------------------------------    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_results = session.query(Station.name).all()
    all_stations = list(np.ravel(stations_results))
    return jsonify(all_stations)    


#-------------------------------------------------------------------------
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temp_obs = session.query(Measurement.tobs)\
    .order_by(Measurement.date).all()
    return jsonify(temp_obs)
#-------------------------------------------------------------------------
@app.route("/api/v1.0/<start>")
def start(start):
    
    session = Session(engine)
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  start_date

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

   
    results = session.query(*sel).\
        filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    

#-------------------------------------------------------------------------
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    session = Session(engine)
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date
    
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

   
    results = session.query(*sel).\
        filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)



#-------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
