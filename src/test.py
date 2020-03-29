import PySimpleGUI as sg

def preview_all_look_and_feel_themes(columns):
    """
    Displays a "Quick Reference Window" showing all of the different Look and Feel settings that are available.
    They are sorted alphabetically.  The legacy color names are mixed in, but otherwise they are sorted into Dark and Light halves
    :param columns: (int) The number of themes to display per row
    """
    web = False
    win_bg = 'black'
    def sample_layout():
        return [
            [sg.Checkbox('Checkbox Text')]
        ]

    layout = [[sg.Text('Here is a complete list of themes', font='Default 18', background_color=win_bg)]]

    names = sg.list_of_look_and_feel_values()
    names.sort()
    row = []
    for count, theme in enumerate(names):
        sg.change_look_and_feel(theme)
        if not count % columns:
            layout += [row]
            row = []
        row += [sg.Frame(theme, sample_layout() if not web else [[sg.T(theme)]] + sample_layout())]
    if row:
        layout += [row]

    window = sg.Window('Preview of all Look and Feel choices', layout, background_color=win_bg)
    window.read()
    window.close()

if __name__ == "__main__":
    preview_all_look_and_feel_themes(10)
