#!/usr/bin/env python
"""This script generates a 50x50 animated gif either randomly or with provided
color and image information via a json file."""

from PIL import Image
from PIL import GifImagePlugin
import json
import random
from datetime import datetime

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

def getRGBAFromHex(hex):
    """Converts hex color string to rgba color tuple.

    Arguments:
        hex {string} -- hex color string, i.e. 79ede2

    Returns:
        typle -- 4-entry tuple of ints representing rgba, i.e. (121, 237, 226, 255)
    """
    rgb = list(int(hex[i:i+2], 16) for i in (0, 2, 4))
    rgb.append(255)
    return tuple(rgb)

# im needs to be converted to RGBA
def updatePalette(beforeImg, beforeColors, afterColors):
    beforePixelMap = beforeImg.load()

    afterImg = Image.new('RGBA', beforeImg.size)
    afterPixelMap = afterImg.load()
    for i in range(afterImg.size[0]):
        for j in range(afterImg.size[1]):
            currColor = beforePixelMap[i, j]
            if currColor in beforeColors:
                afterIndex = beforeColors.index(currColor)
                afterPixelMap[i, j] = afterColors[afterIndex]
            else:
                afterPixelMap[i, j] = beforePixelMap[i, j]
    return afterImg

def makeTransparent(img):
    img = updatePalette(img, [DEFAULT_COLOR], [TRANSPARENT_COLOR])
    return img

def changeColor(img, colorDict, defaultColor, newColor):
    img = img.convert('RGBA')
    beforeHexes = colorDict[defaultColor]
    afterHexes = colorDict[newColor]
    beforeRGBAs = list(map(getRGBAFromHex, beforeHexes.split(",")))
    afterRGBAs = list(map(getRGBAFromHex, afterHexes.split(",")))
    return updatePalette(img, beforeRGBAs, afterRGBAs)

def getFrame(frameNum, assets):
    # get the order that images are layered
    sortedLayers = sorted(assetsJson['imageTypes'].items(), key=lambda x: x[1]['order'])
    frame = Image.new('RGBA', (50, 50), color=DEFAULT_COLOR)
    for layer in sortedLayers:
        imageType = layer[0]
        imageInfo = layer[1]
        if imageType not in assets.images:
            continue
        assetName = assets.images[imageType]
        # section for handling blinking animation
        if imageType == "eyes":
            if frameNum == 29 or frameNum == 25:
                assetName += "B"
            elif frameNum == 28 or frameNum == 26:
                assetName += "C"
            elif frameNum == 27:
                assetName += "D"
            else:
                assetName += "A"
        if imageInfo['type'] == "2frame":
            imageLayer = get_2frame_asset(imageType, assetName, frameNum)
        elif imageInfo['type'] == "custom":
            imageLayer = get_custom_asset(imageType, assetName, frameNum)

        if 'recolor' in imageInfo:
            for recolorType in imageInfo['recolor']:
                # variables are suffering
                colorDict = assets.json['colorHexes'][recolorType]['options']
                defaultColor = assets.json['colorHexes'][recolorType]['default']
                newColor = assets.colors[recolorType]
                imageLayer = changeColor(imageLayer, colorDict, defaultColor, newColor)
        frame.paste(imageLayer, (0, 0), imageLayer)

    frame = translate_image(frame, 'left', 5)
    frame = makeTransparent(frame)
    watermark = Image.open("images/watermark.png")
    frame.paste(watermark, (0, 0), watermark)
    return frame

# assets is a SelectedAssets object
def getGif(assets, currentTime):
    # generate frames
    frames = []
    for i in range(32):
        frames.append(getFrame(i, assets))
    frames[0].save(f'output/{currentTime}.gif', format='GIF', append_images=frames[1:],
                   save_all=True, duration=100, loop=0, transparency=0, disposal=2)

# returns the list of colors and components for the generated gif
def getAssetList(assetsJson):
    assets = SelectedAssets()
    colorTypes = list(assetsJson['colorHexes'].keys())
    for colorType in colorTypes:
        selectedColor = random.choice(list(assetsJson['colorHexes'][colorType]['options'].keys()))
        assets.add_color(colorType, selectedColor)
    imageTypes = list(assetsJson['imageTypes'].keys())
    for imageType in imageTypes:
        coinToss = random.random()
        if coinToss < assetsJson['imageTypes'][imageType]['probability']:
            selectedNum = random.randint(0, assetsJson['imageTypes'][imageType]['count']-1)
            assets.add_image(imageType, selectedNum)
    return assets

def get_json(assets, currentTime):
    f = open(f'output/{currentTime}.json', "w")
    f.write(json.dumps(assets.get_json(), indent=2))
    f.close()

if __name__ == "__main__":
    with open('assets.json', 'r') as f:
        assetsJson = json.load(f)
    assets = getAssetList(assetsJson)
    assets.store_json(assetsJson)

    with open('presets/rin.json', 'r') as f:
        rinJson = json.load(f)
    assets.debug_override(rinJson)

    assets.debug()
    currentTime = datetime.today().strftime("%Y-%m-%d_%I:%M:%S%p")
    getGif(assets, currentTime)
    get_json(assets, currentTime)
