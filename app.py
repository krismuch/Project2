import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import sqlite3 as sql
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/plantchoices")
def names():
    """Return a list of distinct plant names."""

    with sql.connect("db//data_farming.db") as con:
        cur = con.cursor()
        cur.execute("select distinct UPPER(common_name) from PLANT_CHARACTERISTICS WHERE common_name is NOT NULL ORDER BY common_name")

        rows = cur.fetchall()
 
        for row in rows:
            print(row)

        return jsonify(rows)

@app.route("/weather/<year_>/<month_>")
def weather(year_, month_):
    """Return a list of distinct plant names."""
    
    with sql.connect("db//data_farming.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT c.county, w.tmax, w.tmin, w.prcp, w.year, w.month-1 as month2 FROM NC_COUNTIES AS c INNER JOIN NC_MONTHLY_WEATHER AS w ON w.FIPS = c.FIPS WHERE year={year_} and month2={month_}")
        
        rows = cur.fetchall()
 
        for row in rows:
            print(row)

        return jsonify(rows)

@app.route("/metadata/<plant>")
def plant_metadata(plant):
    """Return the MetaData for a given plant."""
    print(plant)
    with sql.connect("db//data_farming.db") as con:
        cur = con.cursor()
        plant = plant.replace("'","''")
        cur.execute(f"SELECT common_name, min_temp_deg_f, frost_free_days, min_precip_inches, max_precip_inches, drought_tolerance FROM PLANT_CHARACTERISTICS WHERE UPPER(common_name)='{plant.upper()}'")

        results = cur.fetchall()

    # Create a dictionary entry for each row of metadata information
    plant_metadata = {}
    for result in results:
        plant_metadata["common_name"] = result[0]
        plant_metadata["min_temp_deg_f"] = result[1]
        plant_metadata["frost_free_days"] = result[2]
        plant_metadata["min_precip_inches"] = result[3]
        plant_metadata["max_precip_inches"] = result[4]
        plant_metadata["drought_tolerance"] = result[5]


    print(plant_metadata)
    return jsonify(plant_metadata)

if __name__ == "__main__":
    app.run()