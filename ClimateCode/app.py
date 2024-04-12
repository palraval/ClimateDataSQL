# Imports the dependencies.

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################


# Reflects an existing database into a new model

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflects the tables

Base = automap_base()

Base.prepare(autoload_with = engine)

# Saves references to each table

station = Base.classes.station

measurement = Base.classes.measurement


# Creates session from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# The home page which lists all the possible routes 
@app.route("/")
def home():
    return(f"Welcome to the home page! <br/>"
           
           f"Here are all the available routes: <br/>"
           
           f"/api/v1.0/precipitation <br/>"
           
           f"/api/v1.0/stations <br/>"
           
           f"/api/v1.0/tobs <br/>"
           
           f"/api/v1.0/&lt;start&gt <br/>" 
           
           f"/api/v1.0/&lt;start&gt/&lt;end&gt <br/>")


# Route for precipitation values           
@app.route("/api/v1.0/precipitation")
def precip():

# Finds the most recent date 
    dates = session.query(func.max(measurement.date)).first()
    
    for date in dates:
        recent_date = date

# Creates two empty lists    
    dates = []
    precipitation = []
 

# Calculates the date one year from the last date in data set.

    recent_date = dt.datetime.fromisoformat(recent_date)
    one_year_date = recent_date - dt.timedelta(days = 365)

# Performs a query to retrieve the date and precipitation scores for year-span

    filter1 =  session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_date)


# Saves the query results as a Pandas DataFrame

    for value in filter1:
        dates.append(value[0])
        precipitation.append(value[1])

    
    precipitation_date_dataframe = pd.DataFrame({"dates": dates,
                                             "precipitation": precipitation})

# Sorts the dataframe by date and removes "NA" values

    precipitation_date_dataframe = precipitation_date_dataframe.sort_values(by = ['dates'])
    precipitation_date_dataframe = precipitation_date_dataframe.dropna(subset=["precipitation"])

#Converts the dataframe to a dictionary

    precipitation_dictionary = dict(precipitation_date_dataframe.values)
    

    return jsonify(precipitation_dictionary)


# Route for station values
@app.route("/api/v1.0/stations")
def station():

# Creates empty list 
    station_list = []

# Finds all the stations
    station_query = session.query(measurement.station)

# Places each station in a list
    for station in station_query:
        station_list.append(station[0])

# Creates a dictionary from the list of stations
    station_dictionary = {"stations": station_list}

# Returns a JSON list
    return jsonify(station_dictionary)


# Route for temperature values
@app.route("/api/v1.0/tobs")
def month():
    
# Queries all the temperature and date values
    all_temp = session.query(measurement.tobs, measurement.date)

# Filters for only the most-active station
    all_temp = all_temp.filter(measurement.station == "USC00519281")

# Finds the final date for this station 
    all_temps = all_temp.order_by(measurement.date.desc()).first()

    final_date = all_temps[1]    

# Converts the final date into a datetime format

    final_date = dt.datetime.fromisoformat(final_date)


# Finds the date for the year prior and converts it to string

    first_date = final_date - dt.timedelta(days = 365)

    first_date = first_date.strftime("%Y-%m-%d")

# Filters only for the date and temperature values that within the past year from the final date     
    first_date_filter = all_temp.filter(measurement.date >= first_date).all()


# Puts all the temperatures of the most active station into a dictionary

    dict = {}
    for temp in first_date_filter:
        dict[temp[1]] = temp[0]

# Makes a JSON list   
    return jsonify(dict)


# Route for the temperature statistics based on the start value only
@app.route("/api/v1.0/<start>")
def start(start):
# Creates empty dictionary
    start_date_temp_values = {}

# Calculates the minimum, maximum, and average for temperatures associated with dates after the date provided
    date_temperature = session.query(func.min(measurement.tobs), func.max(measurement.tobs), 
                                    func.avg(measurement.tobs)).filter(measurement.date >= start).all()

# Stores the minimum, maximum, and average values in the dictionary
    for summary_statistic in date_temperature:
        TMIN = summary_statistic[0]
        start_date_temp_values['TMIN'] = TMIN
        TMAX = summary_statistic[1]
        start_date_temp_values['TMAX'] = TMAX
        TMEAN = summary_statistic[2]
        start_date_temp_values['TMEAN'] = TMEAN

# Returns a JSON list based on the created dictionary
    return jsonify(start_date_temp_values)



# Route for the temperature statistics based on the start and end values
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
# Calculates the minimum, maximum, and average for temperatures associated with the range of dates provided 
    start_end_filter = session.query(func.min(measurement.tobs), func.max(measurement.tobs), 
                        func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end)

# Creates empty dictionary
    start_end_temp_values = {}
# Stores the minimum, maximum, and average values in the dictionary
    for calculation in start_end_filter:
        TMIN = calculation[0]
        start_end_temp_values['TMIN'] = TMIN
        TMAX = calculation[1]
        start_end_temp_values['TMAX'] = TMAX
        TMEAN = calculation[2]
        start_end_temp_values['TMEAN'] = TMEAN
# Returns a JSON list for the dictionary
    return jsonify(start_end_temp_values)

        
        

# Opens the server  
if __name__  == "__main__":
    app.run(debug = True)