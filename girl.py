from PIL import Image
from PIL import GifImagePlugin
import random

def translateOnePixelDown(image):
  transMatrix = [1,0,0,0,1,0]
  # matrix[2] left/right (i.e. 5/-5)
  # matrix[5] up/down    (i.e. 5/-5)
  transMatrix[5] = -1
  return image.transform(image.size, Image.AFFINE, tuple(transMatrix))

# assets that are static
def getStaticAsset(assetName):
  fileName = f"test/{assetName}.png"
  return Image.open(fileName)

# assets where all the frames are stored vs. generated
def getCustomAsset(assetName, frameNum):
  fileName = f"test/{assetName}{frameNum}.png"
  return Image.open(fileName)

# assets that bob up and down, second frame is generated
def get2FrameAsset(assetName, frameNum):
  fileName = f"test/{assetName}.png"
  image = Image.open(fileName)
  if frameNum % 2 == 0:
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

skinColors = {
  "white": "8c2323,c3412d,e66e46,f5a56e,ffd2a5",
  "black": "370a14,5a1423,8c3c32,b26247,dc9b78",
  "pale":  "6e2850,96465f,be6973,e69b96,ffcdb4",
}
hairColors = {
  "pink":   "4b143c,820a64,b4236e,e65078",
  "orange": "7d0041,aa143c,d72d2d,f06923"
}

def changeColor(img, colorDict, defaultColor, newColor):
  img = img.convert('RGBA')
  beforeHexes = colorDict[defaultColor]
  afterHexes = colorDict[newColor]
  beforeRGBAs = list(map(getRGBAFromHex, beforeHexes.split(",")))
  afterRGBAs = list(map(getRGBAFromHex, afterHexes.split(",")))
  return updatePalette(img, beforeRGBAs, afterRGBAs)




def getFrame(frameNum, skinColor, hairColor):
  base = getCustomAsset("base", frameNum)
  base = changeColor(base, skinColors, 'white', skinColor)
  
  head = get2FrameAsset("head1", frameNum)
  head = changeColor(head, skinColors, 'white', skinColor)
  base.paste(head, (0, 0), head)

  socks = getStaticAsset("socks")
  base.paste(socks, (0, 0), socks)

  outfit = getCustomAsset("outfit", frameNum)
  base.paste(outfit, (0, 0), outfit)

  hair = get2FrameAsset("hair", frameNum)
  hair = changeColor(hair, hairColors, 'pink', hairColor)
  base.paste(hair, (0, 0), hair)
  return base

def getGif():
  # pick colors
  skinColor = random.choice(list(skinColors.keys()))
  print(f"Skin color will be '{skinColor}'")
  hairColor = random.choice(list(hairColors.keys()))
  print(f"Hair color will be '{hairColor}'")
  skinColor = 'black'
  hairColor = 'orange'

  # generate frames
  frames = []
  for i in range(1, 3):
    frames.append(getFrame(i, skinColor, hairColor))
  frames[0].save(
    'GIRL2.gif',
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=500,
    loop=0
  )

if __name__ == "__main__":
  # assembleGif()
  # updatePalette()
  # assembleUpdatedGif()
  getGif()
