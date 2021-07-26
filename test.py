from __future__ import print_function
import json
from json import JSONEncoder
from types import SimpleNamespace as Namespace

class Folder:
    def __init__(self, folderId, gallectionUuid, parentId, type, name, description, owner, commentCount, size, thumb, hasSubfolders, totalItemCount):
        self.folderId = folderId
        self.gallectionUuid = gallectionUuid
        self.parentId = parentId
        self.type = type
        self.name = name
        self.description = description
        self.owner = owner
        self.commentCount = commentCount
        self.size = size
        self.thumb = thumb
        self.hasSubfolders = hasSubfolders
        self.totalItemCount = totalItemCount

class Owner:
    def __init__(self, userId, useridUuid, username, usericon, type, isWatching, isNewDeviant):
        self.userId = userId
        self.useridUuid = useridUuid
        self.username = username
        self.usericon = usericon
        self.type = type
        self.isWatching = isWatching
        self.isNewDeviant = isNewDeviant


f = open('folder.json',)
folderData = json.load(f)

folderJsonData = json.dumps(folderData, indent=4, cls=StudentEncoder)
folderObj = json.loads(folderJsonData, object_hook=lambda d: Namespace(**d))
print(folderObj.name)
print(folderObj.owner)
