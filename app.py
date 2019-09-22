import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///<enterdatabasename>.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
<tableref> = Base.classes.<tablename>

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

@app.route("/county")
def names():
    """Return a list of county names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(<countylist>).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    #return jsonify(list(df.columns)[2:])

@app.route("/plant")
def names():
    """Return a list of plant names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(<plants>).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    #return jsonify(list(df.columns)[2:])

@app.route("/<plant>/<year>/<month>")
def names():
    """Return a list of plant names."""
    countylist
    plantlist
    <plant>/<year>/<month>