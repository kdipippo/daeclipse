import json
import eclipse_groups
import PySimpleGUI as sg

def get_folder_categories():
    groups_listing = eclipse_groups.Groups()
    categories = groups_listing.get_categories()
    for category in categories:
        print(category)

def delete_folders_by_filter(sg):
    groups_listing = eclipse_groups.Groups()
    filter_str = sg.PopupGetText('Please specify what substring to filter:', 'filter_str')
    print(filter_str)
    groups_listing.delete_folders_by_filter2(sg, filter_str)

def populate_empty_folder_categories(sg):
    groups_listing = eclipse_groups.Groups()
    groups_listing.go_through_empty_categories2(sg)

if __name__ == "__main__":
    buttons = {
        "Get Folder Categories": "get_folder_categories()",
        "Delete Folders by Filter": "delete_folders_by_filter(sg)",
        "Populate Empty Folder Categories": "populate_empty_folder_categories(sg)"
    }
    top_row_buttons = []
    for button_text in buttons.keys():
        top_row_buttons.append(sg.Button(button_text))
    top_row_buttons.append(sg.Button('EXIT'))

    layout = [
        top_row_buttons,
        [sg.Text('Script output....', size=(40, 1))],
        [sg.Output(size=(120, 40))]
    ]
    window = sg.Window('MitzyBANANA Control Center', layout)

    while True:
        (event, value) = window.read()
        print("#" * 80)
        print("#" * 80)
        print("#" * 80)
        if event == 'EXIT'  or event is None:
            break
        elif event in buttons:
            eval(buttons[event])
