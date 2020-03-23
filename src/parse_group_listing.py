import json
import eclipse_groups

if __name__ == "__main__":
    groups_listing = eclipse_groups.Groups()

    print("1) delete group folders by filter")
    print("2) add category individually")
    option = input("Select the number procedure to undergo: ")
    if option == "1":
        filter_str = input("Please specify what substring to filter: ")
        groups_listing.delete_folders_by_filter(filter_str)
    elif option == "2":
        groups_listing.go_through_empty_categories()
