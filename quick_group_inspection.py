import json

with open('eclipse_groups_listing.json', 'r') as f:
    eclipse_groups_listing = json.load(f)

categories = []
for group in eclipse_groups_listing["groups_information"]:
    for folder in group["folders"]:
        if len(folder["category"]) > 0:
            categoryStr = folder["category"].replace("(","").replace(")","")
            categoryList = categoryStr.split(" ")
            for cat in categoryList:
                if cat not in categories:
                    categories.append(cat)

categories.sort()

with open('heyo.txt', 'w') as filehandle:
    for category in categories:
        filehandle.write('%s\n' % category)
