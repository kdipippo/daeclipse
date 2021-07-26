from .stats import EclipseStats
from .user import EclipseUser

class EclipseDeviation:
    def __init__(self, d = None):
        self.deviationId = None
        self.type = None
        self.typeId = None
        self.printId = None
        self.url = None
        self.title = None
        self.isJournal = None
        self.isVideo = None
        self.isPurchasable = None
        self.isFavouritable = None
        self.publishedTime = None
        self.isTextEditable = None
        self.legacyTextEditUrl = None
        self.isShareable = None
        self.isCommentable = None
        self.isFavourited = None
        self.isDeleted = None
        self.isMature = None
        self.isDownloadable = None
        self.isAntisocial = None
        self.isBlocked = None
        self.isPublished = None
        self.isDailyDeviation = None
        self.hasPrivateComments = None
        self.blockReasons = None
        self.author = None
        self.stats = None
        self.media = None
        if d is not None and type(d) is dict:
            self.from_dict(d)

    def __repr__(self):
        return self.deviationId
    
    def from_dict(self, d):
        if 'deviationId' in d: self.deviationId = d['deviationId']
        if 'type' in d: self.type = d['type']
        if 'typeId' in d: self.typeId = d['typeId']
        if 'printId' in d: self.printId = d['printId']
        if 'url' in d: self.url = d['url']
        if 'title' in d: self.title = d['title']
        if 'isJournal' in d: self.isJournal = d['isJournal']
        if 'isVideo' in d: self.isVideo = d['isVideo']
        if 'isPurchasable' in d: self.isPurchasable = d['isPurchasable']
        if 'isFavouritable' in d: self.isFavouritable = d['isFavouritable']
        if 'publishedTime' in d: self.publishedTime = d['publishedTime']
        if 'isTextEditable' in d: self.isTextEditable = d['isTextEditable']
        if 'legacyTextEditUrl' in d: self.legacyTextEditUrl = d['legacyTextEditUrl']
        if 'isShareable' in d: self.isShareable = d['isShareable']
        if 'isCommentable' in d: self.isCommentable = d['isCommentable']
        if 'isFavourited' in d: self.isFavourited = d['isFavourited']
        if 'isDeleted' in d: self.isDeleted = d['isDeleted']
        if 'isMature' in d: self.isMature = d['isMature']
        if 'isDownloadable' in d: self.isDownloadable = d['isDownloadable']
        if 'isAntisocial' in d: self.isAntisocial = d['isAntisocial']
        if 'isBlocked' in d: self.isBlocked = d['isBlocked']
        if 'isPublished' in d: self.isPublished = d['isPublished']
        if 'isDailyDeviation' in d: self.isDailyDeviation = d['isDailyDeviation']
        if 'hasPrivateComments' in d: self.hasPrivateComments = d['hasPrivateComments']
        if 'blockReasons' in d: self.blockReasons = d['blockReasons']
        if 'author' in d:
            self.author = EclipseUser()
            self.author.from_dict(d['author'])
        if 'stats' in d:
            self.stats = EclipseStats()
            self.stats.from_dict(d['stats'])
        if 'media' in d: self.media = d['media']
