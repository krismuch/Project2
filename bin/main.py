import sys
sys.path.append("..")

import sqlite3 as sq
import os
import requests
import json

from datetime import datetime
from config.config import db_config, config, NUM_PAGES_TO_EXTRACT

log_list = []
start_date_time = datetime.now().strftime("%d-%B-%Y_%H-%M-%S_%p")
def printf(message, message_type = "INFO", display_on_screen = False):
    dt_string = datetime.now().strftime("%d-%b-%Y %H:%M:%S %p")
    message_to_be_displayed = f"{dt_string} [::{message_type}::]: {message}"
    
    log_list.append(message_to_be_displayed)

    if display_on_screen:
        print(message_to_be_displayed)

def write_log_to_file():
    log_file_path = r"..\logs"
    log_file_name = f"execution_log_{start_date_time}.log"
    log_file = os.path.join(log_file_path, log_file_name)

    with open(log_file, "w") as fp:
        fp.writelines("%s\n" % log for log in log_list)

def connect(config):
    conn = None
    try:
        db_name = config["db_name"]
        db_path = config["db_path"]
        conn = sq.connect(os.path.join(db_path, db_name))
        printf(f"Successfully connected to SQLite DB {db_name}")
        return conn
    except Exception as exc:
        printf(f"Exception of type {type(exc).__name__} occured while trying to connect to SQLite DB", "ERROR")
        printf(f"Details of exception are {str(exc)}", "ERROR")
        raise exc

def execute_script(connection, path, script):
    cursor = conn.cursor()
    script_to_be_executed = os.path.join(path, script)
    try:
        with open(script_to_be_executed, "r") as readfp:
            statements = readfp.read()
            for statement in statements.split(";"):
                cursor.execute(statement)

        printf(f"Successfully executed the script {script}")
    except Exception as exc:
        printf(f"Exception of type {type(exc).__name__} occured while executing SQL scripts", "ERROR")
        printf(f"Details of exception are {str(exc)}", "ERROR")
        raise exc

def insert_data(conn, table_name, insert_statement, values_list):
    try:
        cursor = conn.cursor()
        cursor.executemany(insert_statement, values_list)
        #resultset = cursor.fetchall()
        printf(f"{len(values_list)} Rows Successfully inserted into {table_name} table")
        conn.commit()

    except Exception as exc:
        printf(f"Exception of type {type(exc).__name__} occured while inserting data into table {table_name}", "ERROR")
        printf(f"Details of exception are {str(exc)}", "ERROR")
        raise exc

def close(conn):
    try:
        conn.close()
    except Exception:
        pass

def execute_api(query, config, page_num=1):
    base_url = config["base_url"]
    page_size = config["page_size"]
    token = config["token"]
    url_to_scrape = f"{base_url}{query}/?page_size={page_size}&page={page_num}&token={token}"
    #print(url_to_scrape)

    try:
        response = requests.get(url_to_scrape)
        printf(f"GET {query} ... {response}")
        return response
    except Exception as exc:
        printf(f"Exception of type {type(exc).__name__} occured while retrieving data from end-point {query}", "ERROR")
        printf(f"Details of exception are {str(exc)}", "ERROR")
        raise exc

def get_total_page_nums(config):
    response = execute_api("/api/plants", config)

    if "total-pages" in response.headers:
        return int(response.headers["total-pages"])
    else:
        return None

def get_response_json(query, config, page_num=1):
    response = execute_api(query, config, page_num)
    return response.json()

def get_value(dict, key):
    value = dict[key] if key in dict else "NULL"
    return value

def get_meta_data_list(meta_data, record_id):
    result = []
    result.append(record_id)
    result.append(get_value(meta_data, "slug"))
    result.append(get_value(meta_data, "scientific_name"))
    result.append(get_value(meta_data, "link"))
    result.append(get_value(meta_data, "id"))
    result.append(get_value(meta_data, "complete_data"))
    result.append(get_value(meta_data, "common_name"))

    return result


if __name__ == "__main__":

    ###### Step 1 > Connect to the database
    conn = connect(db_config)

    ###### Step 2 > Create the base tables to store METADATA and JSON data in tables
    execute_script(conn, r"..\sql", "create_plant_data.sql")

    ###### Step 3 > Get total number of pages for page width defined in config
    total_pages = get_total_page_nums(config)
    
    if total_pages:
        printf(f"There are a total of {total_pages} pages worth of responses")

        ##### Step 4 > Fetch data for NUM_PAGES_TO_EXTRACT Pages
        ##  This is being done to keep the size of database under 200 MB so as to be able to push to Github

        range_start = 1
        range_end = NUM_PAGES_TO_EXTRACT + 1
        range_step = 1

        record_id = 1
        for page in range(range_start, range_end, range_step):
            printf(f"Processing page {page} of {NUM_PAGES_TO_EXTRACT}", message_type="INFO", display_on_screen=True)
            converted_plant_meta_data_list = []
            plant_data_json_list = []
            try:
                page_data_json = get_response_json(query="/api/plants", config=config, page_num=page)
                for plant_data in page_data_json:
                    printf(plant_data)
                    ##### Step 5 > Having fetched the METADATA log the METADATA into the PLANT_META_DATA table
                    converted_plant_meta_data = get_meta_data_list(plant_data, record_id)
                    converted_plant_meta_data_list.append(converted_plant_meta_data)

                    ##### Step 6 > Extract individual plant details using the ID column returned in the METADATA
                    #####          Only if common_name data is available
                    plant_id = plant_data["id"]
                    if plant_data["common_name"]:
                        try:
                            plant_data_json = get_response_json(query=f"/api/plants/{plant_id}", config=config, page_num=1)
                            plant_data_json_record = [record_id, json.dumps(plant_data_json)]
                            plant_data_json_list.append(plant_data_json_record)
                        except Exception as exc:
                            printf(f"Exception of type {type(exc).__name__} occured while retrieving plant details for plant_id {plant_id}", "ERROR")
                            printf(f"Details of exception are {str(exc)}", "ERROR")
                    record_id = record_id + 1

                ##### Step 7 > Log the extracted data into tables to be later used in visualizatons
                plant_meta_data_insert_statement = f"insert into plant_meta_data(rowid, plant_id, slug, scientific_name, link, complete_data, common_name) values(?,?,?,?,?,?,?)"
                insert_data(conn, "PLANT_META_DATA", plant_meta_data_insert_statement, converted_plant_meta_data_list)
                plant_json_data_insert_statement = f"insert into PLANT_JSON_DATA (meta_data_id, json_data) values(?, ?)"
                insert_data(conn, "PLANT_JSON_DATA", plant_json_data_insert_statement, plant_data_json_list)
            except Exception as exc:
                printf(f"Exception of type {type(exc).__name__} occured on page {page}")
                printf(f"{str(exc)}")
    else:
        printf("Could not determine the total number of pages. Exiting data retrieval")

    ###### Step 8 > Write log to file
    printf("Processing completed")
    write_log_to_file()
    
    ###### Step 9 > Close the database connection
    close(conn)