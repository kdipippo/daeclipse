import eclipse_groups
import PySimpleGUI as sg
import builtins
from gif_generator import create_gif
from update_groups_listing import update_groups_listing
import os
import webbrowser


window = sg.Window('MitzyBANANA Control Center')


def popup_input(prompt) -> str:
    """Override the input() function when working in the UI, based on what the
    prompt string contains.

    Args:
        prompt (string): Message the user sees when prompted.

    Returns:
        string: user input result.
    """
    if "(Yes/No)" in prompt:
        result = sg.PopupYesNo(prompt)
    elif "[FILE INPUT]" in prompt:
        result = sg.PopupGetFile(prompt)
    else:
        result = sg.PopupGetText(prompt)
    return result


builtins.input = popup_input


def print(*args, **kwargs) -> None:
    """Override the print() function to call window.Refresh() after all print() calls."""
    builtins.print(*args, **kwargs)
    window.Refresh()


def get_folder_categories():
    """Display the list of

    Returns:

    """
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
    """Placeholder function for actions that are not implemented yet."""
    print("TODO")


def call_create_gif():
    """Generate an animated icon gif and open the result as a preview HTML page in the browser."""
    gif_filename = create_gif()
    with open('create_gif_template.html', 'r') as file:
        html = file.read().replace('\n', '')
    html = html.replace("{{gif_filename}}", gif_filename)
    path = os.path.abspath('create_gif_result.html')
    url = 'file://' + path

    with open(path, 'w') as f:
        f.write(html)
    webbrowser.open(url)


if __name__ == "__main__":
    sg.ChangeLookAndFeel('DarkBlack')
    # TODO The lines below marked as TODO contain functionality that should be refactored simpler.
    ACTIONS = {
        'Art': {
            'Generate Icon': call_create_gif
        },
        'Groups': {
            'Add New Groups': update_groups_listing,
            'Get Folder Categories': get_folder_categories,                       # TODO
            'Delete Folders by Filter': delete_folders_by_filter,                 # TODO
            'Populate Empty Folder Categories': populate_empty_folder_categories, # TODO
            'Submit Art to Group': todo
        }
    }

    layout = [
        [get_button_menu(ACTIONS, 'Art'), get_button_menu(ACTIONS, 'Groups'), sg.Button('Exit')],
        [sg.Output(size=(120, 40))],
    ]

    window = sg.Window('MitzyBANANA Control Center', layout, border_depth=0, use_default_focus=False)

    while True:
        EVENT, VALUES = window.Read()
        if EVENT in (None, 'Exit'):
            break
        print("#" * 120)
        print("#" * 120)
        if VALUES[EVENT] in ACTIONS[EVENT]:
            ACTIONS[EVENT][VALUES[EVENT]]()
