from PIL import Image
from PIL import GifImagePlugin

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


def getFrame(frameNum):
  base = getCustomAsset("base", frameNum)
  
  head = get2FrameAsset("head1", frameNum)
  base.paste(head, (0, 0), head)

  socks = getStaticAsset("socks")
  base.paste(socks, (0, 0), socks)

  outfit = getCustomAsset("outfit", frameNum)
  base.paste(outfit, (0, 0), outfit)

  hair = get2FrameAsset("hair", frameNum)
  base.paste(hair, (0, 0), hair)
  return base

def getGif():
  frames = []
  frames.append(getFrame(1))
  frames.append(getFrame(2))
  frames[0].save(
    'GIRL.gif',
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
