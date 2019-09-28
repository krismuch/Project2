import json
import requests
from config import config

class Plants():
    def __init__(self, page_size = 30):
        self.page_size = page_size
        self.base_url = f"https://trefle.io"
        self.api_key = None
        self.total_pages = None

    def setApiKey(self, api_key):
        self.api_key = api_key

    def get_response(self, api_url, page_num = None):
        api_key = self.api_key
        page_size=self.page_size
        url = self.base_url
        query_operator = "/?"

        url = url + api_url + query_operator + f"page_size={page_size}"
    
        if page_num:
            url =f"{url}&page={page_num}"
        url = f"{url}&token={api_key}"
        #print(url)
        response = requests.get(url)
        return response
    
    def getNumPages(self):
        response = self.get_response("/api/plants")
        num_pages = int(response.headers["total-pages"])
        self.total_pages = num_pages
        return num_pages

    def getDataList(self, api_url, page_num = None):
        response = self.get_response(api_url=api_url, page_num=page_num)
        print(response)
        dataList = response.json()
        #print(dataList)
        return dataList

    def display_plant_data(self, plant, id=None):
        if id:
            print(f'({id:<03}.)["SLUG", "SCIENTIFIC_NAME", "LINK", "ID", "COMPLETE_DATA", "COMMON_NAME"] = [{plant["slug"]}, {plant["scientific_name"]}, {plant["link"]}, {plant["id"]}, {plant["complete_data"]}, {plant["common_name"]}]')
        else:
            print(f'["SLUG", "SCIENTIFIC_NAME", "LINK", "ID", "COMPLETE_DATA", "COMMON_NAME"] = [{plant["slug"]}, {plant["scientific_name"]}, {plant["link"]}, {plant["id"]}, {plant["complete_data"]}, {plant["common_name"]}]')

    def get_full_plant_data_in_json(self, plant_link):
        url = f"{plant_link}/?token={self.api_key}"
        try:
            response = requests.get(url)
            print(response)
            response_json = response.json()
            return response_json
        except Exception as e:
            print(f"Exception occured while fetching data from url {url}, {type(e).__name__}, {e}")
            return {}


if __name__ == "__main__":
    plants = Plants(page_size=3)
    plants.setApiKey(config["token"])
    plant_data_list = plants.getDataList("/api/plants", page_num=1)

    for recordid, plant in enumerate(plant_data_list, start = 1):
        print(f'({recordid}.) {plant}')
        #pass