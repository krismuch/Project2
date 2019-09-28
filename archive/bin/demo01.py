import json
import requests
from config import config

class Plants():
    def __init__(self, page_size = 30):
        self.page_size = 30
        self.base_url = f"https://trefle.io"
        self.api_key = None
        self.total_pages = None

    def setApiKey(self, api_key):
        self.api_key = api_key

    # def convertToParams(self, config):
    #     retlist = [f"{key}:{value}" for key, value in config.items()]
    #     retstring = '&'.join(retlist)
    #     return retstring

    def get_response(self, api_url, page_num = None):
        api_key = self.api_key
        page_size=self.page_size
        url = self.base_url
        query_operator = "/?"

        url = url + api_url + query_operator + f"page_size={page_size}"
        #url = f"https://trefle.io{api_url}/?page_size={page_size}"
    
        if page_num:
            url =f"{url}&page={page_num}"
        url = f"{url}&token={api_key}"
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
        return dataList

# totalPages = getNumPages()

# plant_list = getDataList("/api/plants")
# for plantid, plant in enumerate(plant_list, start = 1):
#     print(f"({plantid:>02}.)  Slug => {plant['slug']}")