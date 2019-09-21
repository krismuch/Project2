import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Plants_Metadata = Base.classes.plant_metadata
Plants = Base.classes.plants


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of plant names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Plants).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<plant>")
def plant_metadata(plant):
    """Return the MetaData for a given plant."""
    sel = [
        Plants_Metadata.common_name,
        Plants_Metadata.min_temp_deg_f,
        Plants_Metadata.frost_free_days,
        Plants_Metadata.min_precip_inches,
        Plants_Metadata.max_precip_inches,
        Plants_Metadata.drought_tolerance,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

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


@app.route("/plants/<plant>")
def plants(plant):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Plants).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the plant number and
    # only keep rows with values above 1
    plant_data = df.loc[df[plant] > 1, ["otu_id", "otu_label", plant]]

    # Sort by plant
    plant_data.sort_values(by=plant, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "otu_ids": plant_data.otu_id.values.tolist(),
        "sample_values": plant_data[sample].values.tolist(),
        "otu_labels": plant_data.otu_label.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
