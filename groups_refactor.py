import json

with open('eclipse_groups_listing.json', 'r') as f:
    eclipse_groups_listing = json.load(f)

for group in eclipse_groups_listing["groups_information"]:
    group["group_id"] = int(group["group_id"])

if True:
    json_file = open('eclipse_groups_listing.json', "w")
    json_file.write(json.dumps(eclipse_groups_listing, indent=2))
    json_file.close()
