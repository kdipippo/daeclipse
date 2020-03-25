import json
import eclipse_groups
import PySimpleGUI as sg
import builtins
from create_gif import create_gif
from update_groups_listing import update_groups_listing
import os

def popup_input(prompt):
    """Override the input() function when working in the UI, based on what the
    prompt string contains.

    Arguments:
        prompt {string} -- Message the user sees when prompted.

    Returns:
        string -- user input result.
    """
    if "(Yes/No)" in prompt:
        result = sg.PopupYesNo(prompt)
    elif "[FILE INPUT]" in prompt:
        result = sg.PopupGetFile(prompt)
    else:
        result = sg.PopupGetText(prompt)
    return result

builtins.input = popup_input

def get_folder_categories():
    groups_listing = eclipse_groups.Groups()
    categories = groups_listing.get_categories()
    for category in categories:
        print(category)

def delete_folders_by_filter():
    groups_listing = eclipse_groups.Groups()
    filter_str = input('Please specify what substring to filter:')
    groups_listing.delete_folders_by_filter(filter_str)

def populate_empty_folder_categories():
    groups_listing = eclipse_groups.Groups()
    groups_listing.go_through_empty_categories()

def get_button_menu(actions, menu_title):
    menu_def = [menu_title]
    menu_def.append(list(actions[menu_title].keys()))
    print(menu_def)
    return sg.ButtonMenu(menu_title, menu_def, key=menu_title)

def todo():
    print("TODO")

def call_create_gif():
    gif_filename = create_gif()
    os.system(f'code {gif_filename}')

if __name__ == "__main__":
    sg.ChangeLookAndFeel('DarkBlack')
    actions = {
        'Art': {
            'Generate Icon': 'call_create_gif()'
        },
        'Groups': {
            'Add New Groups': 'update_groups_listing()',
            'Get Folder Categories': 'get_folder_categories()',       # TODO remove this function
            'Delete Folders by Filter': 'delete_folders_by_filter()', # TODO remove this function
            'Populate Empty Folder Categories': 'populate_empty_folder_categories()', # TODO remove this function
            'Submit Art to Group': 'todo()'
        }
    }

    layout = [
        [get_button_menu(actions, 'Art'), get_button_menu(actions, 'Groups'), sg.Button('Exit')],
        [sg.Output(size=(120, 40))],
    ]
    window = sg.Window('MitzyBANANA Control Center', layout, border_depth=0, use_default_focus=False)

    while True:
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        print("#" * 120)
        print("#" * 120)
        if values[event] in actions[event]:
            eval(actions[event][values[event]])
