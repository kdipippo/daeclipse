"""Model to represent DeviantArt Eclipse Deviation."""

from stats import EclipseStats
from user import EclipseUser

class EclipseDeviation:
    """Model to represent DeviantArt Eclipse Deviation."""

    def __init__(self, input_dict = None):
        self.deviation_id = None
        self.type = None
        self.type_id = None
        self.print_id = None
        self.url = None
        self.title = None
        self.is_journal = None
        self.is_video = None
        self.is_purchasable = None
        self.is_favouritable = None
        self.published_time = None
        self.is_text_editable = None
        self.legacy_text_edit_url = None
        self.is_shareable = None
        self.is_commentable = None
        self.is_favourited = None
        self.is_deleted = None
        self.is_mature = None
        self.is_downloadable = None
        self.is_antisocial = None
        self.is_blocked = None
        self.is_published = None
        self.is_daily_deviation = None
        self.has_private_comments = None
        self.block_reasons = None
        self.author = None
        self.stats = None
        self.media = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def __repr__(self):
        return self.deviation_id

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviation fields.
        """
        if 'deviationId' in input_dict:
            self.deviation_id = input_dict['deviationId']
        if 'type' in input_dict:
            self.type = input_dict['type']
        if 'typeId' in input_dict:
            self.type_id = input_dict['typeId']
        if 'printId' in input_dict:
            self.print_id = input_dict['printId']
        if 'url' in input_dict:
            self.url = input_dict['url']
        if 'title' in input_dict:
            self.title = input_dict['title']
        if 'isJournal' in input_dict:
            self.is_journal = input_dict['isJournal']
        if 'isVideo' in input_dict:
            self.is_video = input_dict['isVideo']
        if 'isPurchasable' in input_dict:
            self.is_purchasable = input_dict['isPurchasable']
        if 'isFavouritable' in input_dict:
            self.is_favouritable = input_dict['isFavouritable']
        if 'publishedTime' in input_dict:
            self.published_time = input_dict['publishedTime']
        if 'isTextEditable' in input_dict:
            self.is_text_editable = input_dict['isTextEditable']
        if 'legacyTextEditUrl' in input_dict:
            self.legacy_text_edit_url = input_dict['legacyTextEditUrl']
        if 'isShareable' in input_dict:
            self.is_shareable = input_dict['isShareable']
        if 'isCommentable' in input_dict:
            self.is_commentable = input_dict['isCommentable']
        if 'isFavourited' in input_dict:
            self.is_favourited = input_dict['isFavourited']
        if 'isDeleted' in input_dict:
            self.is_deleted = input_dict['isDeleted']
        if 'isMature' in input_dict:
            self.is_mature = input_dict['isMature']
        if 'isDownloadable' in input_dict:
            self.is_downloadable = input_dict['isDownloadable']
        if 'isAntisocial' in input_dict:
            self.is_antisocial = input_dict['isAntisocial']
        if 'isBlocked' in input_dict:
            self.is_blocked = input_dict['isBlocked']
        if 'isPublished' in input_dict:
            self.is_published = input_dict['isPublished']
        if 'isDailyDeviation' in input_dict:
            self.is_daily_deviation = input_dict['isDailyDeviation']
        if 'hasPrivateComments' in input_dict:
            self.has_private_comments = input_dict['hasPrivateComments']
        if 'blockReasons' in input_dict:
            self.block_reasons = input_dict['blockReasons']
        if 'author' in input_dict:
            self.author = EclipseUser()
            self.author.from_dict(input_dict['author'])
        if 'stats' in input_dict:
            self.stats = EclipseStats()
            self.stats.from_dict(input_dict['stats'])
        if 'media' in input_dict:
            self.media = input_dict['media']
