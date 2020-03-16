#!/usr/bin/env python
"""This script generates a 50x50 animated gif either randomly or with provided
color and image information via a json file."""

from datetime import datetime
import json
import random
from PIL import Image

# Used for the background to be erased when the image is made transparent.
# Set to a muted green color that does not coincide with the pixel art palette.
DEFAULT_COLOR = (83, 106, 89, 255)
TRANSPARENT_COLOR = (255, 255, 255, 0)

class SelectedAssets:
    """Class to handle the list of colors and images randomly generated for gif creation."""
    colors = {}
    images = {}
    json = None
    def add_color(self, color_type, selected_type):
        """Assign the selected palette to the component to recolor.

        Arguments:
            color_type {string} -- Component the recolor applies to, i.e. 'skin'.
            selected_type {string} -- Palette to recolor the component to, i.e. 'pale'.
        """
        self.colors[color_type] = selected_type

    def add_image(self, image_type, image_num):
        """Assign the selected image asset to the image layer when gif parts are layered.

        Arguments:
            image_type {string} -- Image layer being added, i.e. 'hairbackshort'.
            image_num {string} -- Asset number for the image layer, i.e. '00A'.
        """
        self.images[image_type] = "{:02d}".format(image_num)

    def store_json(self, assets_json):
        """Store the full, parsed assets.json file for reference.

        Arguments:
            assets_json {dict} -- Dictionary result from loading assets.json.
        """
        self.json = assets_json

    def debug_override(self, override):
        """Manually override the colors and images dictionaries.

        Arguments:
            override {dict} -- A combined dict with keys 'colors' and 'images'.
        """
        self.colors = override['colors']
        self.images = override['images']

    def debug(self):
        """Print out the stored colors and images settings."""
        for color in self.colors.keys():
            print(f"COLOR {color} = {self.colors[color]}")
        for image in self.images.keys():
            print(f"IMAGE {image} = {self.images[image]}")

    def get_json(self):
        """Return the colors and images dicts as one combined dict.

        Returns:
            dict -- A combined dict with keys 'colors' and 'images'.
        """
        combined_json = {}
        combined_json['colors'] = self.colors
        combined_json['images'] = self.images
        return combined_json

def bob_down(frame_num):
    """Returns whether the sprite is bobbing down, false if bobbing up.

    Arguments:
        frame_num {int} -- Current frame number.

    Returns:
        boolean -- True if sprite is bobbing down, false if bobbing up.
    """
    if frame_num % 4 == 1 or frame_num % 4 == 2:
        return False
    return True

def translate_image(image, direction, pixels):
    """Return a translated image.

    Arguments:
        image {Image} -- Image object.
        direction {string} -- "left", "right", "up", or "down".
        pixels {int} -- Number of pixels to translate.

    Returns:
        Image -- Translated Image object.
    """
    trans_matrix = [1, 0, 0, 0, 1, 0]
    if direction == "left":
        trans_matrix[2] += pixels
    elif direction == "right":
        trans_matrix[2] -= pixels
    elif direction == "up":
        trans_matrix[5] += pixels
    elif direction == "down":
        trans_matrix[5] -= pixels
    return image.transform(image.size, Image.AFFINE, tuple(trans_matrix), fillcolor=DEFAULT_COLOR)

def get_filename(image_type, asset_name):
    """Returns path to the given image asset.

    Arguments:
        image_type {string} -- Type of image, i.e. 'hairfront', 'eyes'.
        asset_name {string} -- Asset number, sometimes with position letter, i.e. '00', '00A'.

    Returns:
        string -- Path to image asset.
    """
    return f"images/{image_type}/{image_type}{asset_name}.png"

def get_custom_asset(image_type, asset_name, frame_num):
    """Get the Image object for the current custom asset. The second frame is manually created.

    Arguments:
        image_type {string} -- Type of image, i.e. 'hairfront', 'eyes'.
        asset_name {string} -- Asset number, i.e. '00'.
        frame_num {int} -- Current frame number.

    Returns:
        Image -- Requested Image object.
    """
    asset_letter = "A"
    if bob_down(frame_num):
        asset_letter = "B"
    return Image.open(get_filename(image_type, f"{asset_name}{asset_letter}"))

def get_2frame_asset(image_type, asset_name, frame_num):
    """Get the Image object for the current 2-frame asset. The second frame is generated rather
    than manually created, as with a custom asset.

    Arguments:
        image_type {string} -- Type of image, i.e. 'hairfront', 'eyes'.
        asset_name {string} -- Asset number, i.e. '00'.
        frame_num {int} -- Current frame number.

    Returns:
        Image -- Requested Image object.
    """
    image = Image.open(get_filename(image_type, asset_name))
    if bob_down(frame_num):
        return translate_image(image, 'down', 1)
    return image

def get_rgba_from_hex(hex_string):
    """Converts hex color string to rgba color tuple.

    Arguments:
        hex_string {string} -- hex color string, i.e. 79ede2

    Returns:
        tuple -- 4-entry tuple of ints representing rgba, i.e. (121, 237, 226, 255)
    """
    rgb = list(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
    rgb.append(255)
    return tuple(rgb)

def update_palette(before_img, before_colors, after_colors):
    """Recolor a given image with an array of 'before' colors to an array of 'after'.

    Arguments:
        before_img {Image} -- Image object with mode 'RGBA' to be recolored.
        before_colors {list(tuple)} -- RGBA colors that will be recolored, i.e. [(0, 0, 0, 255)]
        after_colors {list(tuples)} -- RGBA colors to be used for recoloring, i.e. [(1, 1, 1, 255)]

    Returns:
        Image -- Recolored Image object.
    """
    before_pixel_map = before_img.load()

    after_img = Image.new('RGBA', before_img.size)
    after_pixel_map = after_img.load()
    for i in range(after_img.size[0]):
        for j in range(after_img.size[1]):
            curr_color = before_pixel_map[i, j]
            if curr_color in before_colors:
                after_index = before_colors.index(curr_color)
                after_pixel_map[i, j] = after_colors[after_index]
            else:
                after_pixel_map[i, j] = before_pixel_map[i, j]
    return after_img

def make_transparent(img):
    """Return the image with a transparent background. Transparency is based on what is left as
    the DEFAULT_COLOR from the original Image creation.

    Arguments:
        img {Image} -- Image object.

    Returns:
        Image -- Image object with a transparent background.
    """
    return update_palette(img, [DEFAULT_COLOR], [TRANSPARENT_COLOR])

def change_color(img, color_dict, default_color, new_color):
    """Recolor an image with a provided palette of colors.

    Arguments:
        img {Image} -- Image object.
        color_dict {dict} -- Dictionary that maps palette name to a string of hex colors.
        default_color {string} -- Default palette name for the asset, i.e. 'pink'.
        new_color {string} -- Desired palette name to recolor the asset, i.e. 'orange'.

    Returns:
        Image -- Recolored Image object.
    """
    img = img.convert('RGBA')
    before_hexes = color_dict[default_color]
    after_hexes = color_dict[new_color]
    before_rgba = list(map(get_rgba_from_hex, before_hexes.split(",")))
    after_rgba = list(map(get_rgba_from_hex, after_hexes.split(",")))
    return update_palette(img, before_rgba, after_rgba)

def get_frame(frame_num, assets):
    """Assemble a single frame of the gif.

    Arguments:
        frame_num {int} -- Current frame number.
        assets {SelectedAssets} -- SelectedAssets object.

    Returns:
        Image -- Frame as an Image object.
    """
    # Get the order that images are layered.
    sorted_layers = sorted(ASSETS_JSON['imageTypes'].items(), key=lambda x: x[1]['order'])
    frame = Image.new('RGBA', (50, 50), color=DEFAULT_COLOR)
    for layer in sorted_layers:
        image_type = layer[0]
        image_info = layer[1]
        if image_type not in assets.images:
            continue
        asset_name = assets.images[image_type]

        # Handling 'eyes' animation: get the correct letter based on blinking position.
        if image_type == "eyes":
            if frame_num in [25, 29]:
                asset_name += "B"
            elif frame_num in [26, 28]:
                asset_name += "C"
            elif frame_num == 27:
                asset_name += "D"
            else:
                asset_name += "A"

        if image_info['type'] == "2frame":
            image_layer = get_2frame_asset(image_type, asset_name, frame_num)
        elif image_info['type'] == "custom":
            image_layer = get_custom_asset(image_type, asset_name, frame_num)

        if 'recolor' in image_info:
            for recolor_type in image_info['recolor']:
                # variables are suffering
                color_dict = assets.json['colorHexes'][recolor_type]['options']
                default_color = assets.json['colorHexes'][recolor_type]['default']
                new_color = assets.colors[recolor_type]
                image_layer = change_color(image_layer, color_dict, default_color, new_color)
        frame.paste(image_layer, (0, 0), image_layer)

    frame = translate_image(frame, 'left', 5)
    frame = make_transparent(frame)
    watermark = Image.open("images/watermark.png")
    frame.paste(watermark, (0, 0), watermark)
    return frame

def get_gif(assets, current_time):
    """Assemble a list of frames, string them together, and save the gif to output/.

    Arguments:
        assets {SelectedAssets} -- SelectedAssets object.
        current_time {string} -- Full current time string, i.e. '2020-03-16_12:02:08AM'.
    """
    frames = []
    for i in range(32):
        frames.append(get_frame(i, assets))
    frames[0].save(
        f'output/{current_time}.gif',
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=100,
        loop=0,
        transparency=0,
        disposal=2
    )

def get_random_asset_list(assets_json):
    """Randomize and return the list of colors and components for the generated gif.

    Arguments:
        assets_json {dict} -- Parsed assets.json file as a dictionary.

    Returns:
        SelectedAssets -- SelectedAssets object.
    """
    assets = SelectedAssets()
    color_types = list(assets_json['colorHexes'].keys())
    for color_type in color_types:
        color_options = list(assets_json['colorHexes'][color_type]['options'].keys())
        assets.add_color(color_type, random.choice(color_options))
    image_types = list(assets_json['imageTypes'].keys())
    for image_type in image_types:
        coin_toss = random.random()
        if coin_toss < assets_json['imageTypes'][image_type]['probability']:
            selected_num = random.randint(0, assets_json['imageTypes'][image_type]['count']-1)
            assets.add_image(image_type, selected_num)
    return assets

def get_json(assets, current_time):
    """Creates a json file with the generated asset settings along with the same-named gif.

    Arguments:
        assets {SelectedAssets} -- SelectedAssets object.
        current_time {string} -- Full current time string, i.e. '2020-03-16_12:02:08AM'.
    """
    json_file = open(f'output/{current_time}.json', "w")
    json_file.write(json.dumps(assets.get_json(), indent=2))
    json_file.close()

if __name__ == "__main__":
    with open('assets.json', 'r') as f:
        ASSETS_JSON = json.load(f)
    GIF_ASSETS = get_random_asset_list(ASSETS_JSON)
    GIF_ASSETS.store_json(ASSETS_JSON)

    with open('presets/rin.json', 'r') as f:
        RIN_JSON = json.load(f)
    GIF_ASSETS.debug_override(RIN_JSON)

    GIF_ASSETS.debug()
    CURRENT_TIME = datetime.today().strftime("%Y-%m-%d_%I:%M:%S%p")
    get_gif(GIF_ASSETS, CURRENT_TIME)
    get_json(GIF_ASSETS, CURRENT_TIME)
