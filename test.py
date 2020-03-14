import json

def getOrder(images):
  return None
  # return images[imageType]['order']

def test():
  with open('assets.json', 'r') as f:
    assetsJson = json.load(f)
  sortedLayers = sorted(assetsJson['imageTypes'].items(), key=lambda x: x[1]['order'])
  for layer in sortedLayers:
    print(layer)


'''
  imageTypesBefore = list(assetsJson['imageTypes'].keys())
  images = list(assetsJson['imageTypes'])
  imageTypesAfter = sorted(images, key=getOrder)

  for imageType in imageTypesBefore:
    print(f"{images[imageType]['order']} - {imageType}")
  print("------")
  for imageType in imageTypesAfter:
    print(f"{images[imageType]['order']} - {imageType}")
'''

test()
