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

def test(sg):
    layout =  [[sg.Checkbox('My first Checkbox!', default=True), sg.Checkbox('My second Checkbox!')]]
    sg.Popup('testing', layout)

if __name__ == "__main__":
    sg.ChangeLookAndFeel('GreenTan')

    buttons = {
        "Get Folder Categories": "get_folder_categories()",
        "Delete Folders by Filter": "delete_folders_by_filter(sg)",
        "Populate Empty Folder Categories": "populate_empty_folder_categories(sg)",
        "test": "test(sg)"
    }
    top_row_buttons = []
    for button_text in buttons.keys():
        top_row_buttons.append(sg.Button(button_text))
    top_row_buttons.append(sg.Button('EXIT'))

    tab1_layout =  [[sg.T('This is inside tab 1')]]
    tab2_layout = [[sg.T('This is inside tab 2')],
                [sg.In(key='in')]]

    layout = [
        top_row_buttons,
        [sg.Output(size=(120, 40))],
        [sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])],
        [sg.Button('Read')]
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
