import requests
import json
import sqlite3 as sq

conn = sq.connect("../db/data_farming_updated.db")
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS PLANT_META_DATA (rowid                      integer, 
                                                         plant_id                   integer, 
                                                         slug                       varchar(1000),
                                                         scientific_name            varchar(1000),
                                                         link                       varchar(1000),
                                                         complete_data              boolean,
                                                         common_name                varchar(1000)
                                                        )
         """)

c.execute("""CREATE TABLE IF NOT EXISTS PLANT_JSON_DATA (meta_data_id               integer,
                                                         json_data                  json
                                                        )
         """)

base_url = f"https://trefle.io/"
query="/api/plants"
token=input("Please provide your token:")
per_page = 200
page_size_url="page_size="+str(per_page)

plant_metadata_extraction_url = base_url + query + "/?" +page_size_url+"&token="+token
response = requests.get(plant_metadata_extraction_url)
#print(response.headers)
total_pages = int(response.headers["total-pages"])
page_range = range(1, total_pages + 1)
token_url="token="+token

for page in page_range:
    page_url="page="+str(page)
    extract_page_data_url = f"{base_url}{query}/?{page_size_url}&{page_url}&{token_url}"
    #print(extract_page_data_url)
    response=requests.get(extract_page_data_url)
    #print(type(response.json()))
    plant_response_list = response.json()

    print(f"Processing page {page} of {total_pages}")
    metadata_values_list=[]
    details_list = []
    for rowid, plant in enumerate(plant_response_list):
        #print(plant["slug"])
        print(f"{page}.{rowid}")
        record_id = per_page * (page - 1) + rowid
        slug=plant["slug"] if "slug" in plant else "NULL"
        plant_id = plant["id"] if "id" in plant else "NULL"
        scientific_name = plant["scientific_name"] if "scientific_name" in plant else "NULL"
        link=plant["link"] if "link" in plant else "NULL"
        complete_data = plant["complete_data"] if "complete_data" in plant else "NULL"
        common_name = plant["common_name"] if "common_name" in plant else "NULL"

        if "common_name" not in plant:
            continue
        metadata_insert_statement = f"insert into plant_meta_data(rowid, plant_id, slug, scientific_name, link, complete_data, common_name) values(?,?,?,?,?,?,?)"
        #
        metadata_record = (record_id, plant_id, slug, scientific_name, link, complete_data, common_name)
        metadata_values_list.append(metadata_record)
        #print(metadata_values_list)
        plant_detail_url = f"{link}/?{page_size_url}&{page_url}&{token_url}"
        #print(plant_detail_url)
        try:
            response = requests.get(plant_detail_url)
            #print(plant_detail_url)
            #print(response)
            response_json = response.json()

            json_data_insert_statement = f"insert into PLANT_JSON_DATA (meta_data_id, json_data) values(?, ?)"
            detail_record = (record_id, json.dumps(response_json))
            details_list.append(detail_record)
        except Exception as exc:
            print(f"Exception {type(exc).__name__} occured while processing URL ({plant_detail_url})")
        #
    try:
        c.executemany(metadata_insert_statement, metadata_values_list)
    except Exception as e:
        print(type(e).__name__)
    conn.commit()
    try:
        c.executemany(json_data_insert_statement, details_list)
    except Exception as e:
        print(type(e).__name__)
    conn.commit()
    if page >= 100:
        break

conn.commit()
conn.close()