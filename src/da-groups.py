import json
import requests
import browser_cookie3
from bs4 import BeautifulSoup

class DeviantArtNAPI:
    base_uri = "https://www.deviantart.com/_napi/shared_api/deviation"
    def __init__(self, deviation_url):
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')
        self.set_deviation_id(deviation_url)
        self.setCSRF(deviation_url)
    def getGroups(self):
        # this only returns 10 results. The "userId" field corresponds
        # to the group_id for getGroupFolders()
        url = f"{self.base_uri}/groups"
        response = requests.get(url, cookies=self.cookies)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))
    def getGroupFolders(self, group_id):
        url = f"{self.base_uri}/group_folders?groupid={group_id}&type=gallery"
        response = requests.get(url, cookies=self.cookies)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))
    def addDeviationToGroup(self, group_id, folder_id):
        url = f"{self.base_uri}/group_add"
        payload = {
            "groupid": group_id,
            "type": "gallery",
            "folderid": folder_id,
            "deviationid": self.deviation_id,
            "csrf_token": self.csrf_token
        }
        headers = {
            "accept": 'application/json, text/plain, */*',
            "content-type": 'application/json;charset=UTF-8'
        }
        response = requests.post(url, cookies=self.cookies, headers=headers, data=json.dumps(payload))
        print(response.status_code)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))
    def setCSRF(self, deviation_url):
        page = requests.get(deviation_url, cookies=self.cookies)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.csrf_token = soup.find("input", {"name":"validate_token"})["value"]
    def set_deviation_id(self, deviation_url):
        url_parts = deviation_url.split("-")
        self.deviation_id = url_parts[-1]

if __name__ == "__main__":
    # working, only gives 10 - deviantart.getGroups()
    # working - deviantart.getGroupFolders(14718292)
    # not working - deviantart.addDeviationToGroup(14718292, 63180668, 765976537)
    url = "https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537"
    check = input("Press enter to confirm that the deviation is open in Chrome with Eclipse set to on: ")
    deviantart = DeviantArtNAPI(url)
    deviantart.addDeviationToGroup(
        40852213, # Candycorn-Kingdom
        60854872  # Featured
    )
