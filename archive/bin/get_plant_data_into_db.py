from datetime import datetime as dt
from Connection import Connection
from Plants import Plants
from config import config, dbConfig

connection = Connection()

plants = Plants(page_size=2)
plants.setApiKey(config["token"])
totalPages = plants.getNumPages()
page_list = range(1, totalPages+1)

for page in page_list:
    plant_data_set = plants.getDataList(api_url="/api/plants", page_num=page)
    for plant_data in plant_data_set:
        plants.display_plant_data(plant_data)
        plant_full_data = plants.get_full_plant_data_in_json(plant_data["link"])
    #print(plant_data)
    #plants.display_plant_data(plant_data)
    insert_statement = f"INSERT INTO PLANT_DETAILS(INSERT_DATETIME, PLANT_ID, SLUG, SCIENTIFIC_NAME, PLANT_LINK, COMPLETE_DATA, COMMON_NAME, PLANT_DETAILS_JSON) VALUES('{dt.now()}', {plant_data['id']}, '"+plant_data['slug']+"', '"+plant_data['scientific_name']+"', '"+plant_data['link']+"', "+str(plant_data['complete_data'])+", '"+plant_data['common_name']+"', NULL);"
    print(insert_statement)
    if page > 10:
        break




    