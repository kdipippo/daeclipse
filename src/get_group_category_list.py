import json
import groups

def get_group_categories():
    groups_listing = groups.GroupsListing()
    categories = groups_listing.get_categories()
    for category in categories:
        print(category)

if __name__ == "__main__":
    get_group_categories()
