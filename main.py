from PIL import Image
from PIL import GifImagePlugin

'''
Notes:
1 - transparent=0 refers to the palette index. There's no way to figure out the palette in order to determine
    the index, so the safer bet is to set the background to a color that should never be used (i.e. a gross green).
    Then, if the top left corner is left transparent, the resulting gifs should turn out alright. Have each frame
    stored with the green background by default (if not just setting it as part of the palette change).
2 - Dedicate different color groups for substitutions. Skin tones should have a reserved number of shades, hair tones, etc.
3 - This current BEFORE and AFTER prototype has its flaws, i.e. the nose highlight is pure white. Changing that white
    will result in changing all parts of the picture. Future white shines in the final product should still be designated
    with different blocking tones.

TODO
I started trying to get the handbag to paste on top of the white girl version, but
I think it's better to try to get a more exact replica of what the templating system
will be:
- Determine style / concept for pixel art.
- Block it into the color theme groups, with the bg set to gross green.
- Base can have bg green, layers on top should be transparent
'''

def assembleGif():
  # How many times each frame is repeated
  frameSpeed = {
    0: 1,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 11,
  }

  frames = []
  for frameNum in range(7):
    im = Image.open("frame_" + str(frameNum) + ".png")
    for i in range(frameSpeed[frameNum]):
      frames.append(im)
  frames[0].save('BEFORE.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)

def updatePalette(fileName):
  paleToTan = {
    (0,0,0,0): (40,54,48,255), # changing transparent background to solid color
    (255,251,245,255): (236,191,169,255),  # skin tone
    (255,225,214,255): (238,170,135,255),  # neck shading
    (255,200,176,255): (240,138,116,255),  # darker neck shading
    (255,185,182,255): (246,129,141,255), # dark cheek
    (255,199,196,255): (255,158,168,255), # cheek
    (255,210,208,255): (255,158,168,255), # lighter cheek
    (255,225,223,255): (255,179,187,255), # lightest cheek
    (255,225,223,255): (255,204,210,255) # cheek shine
  }
  # name = "frame_test.png"
  # out = "frame_output.png"
  im = Image.open(fileName).convert('RGBA')
  pixelMap = im.load()

  img = Image.new('RGBA', im.size)
  pixelsNew = img.load()
  for i in range(img.size[0]):
    for j in range(img.size[1]):
      # print(pixelMap[i,j])
      # if 205 in pixelMap[i,j]:
      if pixelMap[i,j] in paleToTan:
        # pixelsMap[i,j] = (0,0,0,255)
        pixelsNew[i,j] = paleToTan[pixelMap[i,j]]
      else:
        pixelsNew[i,j] = pixelMap[i,j]
  return img

def assembleUpdatedGif():
  # How many times each frame is repeated
  frameSpeed = {
    0: 1,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 11,
  }

  frames = []
  for frameNum in range(7):
    im = updatePalette("frame_" + str(frameNum) + ".png")
    for i in range(frameSpeed[frameNum]):
      frames.append(im)
  frames[0].save('AFTER.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0, transparency=0)

def mergeImages():
  handbag = "handbag.png"
  base = "frame_test.png"
  background = Image.open(base)
  foreground = Image.open(handbag)

  background.paste(foreground, (0, 0), foreground)
  background.show()

if __name__ == "__main__":
  # assembleGif()
  # updatePalette()
  # assembleUpdatedGif()
  mergeImages()
