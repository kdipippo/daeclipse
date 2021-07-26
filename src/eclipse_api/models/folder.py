from .deviation import EclipseDeviation
from .user import EclipseUser

class EclipseFolder:
    def __init__(self, d = None):
        self.folderId = None
        self.gallectionUuid = None
        self.parentId = None
        self.type = None
        self.name = None
        self.description = None
        self.owner = None
        self.commentCount = None
        self.size = None
        self.thumb = None
        self.hasSubfolders = None
        self.totalItemCount = None
        if d is not None and type(d) is dict:
            self.from_dict(d)

    def __repr__(self):
        return self.folderId

    def from_dict(self, d):
        if 'folderId' in d: self.folderId = d['folderId']
        if 'gallectionUuid' in d: self.gallectionUuid = d['gallectionUuid']
        if 'parentId' in d: self.parentId = d['parentId']
        if 'type' in d: self.type = d['type']
        if 'name' in d: self.name = d['name']
        if 'description' in d: self.description = d['description']
        if 'owner' in d:
            self.owner = EclipseUser()
            self.owner.from_dict(d['owner'])
        if 'commentCount' in d: self.commentCount = d['commentCount']
        if 'size' in d: self.size = d['size']
        if 'thumb' in d:
            self.thumb = EclipseDeviation()
            self.thumb.from_dict(d['thumb'])
        if 'hasSubfolders' in d: self.hasSubfolders = d['hasSubfolders']
        if 'totalItemCount' in d: self.totalItemCount = d['totalItemCount']
