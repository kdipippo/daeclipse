import eclipse_api
import eclipse_groups
import PySimpleGUI as sg
import builtins
from gif_generator import create_gif
from update_groups_listing import update_groups_listing
import os
import webbrowser
import sys


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


'''
def print(*args, **kwargs):
    """Override the print() function to call window.Refresh() after all print() calls."""
    # sys.stdout.write() is used instead of print() to avoid recursively calling builtins.print().
    sys.stdout.write(*args, **kwargs)
    sys.stdout.write('\n')
    window.Refresh()
'''

def print(*args, **kwargs):
    # THIS IS A COPY OF HOW PRINT() BEHAVES WITH window.Refresh() at the end of it
    """print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    """
    fp = kwargs.pop("file", None)
    if fp is None:
        fp = sys.stdout
        if fp is None:
            return
    def write(data):
        fp.write(str(data))
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
        fp.flush()
    window.Refresh()


builtins.print = print


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


def get_category_selection(categories):
    checkbox_layout = []
    checkbox_row = []
    for i in range(len(categories)):
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

    Arguments:
        count {int} -- Current count.
        total {int} -- Total.

    Returns:
        int -- Rounded-down percentage.
    """
    result = count / total
    result *= 100
    result = int(result)
    return result


def add_art_to_groups2():
    """Automatically sends out group submission requests based on a user-provided deviation URL and
    a set of folder categories."""
    print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    art_url = input("Paste deviation URL: ")
    groups_listing = eclipse_groups.Groups()

    # TODO 1) obtain the list of categories
    categories = groups_listing.get_categories()

    # TODO 2) send out a window with checkbox options to submit
    # TODO 3) receive the list of checkbox selections
    checkbox_values = get_category_selection(categories)

    # TODO 4) use the checkbox selections to get the list of groups & folders to submit to
    submission_folders = groups_listing.get_submission_folders(checkbox_values)
    # TODO 5) iterate over result with add_deviation_to_group. Be sure that this call shows with delays.
    cont = input("Please confirm if you want to move forward with the submission process (Yes/No): ")
    if cont == "Yes":
        eclipse = eclipse_api.Eclipse()
        count = 0
        for folder in submission_folders:
            print(f"{get_percent(count, len(submission_folders))}% Done - Submitting to Group {folder['group_id']}, Folder {folder['folder_id']}")
            eclipse.add_deviation_to_group(folder["group_id"], folder["folder_id"], art_url)
            count += 1
    elif cont == "No":
        print("Stopping action.")

if __name__ == "__main__":
    sg.ChangeLookAndFeel('LightTeal')
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
            'Submit Art to Groups': add_art_to_groups2
        }
    }

    layout = [
        [get_button_menu(ACTIONS, 'Art'), get_button_menu(ACTIONS, 'Groups'), sg.Button('Exit')],
        [sg.Output(size=(120, 40))]
    ]

    window = sg.Window('MitzyBANANA Control Center', layout, border_depth=0)

    while True:
        EVENT, VALUES = window.Read()
        if EVENT in (None, 'Exit'):
            break
        print("#" * 120)
        print("#" * 120)
        if VALUES[EVENT] in ACTIONS[EVENT]:
            ACTIONS[EVENT][VALUES[EVENT]]()
