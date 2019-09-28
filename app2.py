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
# Database Setup
#################################################

#try:
#    engine = create_engine("sqlite:///data_farming.db")
#   print("connectedtosqlitedb")
#except expression as identifier:
#    print(identifier)

db_file="db//data_farming.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sql.connect(db_file)
    except Exception as e:
        print(e)
 
    return conn

conn = create_connection(db_file)
cur = conn.cursor()
# reflect an existing database into a new model
#Base = automap_base()
# reflect the tables
#Base.prepare(engine, reflect=True)

# Save reference to the table
#NC_MONTHLY_WEATHER = Base.classes.NC_MONTHLY_WEATHER
#PLANT_CHARACTERISTICS = Base.classes.PLANT_CHARACTERISTICS

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
        cur.execute("select distinct common_name from PLANT_CHARACTERISTICS")

        rows = cur.fetchall()
 
        for row in rows:
            print(row)

        return jsonify(rows)
                
        #con.commit()
        #msg = "Record successfully added"

if __name__ == "__main__":
    app.run()