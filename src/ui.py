#!/usr/bin/env python
"""Main file for building the app into a GUI."""

# standard imports
import builtins
import os
import sys
import webbrowser

# third-party imports
import PySimpleGUI as sg

# local package imports
import eclipse_api
import eclipse_groups
from gif_generator import create_gif
from update_groups_listing import update_groups_listing


WINDOW = sg.Window('MitzyBANANA Command Center')


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


def print(*args, **kwargs):
    """Replicated implementation of print() with an added window.Refresh() at the end.
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    """
    file_print = kwargs.pop("file", None)
    if file_print is None:
        file_print = sys.stdout
        if file_print is None:
            return
    def write(data):
        file_print.write(str(data))
    sep = kwargs.pop("sep", None)
    if sep is not None:
        if not isinstance(sep, str):
            raise TypeError("sep must be None or a string")
    end = kwargs.pop("end", None)
    if end is not None:
        if not isinstance(end, str):
            raise TypeError("end must be None or a string")
    flush = kwargs.pop('flush', None)
    if kwargs:
        raise TypeError("invalid keyword arguments to print()")
    if sep is None:
        sep = " "
    if end is None:
        end = "\n"
    for i, arg in enumerate(args):
        if i:
            write(sep)
        write(arg)
    write(end)
    if flush:
        file_print.flush()
    window.Refresh()


builtins.print = print


def get_folder_categories() -> None:
    """Displays the list of categories."""
    groups_listing = eclipse_groups.Groups()
    categories = groups_listing.get_categories()
    for category in categories:
        print(category)


def populate_empty_folder_categories():
    """Pass-through for go_through_empty_categories()."""
    groups_listing = eclipse_groups.Groups()
    groups_listing.go_through_empty_categories()


def get_button_menu(actions, menu_title):
    """Returns a ButtonMenu object containing the list of actions with an associated menu category.

    Args:
        actions (dict): Full actions dictionary with labels and callback functions.
        menu_title (string): Top-level menu button title.

    Returns:
        ButtonMenu: object with printed title and dropdown options.
    """
    menu_def = list()
    menu_def.append(menu_title)
    menu_def.append(list(actions[menu_title].keys()))
    return sg.ButtonMenu(menu_title, menu_def, key=menu_title)


def call_create_gif():
    """Generate an animated icon gif and open the result as a preview HTML page in the browser."""
    gif_filename = create_gif()
    with open('create_gif_template.html', 'r') as file:
        html = file.read().replace('\n', '')
    html = html.replace("{{gif_filename}}", gif_filename)
    create_gif_result_path = os.path.abspath('create_gif_result.html')
    create_gif_result_url = f"file://{create_gif_result_path}"

    with open(create_gif_result_path, 'w') as create_gif_result:
        create_gif_result.write(html)
    webbrowser.open(create_gif_result_url)


def get_category_selection(categories):
    """Displays a popup with all possible folder categories to prompt user for appropriate folders.

    Args:
        categories (list(string)): List of folder category names.

    Returns:
        dict(string:boolean): Folder categories marked as True or False, i.e. { 'pixel': True }
    """
    checkbox_layout = []
    checkbox_row = []
    for i in enumerate(categories):
        if i % 5 == 4:
            checkbox_layout.append(checkbox_row)
            checkbox_row = []
        checkbox_row.append(sg.Checkbox(categories[i], key=categories[i]))
    checkbox_layout.append(checkbox_row)
    checkbox_layout.append([sg.Button('SUBMIT'), sg.Button('EXIT')])
    checkbox_window = sg.Window("heyo", checkbox_layout)
    while True:
        checkbox_event, checkbox_values = checkbox_window.Read()
        if checkbox_event in (None, 'EXIT'):
            checkbox_window.Close()
            return dict()
        if checkbox_event == 'SUBMIT':
            checkbox_window.Close()
            print("==== SELECTED ====")
            for checkbox_key in checkbox_values.keys():
                if checkbox_values[checkbox_key]:
                    print(f"- {checkbox_key}")
            print("==================")
            return checkbox_values


def get_percent(count, total):
    """Return the percentage of how many groups have been parsed in the full input .txt file.

    Args:
        count (int): Current count.
        total (int): Total.

    Returns:
        int: Rounded-down percentage.
    """
    result = count / total
    result *= 100
    result = int(result)
    return result


def add_art_to_groups():
    """Automatically sends out group submission requests based on a user-provided deviation URL and
    a set of folder categories."""
    print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    art_url = input("Paste deviation URL: ")
    groups_listing = eclipse_groups.Groups()

    categories = groups_listing.get_categories()
    checkbox_values = get_category_selection(categories)
    submission_folders = groups_listing.get_submission_folders(checkbox_values)
    cont = input("Do you want to move forward with the submission process? (Yes/No): ")
    if cont == "Yes":
        eclipse = eclipse_api.Eclipse()
        count = 0
        for folder in submission_folders:
            print(f"{get_percent(count, len(submission_folders))}% Done - Submitting to Group " +
                  f"{folder['group_id']}, Folder {folder['folder_id']}")
            eclipse.add_deviation_to_group(folder["group_id"], folder["folder_id"], art_url)
            count += 1
    elif cont == "No":
        print("Stopping action.")


def main() -> None:
    """Build and run the main GUI program."""
    sg.ChangeLookAndFeel('Reddit')
    actions = {
        'Art': {
            'Generate Icon': call_create_gif
        },
        'Groups': {
            'Add New Groups': update_groups_listing,
            'Get Folder Categories': get_folder_categories,
            'Populate Empty Folder Categories': populate_empty_folder_categories,
            'Submit Art to Groups': add_art_to_groups
        }
    }

    layout = [
        [get_button_menu(actions, 'Art'), get_button_menu(actions, 'Groups'), sg.Button('Exit')],
        [sg.Output(size=(120, 40))]
    ]

    WINDOW = sg.Window('MitzyBANANA Command Center', layout, border_depth=0)

    while True:
        event, values = WINDOW.Read()
        if event in (None, 'Exit'):
            break
        print("#" * 120)
        print("#" * 120)
        if values[event] in actions[event]:
            actions[event][values[event]]()


if __name__ == "__main__":
    main()
