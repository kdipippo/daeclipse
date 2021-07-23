#!/usr/bin/env python
"""This script generates a 50x50 animated gif either randomly or with provided
color and image information via a json file."""

from datetime import datetime
import json
import random
import pathlib
from PIL import Image
from gif_generator.selected_assets_class import SelectedAssets
import yaml

# Used for the background to be erased when the image is made transparent.
# Set to a muted green color that does not coincide with the pixel art palette.

DEFAULT_COLOR = (83, 106, 89, 255)
TRANSPARENT_COLOR = (255, 255, 255, 0)

IMAGE_FILE_PREFIX = pathlib.Path(__file__).parent.absolute()
OUTPUT_FILE_PREFIX = pathlib.Path(__file__).parent.parent.parent.absolute()

def bob_down(frame_num):
    """Returns whether the sprite is bobbing down, false if bobbing up.

    Args:
        frame_num (int): Current frame number.

    Returns:
        boolean: True if sprite is bobbing down, false if bobbing up.
    """
    if frame_num % 4 == 1 or frame_num % 4 == 2:
        return False
    return True

def translate_image(image, direction, pixels):
    """Return a translated image.

    Args:
        image (Image): Image object.
        direction (string): "left", "right", "up", or "down".
        pixels (int): Number of pixels to translate.

    Returns:
        Image: Translated Image object.
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

    Args:
        image_type (string): Type of image, i.e. 'hairfront', 'eyes'.
        asset_name (string): Asset number, sometimes with position letter, i.e. '00', '00A'.

    Returns:
        string: Path to image asset.
    """
    return f"{IMAGE_FILE_PREFIX}/images/{image_type}/{image_type}{asset_name}.png"

def get_custom_asset(image_type, asset_name, frame_num):
    """Get the Image object for the current custom asset. The second frame is manually created.

    Args:
        image_type (string): Type of image, i.e. 'hairfront', 'eyes'.
        asset_name (string): Asset number, i.e. '00'.
        frame_num (int): Current frame number.

    Returns:
        Image: Requested Image object.
    """
    asset_letter = "A"
    if bob_down(frame_num):
        asset_letter = "B"
    return Image.open(get_filename(image_type, f"{asset_name}{asset_letter}"))

def get_2frame_asset(image_type, asset_name, frame_num):
    """Get the Image object for the current 2-frame asset. The second frame is generated rather
    than manually created, as with a custom asset.

    Args:
        image_type (string): Type of image, i.e. 'hairfront', 'eyes'.
        asset_name (string): Asset number, i.e. '00'.
        frame_num (int): Current frame number.

    Returns:
        Image: Requested Image object.
    """
    image = Image.open(get_filename(image_type, asset_name))
    if bob_down(frame_num):
        return translate_image(image, 'down', 1)
    return image

def get_rgba_from_hex(hex_string):
    """Converts hex color string to rgba color tuple.

    Args:
        hex_string (string): hex color string, i.e. 79ede2

    Returns:
        tuple: 4-entry tuple of ints representing rgba, i.e. (121, 237, 226, 255)
    """
    rgb = list(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
    rgb.append(255)
    return tuple(rgb)

def update_palette(before_img, before_colors, after_colors):
    """Recolor a given image with an array of 'before' colors to an array of 'after'.

    Args:
        before_img (Image): Image object with mode 'RGBA' to be recolored.
        before_colors (list(tuple)): RGBA colors that will be recolored, i.e. [(0, 0, 0, 255)]
        after_colors (list(tuples)): RGBA colors to be used for recoloring, i.e. [(1, 1, 1, 255)]

    Returns:
        Image: Recolored Image object.
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

def make_transparent(img) -> Image:
    """Return the image with a transparent background. Transparency is based on what is left as
    the DEFAULT_COLOR from the original Image creation.

    Args:
        img (Image): Image object.

    Returns:
        Image: Image object with a transparent background.
    """
    return update_palette(img, [DEFAULT_COLOR], [TRANSPARENT_COLOR])

def change_color(img, color_dict, default_color, new_color):
    """Recolor an image with a provided palette of colors.

    Args:
        img (Image): Image object.
        color_dict (dict): Dictionary that maps palette name to a string of hex colors.
        default_color (string): Default palette name for the asset, i.e. 'pink'.
        new_color (string): Desired palette name to recolor the asset, i.e. 'orange'.

    Returns:
        Image: Recolored Image object.
    """
    img = img.convert('RGBA')
    before_hexes = color_dict[default_color]
    after_hexes = color_dict[new_color]
    before_rgba = list(map(get_rgba_from_hex, before_hexes.split(",")))
    after_rgba = list(map(get_rgba_from_hex, after_hexes.split(",")))
    return update_palette(img, before_rgba, after_rgba)

def get_frame(frame_num, assets):
    """Assemble a single frame of the gif.

    Args:
        frame_num (int): Current frame number.
        assets (SelectedAssets): SelectedAssets object.

    Returns:
        Image: Frame as an Image object.
    """
    # Get the order that images are layered.
    sorted_layers = assets.get_sorted_layers()
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
    watermark = Image.open(f"{IMAGE_FILE_PREFIX}/images/watermark.png")
    frame.paste(watermark, (0, 0), watermark)
    return frame

def get_gif(assets, current_time):
    """Assemble a list of frames, string them together, and save the gif to output/.

    Args:
        assets (SelectedAssets): SelectedAssets object.
        current_time (string): Full current time string, i.e. '2020-03-16_12:02:08AM'.
    """
    frames = []
    for i in range(32):
        frames.append(get_frame(i, assets))
    frames[0].save(
        f"{OUTPUT_FILE_PREFIX}/output/{current_time}.gif",
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

    Args:
        assets_json (dict): Parsed assets.json file as a dictionary.

    Returns:
        SelectedAssets: SelectedAssets object.
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

def get_preset_asset_list(assets_json, preset):
    assets = SelectedAssets()
    assets.colors = preset['colors']
    assets.images = preset['images']
    return assets

def get_json(assets, current_time):
    """Creates a json file with the generated asset settings along with the same-named gif.

    Args:
        assets (SelectedAssets): SelectedAssets object.
        current_time (string): Full current time string, i.e. '2020-03-16_12:02:08AM'.
    """
    json_filename = f"{OUTPUT_FILE_PREFIX}/output/{current_time}.json"
    json_file = open(json_filename, "w")
    json_file.write(json.dumps(assets.get_json(), indent=2))
    json_file.close()

def load_assets():
    return yaml.safe_load(open(f"{pathlib.Path(__file__).parent.absolute()}/assets.yaml"))

def get_presets():
    assets_yaml = load_assets()
    presets = list(assets_yaml['presets'].keys())
    return presets

def create_gif_preset(preset_name):
    """TBD - Generates a gif icon along with its config json into the outputs/ folder.

    Returns:
        string: full path to the gif result.
    """
    assets_yaml = load_assets()

    preset = assets_yaml['presets'][preset_name]
    gif_assets = get_preset_asset_list(assets_yaml, preset)
    gif_assets.store_json(assets_yaml)

    current_time = datetime.today().strftime("%Y-%m-%d_%I:%M:%S%p")
    get_gif(gif_assets, current_time)
    get_json(gif_assets, current_time)
    return f"{OUTPUT_FILE_PREFIX}/output/{current_time}.gif"

def create_gif_random():
    """TBD - Generates a gif icon along with its config json into the outputs/ folder.

    Returns:
        string: full path to the gif result.
    """
    assets_yaml = load_assets()

    gif_assets = get_random_asset_list(assets_yaml)
    gif_assets.store_json(assets_yaml)

    current_time = datetime.today().strftime("%Y-%m-%d_%I:%M:%S%p")
    get_gif(gif_assets, current_time)
    get_json(gif_assets, current_time)
    return f"{OUTPUT_FILE_PREFIX}/output/{current_time}.gif"
