import json

def addFolderCheck(folderName, groupName):
    lowerFolderName = folderName.lower()
    if lowerFolderName in ["journals", "journal"]:
        return False
    if "full" in lowerFolderName:
        result = input(f"{groupName} ::: '{folderName}'. Add? (y/n): ")
        if result == "y":
            return True
        elif result in ("n", ""):
            return False
        else:
            result = input("Answer must be y/n: ")
            if result == "y":
                return True
            elif result in ("n", ""):
                return False
    return True

# ===============================================================

with open('eclipse_groups_listing.json', 'r') as f:
    eclipse_groups_listing = json.load(f)

'''
print("Enter is interpretted the same way as no.")
for group in eclipse_groups_listing["groups_information"]:
    newFolders = []
    for folder in group["folders"]:
        if addFolderCheck(folder["folder_name"], group["group_name"]):
            newFolders.append(folder)
    group["folders"] = newFolders
'''

print("Leave blank to delete folder")
for group in eclipse_groups_listing["groups_information"]:
    newFolders = []
    promptContinue = False
    alreadyPrinted = False
    print(f"\n⭐{group['group_name']}")
    for folder in group["folders"]:
        if len(folder["categories"]) > 0:
            newFolders.append(folder)
        else:
            if not alreadyPrinted:
                for folderListing in group["folders"]:
                    print(f"-- {folderListing['folder_name']}")
                print("-------------------")
                alreadyPrinted = True
            promptContinue = True
            result = input(f"'{folder['folder_name']}'. Category? : ")
            if result != "":
                folder["categories"].append(result)
                newFolders.append(folder)
    group["folders"] = newFolders
    if promptContinue:
        cont = input("Continue? 'EXIT to leave: ")
        if cont == "EXIT":
            break

json_file = open('eclipse_groups_listing.json', "w")
json_file.write(json.dumps(eclipse_groups_listing, indent=2))
json_file.close()


