"""Generate a 50x50 animated pixel gif, either randomly or based on presets."""

import json
import pathlib
import random
from datetime import datetime

import yaml
from PIL import Image

from gif_generator.selected_assets_class import SelectedAssets

# Used for the background to be erased when the image is made transparent.
# Set to a muted green color that does not coincide with the pixel art palette.

DEFAULT_COLOR = (83, 106, 89, 255)
TRANSPARENT_COLOR = (255, 255, 255, 0)

IMAGE_FILE_PREFIX = pathlib.Path(__file__).parent.absolute()
OUTPUT_FILE_PREFIX = pathlib.Path(__file__).parent.parent.absolute()

FRAMES_TOTAL = 32
EYES_CLOSING_FRAMES = (25, 29)
EYES_NEARLY_CLOSED_FRAMES = (26, 28)
EYES_CLOSED_FRAMES = (27)


def bob_down(frame_num):
    """Return true if sprite is bobbing down.

    Args:
        frame_num (int): Current frame number.

    Returns:
        boolean: True if sprite is bobbing down, false if bobbing up.
    """
    return frame_num % 4 != 1 and frame_num % 4 != 2


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
    if direction == 'left':
        trans_matrix[2] += pixels
    elif direction == 'right':
        trans_matrix[2] -= pixels
    elif direction == 'up':
        trans_matrix[5] += pixels
    elif direction == 'down':
        trans_matrix[5] -= pixels
    return image.transform(
        image.size,
        Image.AFFINE,
        tuple(trans_matrix),
        fillcolor=DEFAULT_COLOR,
    )


def get_filename(image_type, asset_name):
    """Return path to the given image asset.

    Args:
        image_type (string): Type of image, i.e. 'hairfront', 'eyes'.
        asset_name (string): Asset name, may have position letter, i.e. '00A'.

    Returns:
        string: Path to image asset.
    """
    return '{0}/images/{1}/{1}{2}.png'.format(
        IMAGE_FILE_PREFIX,
        image_type,
        asset_name,
    )


def get_custom_asset(image_type, asset_name, frame_num):
    """Get the Image object for a custom asset.

    Args:
        image_type (string): Type of image, i.e. 'hairfront', 'eyes'.
        asset_name (string): Asset number, i.e. '00'.
        frame_num (int): Current frame number.

    Returns:
        Image: Requested Image object.
    """
    asset_letter = 'A'
    if bob_down(frame_num):
        asset_letter = 'B'
    return Image.open(get_filename(image_type, '{0}{1}'.format(
        asset_name,
        asset_letter,
    )))


def get_2frame_asset(image_type, asset_name, frame_num):
    """Get Image object for a 2-frame asset.

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
    """Convert hex color string to rgba color tuple.

    Args:
        hex_string (string): hex color string, i.e. 79ede2.

    Returns:
        tuple: 4-entry int tuple representing rgba, i.e. (121, 237, 226, 255).
    """
    rgb = [int(hex_string[index:index+2], 16) for index in (0, 2, 4)]
    rgb.append(255)
    return tuple(rgb)


def update_palette(before_img, before_colors, after_colors):
    """Recolor given image with array of 'before' colors to array of 'after'.

    Args:
        before_img (Image): Image object with mode 'RGBA' to be recolored.
        before_colors (list(tuple)): RGBA colors that will be recolored.
        after_colors (list(tuples)): RGBA colors to be used for recoloring.

    Returns:
        Image: Recolored Image object.
    """
    before_pixelmap = before_img.load()

    after_img = Image.new('RGBA', before_img.size)
    after_pixelmap = after_img.load()
    for width in range(after_img.size[0]):
        for height in range(after_img.size[1]):
            curr_color = before_pixelmap[width, height]
            if curr_color in before_colors:
                after_index = before_colors.index(curr_color)
                after_pixelmap[width, height] = after_colors[after_index]
            else:
                after_pixelmap[width, height] = before_pixelmap[width, height]
    return after_img


def make_transparent(img) -> Image:
    """Return image with a transparent background.

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
        color_dict (dict): Dict that maps palette name to string of hex colors.
        default_color (string): Before palette name for asset, i.e. 'pink'.
        new_color (string): After palette name to recolor asset, i.e. 'orange'.

    Returns:
        Image: Recolored Image object.
    """
    img = img.convert('RGBA')
    before_hexes = color_dict[default_color]
    after_hexes = color_dict[new_color]
    before_rgba = list(map(get_rgba_from_hex, before_hexes.split(',')))
    after_rgba = list(map(get_rgba_from_hex, after_hexes.split(',')))
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

        if image_type == 'eyes':
            '{0}{1}'.format(
                asset_name,
                suffix_blinking_frame(frame_num, asset_name),
            )

        if image_info['type'] == '2frame':
            image_layer = get_2frame_asset(image_type, asset_name, frame_num)
        elif image_info['type'] == 'custom':
            image_layer = get_custom_asset(image_type, asset_name, frame_num)

        if 'recolor' in image_info:
            for recolor in image_info.get('recolor'):
                color_dict = assets.json['colorHexes'][recolor]['options']
                default_color = assets.json['colorHexes'][recolor]['default']
                new_color = assets.colors[recolor]
                image_layer = change_color(
                    image_layer,
                    color_dict,
                    default_color,
                    new_color,
                )
        frame.paste(image_layer, (0, 0), image_layer)

    frame = translate_image(frame, 'left', 5)
    frame = make_transparent(frame)
    watermark = Image.open(
        '{0}/images/watermark.png'.format(IMAGE_FILE_PREFIX),
    )
    frame.paste(watermark, (0, 0), watermark)
    return frame


def suffix_blinking_frame(frame_num, asset_name):
    """Get the frame letter based on blinking position.

    Args:
        frame_num ([type]): [description]
        asset_name ([type]): [description]

    Returns:
        string: eye frame suffix for given frame number.
    """
    if frame_num in EYES_CLOSING_FRAMES:
        return 'B'  # Suffix for frame with eyes closing.
    if frame_num in EYES_NEARLY_CLOSED_FRAMES:
        return 'C'  # Suffix for frame with eyes nearly closed.
    if frame_num in EYES_CLOSED_FRAMES:
        return 'D'  # Suffix for frame with eyes closed.
    return 'A'  # Suffix for frame with eyes open.


def save_gif(assets, current_time):
    """Assemble and combine list of frames and save gif.

    Args:
        assets (SelectedAssets): SelectedAssets object.
        current_time (string): Current time, i.e. '2020-03-16_12:02:08AM'.
    """
    frames = []
    for frame_num in range(FRAMES_TOTAL):
        frames.append(get_frame(frame_num, assets))
    frames[0].save(
        '{0}/{1}.gif'.format(OUTPUT_FILE_PREFIX, current_time),
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=100,
        loop=0,
        transparency=0,
        disposal=2,
    )


def get_random_asset_list(assets_json):
    """Randomize and return the list of colors and components.

    Args:
        assets_json (dict): Parsed assets.json file as a dictionary.

    Returns:
        SelectedAssets: SelectedAssets object.
    """
    assets = SelectedAssets()
    color_types = list(assets_json['colorHexes'].keys())
    for color_type in color_types:
        assets.add_color(color_type, random.choice(  # noqa: S311
            list(assets_json['colorHexes'][color_type]['options'].keys()),
        ))
    image_types = list(assets_json['imageTypes'].keys())
    for image_type in image_types:
        coin_toss = random.random()  # noqa: S311
        if coin_toss < assets_json['imageTypes'][image_type]['probability']:
            selected_num = random.randint(  # noqa: S311
                0,
                assets_json['imageTypes'][image_type]['count'] - 1,
            )
            assets.add_image(image_type, selected_num)
    return assets


def get_preset_asset_list(preset):
    """Convert preset dict to SelectedAssets object.

    Args:
        preset (dict): Dict containing colors and images specification.

    Returns:
        SelectedAssets: SelectedAssets object.
    """
    assets = SelectedAssets()
    assets.colors = preset['colors']
    assets.images = preset['images']
    return assets


def save_json(assets, current_time):
    """Create a json file with the generated asset settings.

    Args:
        assets (SelectedAssets): SelectedAssets object.
        current_time (string): Current time, i.e. '2020-03-16_12:02:08AM'.
    """
    filename = '{0}/{1}.json'.format(OUTPUT_FILE_PREFIX, current_time)
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(assets.as_json(), indent=2))


def load_assets():
    """Return the contents of assets.yaml as a dict.

    Returns:
        dict: assets.yaml contents.
    """
    yaml_path = '{0}/assets.yaml'.format(
        pathlib.Path(__file__).parent.absolute(),
    )
    with open(yaml_path) as yaml_file:
        return yaml.safe_load(yaml_file)


def get_presets():
    """Return the list of preset names.

    Returns:
        string[]: List of preset names stored in assets.yaml.
    """
    assets_yaml = load_assets()
    presets = list(assets_yaml['presets'].keys())
    return presets


def create_gif_preset(preset_name):
    """Generate an animated pixel icon gif based on a stored preset.

    Args:
        preset_name (string): Preset name.

    Returns:
        string: Full path to gif result.
    """
    assets_yaml = load_assets()

    preset = assets_yaml['presets'][preset_name]
    gif_assets = get_preset_asset_list(preset)
    gif_assets.store_json(assets_yaml)

    current_time = datetime.today().strftime('%Y-%m-%d_%I:%M:%S%p')
    save_gif(gif_assets, current_time)
    save_json(gif_assets, current_time)
    return '{0}/{1}.gif'.format(OUTPUT_FILE_PREFIX, current_time)


def create_gif_random():
    """Generate an animated pixel icon gif with randomized assets.

    Returns:
        string: Full path to gif result.
    """
    assets_yaml = load_assets()

    gif_assets = get_random_asset_list(assets_yaml)
    gif_assets.store_json(assets_yaml)

    current_time = datetime.today().strftime('%Y-%m-%d_%I:%M:%S%p')
    save_gif(gif_assets, current_time)
    save_json(gif_assets, current_time)
    return '{0}/{1}.gif'.format(OUTPUT_FILE_PREFIX, current_time)
