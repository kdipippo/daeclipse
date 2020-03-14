from PIL import Image
from PIL import GifImagePlugin
import json
import random

class SelectedAssets:
  colors = {}
  images = {}
  json = None
  def addColor(self, colorType, selectedType):
    self.colors[colorType] = selectedType
  def addImage(self, imageType, imageNum):
    self.images[imageType] = "{:02d}".format(imageNum)
  def storeJson(self, assetsJson):
    self.json = assetsJson
  def debugOverride(self, overrideColors, overrideImages):
    self.colors = overrideColors
    self.images = overrideImages
  def debug(self):
    for color in self.colors.keys():
      print(f"COLOR {color} = {self.colors[color]}")
    for image in self.images.keys():
      print(f"IMAGE {image} = {self.images[image]}")

# returns true if the character should bob down, false otherwise
def bobDown(frameNum):
  if frameNum % 4 == 1 or frameNum % 4 == 2:
    return False
  return True

def translateOnePixelDown(image):
  transMatrix = [1,0,0,0,1,0]
  # matrix[2] left/right (i.e. 5/-5)
  # matrix[5] up/down    (i.e. 5/-5)
  transMatrix[5] = -1
  return image.transform(image.size, Image.AFFINE, tuple(transMatrix))

def getFilename(imageType, assetName):
  filename = f"images/{imageType}/{imageType}{assetName}.png"
  # print(filename)
  return filename

# assets that are static
def getStaticAsset(imageType, assetName):
  return Image.open(getFilename(imageType, assetName))

# assets where all the frames are stored vs. generated
def getCustomAsset(imageType, assetName, frameNum):
  assetLetter = "A"
  if bobDown(frameNum):
    assetLetter = "B"
  return Image.open(getFilename(imageType, f"{assetName}{assetLetter}"))

# assets that bob up and down, second frame is generated
def get2FrameAsset(imageType, assetName, frameNum):
  image = Image.open(getFilename(imageType, assetName))
  if bobDown(frameNum):
    return translateOnePixelDown(image)
  return image

def getRGBAFromHex(hex):
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
      currColor = beforePixelMap[i,j]
      if currColor in beforeColors:
        afterIndex = beforeColors.index(currColor)
        afterPixelMap[i,j] = afterColors[afterIndex]
      else:
        afterPixelMap[i,j] = beforePixelMap[i,j]
  return afterImg

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
  frame = Image.new('RGBA', (50,50), color=(83,106,89,255))
  for layer in sortedLayers:
    imageType = layer[0]
    imageInfo = layer[1]
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
      imageLayer = get2FrameAsset(imageType, assetName, frameNum)
    elif imageInfo['type'] == "custom":
      imageLayer = getCustomAsset(imageType, assetName, frameNum)
    
    if 'recolor' in imageInfo:
      for recolorType in imageInfo['recolor']:
        # variables are suffering
        colorDict = assets.json['colorHexes'][recolorType]['options']
        defaultColor = assets.json['colorHexes'][recolorType]['default']
        newColor = assets.colors[recolorType]
        imageLayer = changeColor(imageLayer, colorDict, defaultColor, newColor)
    frame.paste(imageLayer, (0, 0), imageLayer)
  return frame

# assets is a SelectedAssets object
def getGif(assets):
  # generate frames
  frames = []
  for i in range(32):
    frames.append(getFrame(i, assets))
  frames[0].save('GIRL3.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)

# returns the list of colors and components for the generated gif
def getAssetList(assetsJson):
  assets = SelectedAssets()
  colorTypes = list(assetsJson['colorHexes'].keys())
  for colorType in colorTypes:
    selectedColor = random.choice(list(assetsJson['colorHexes'][colorType]['options'].keys()))
    assets.addColor(colorType, selectedColor)
  imageTypes = list(assetsJson['imageTypes'].keys())
  for imageType in imageTypes:
    selectedNum = random.randint(0, assetsJson['imageTypes'][imageType]['count']-1)
    assets.addImage(imageType, selectedNum)
  return assets

if __name__ == "__main__":
  overrideColors = {'skin': 'red', 'hair': 'white', 'eyes': 'teal'}
  overrideImages = {'base': '00', 'hair_back': '00', 'head': '00', 'eyes': '00', 'outfit': '00', 'hair_front': '01'}

  # assembleGif()
  # updatePalette()
  # assembleUpdatedGif()
  with open('assets.json', 'r') as f:
    assetsJson = json.load(f)
  assets = getAssetList(assetsJson)
  assets.storeJson(assetsJson)

  assets.debugOverride(overrideColors, overrideImages)

  assets.debug()
  getGif(assets)
