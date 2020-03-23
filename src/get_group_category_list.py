import json
import eclipse_groups

def get_group_categories():
    groups_listing = eclipse_groups.Groups()
    categories = groups_listing.get_categories()
    for category in categories:
        print(category)

if __name__ == "__main__":
    get_group_categories()
