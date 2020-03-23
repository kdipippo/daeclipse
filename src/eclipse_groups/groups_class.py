import json
import pathlib

class Groups:
    def __init__(self):
        with open(f'{pathlib.Path(__file__).parent.absolute()}/eclipse_groups_listing.json', 'r') as f:
            self.groups = json.load(f)

    def get_categories(self):
        categories = []
        for group in self.groups["groups_information"]:
            for folder in group["folders"]:
                if len(folder["category"]) > 0:
                    categoryStr = folder["category"].replace("(","").replace(")","")
                    categoryList = categoryStr.split(" ")
                    for cat in categoryList:
                        if cat not in categories and cat not in ["and", "or"]:
                            categories.append(cat)
        categories.sort()
        return categories
