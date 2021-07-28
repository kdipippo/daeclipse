"""Model to represent DeviantArt Eclipse Deviation."""

from daeclipse.models.gruser import EclipseGruser
from daeclipse.models.stats import EclipseStats


class EclipseDeviation(object):  # noqa: WPS230
    """Model to represent DeviantArt Eclipse Deviation."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviation.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviation class attrs.
        """
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
        self.extended = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def __repr__(self):
        """Representation of EclipseDeviation.

        Returns:
            string: EclipseDeviation representation.
        """
        return self.deviation_id

    def from_dict(self, input_dict):  # noqa: WPS231
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviation fields.
        """
        if input_dict is None:
            return
        self.deviation_id = input_dict.get('deviationId')
        self.type = input_dict.get('type')
        self.type_id = input_dict.get('typeId')
        self.print_id = input_dict.get('printId')
        self.url = input_dict.get('url')
        self.title = input_dict.get('title')
        self.is_journal = input_dict.get('isJournal')
        self.is_video = input_dict.get('isVideo')
        self.is_purchasable = input_dict.get('isPurchasable')
        self.is_favouritable = input_dict.get('isFavouritable')
        self.published_time = input_dict.get('publishedTime')
        self.is_text_editable = input_dict.get('isTextEditable')
        self.legacy_text_edit_url = input_dict.get('legacyTextEditUrl')
        self.is_shareable = input_dict.get('isShareable')
        self.is_commentable = input_dict.get('isCommentable')
        self.is_favourited = input_dict.get('isFavourited')
        self.is_deleted = input_dict.get('isDeleted')
        self.is_mature = input_dict.get('isMature')
        self.is_downloadable = input_dict.get('isDownloadable')
        self.is_antisocial = input_dict.get('isAntisocial')
        self.is_blocked = input_dict.get('isBlocked')
        self.is_published = input_dict.get('isPublished')
        self.is_daily_deviation = input_dict.get('isDailyDeviation')
        self.has_private_comments = input_dict.get('hasPrivateComments')
        self.block_reasons = input_dict.get('blockReasons')
        self.author = EclipseGruser(input_dict.get('author'))
        self.stats = EclipseStats(input_dict.get('stats'))
        self.media = input_dict.get('media')

class Extended(object):
    def __init__(self):
        self.deviation_uuid = input_dict.get('deviationUuid')
        self.can_user_add_to_group = input_dict.get('canUserAddToGroup')
        self.groupListUrl = input_dict.get('groupListUrl')
        self.description = input_dict.get('description')
        self.originalFile = FileSpecs(input_dict.get('originalFile'))
        self.license = input_dict.get('license')
        self.download = FileSpecs(input_dict.get('download'))
        self.related_streams = RelatedStreams(input_dict.get('relatedStreams'))
        self.stats = ExtendedStats(input_dict.get('stats'))
        self.report_url = input_dict.get('reportUrl')


def FileSpecs(object):
    def __init__(self):
        self.type = input_dict.get('type')
        self.width = input_dict.get('width')
        self.height = input_dict.get('height')
        self.filesize = input_dict.get('filesize')

def RelatedStreams(object):
    def __init__(self):
        self.gallery = None
        self.recommended = None
        self.collections = None
    def from_dict(self):
        # TODO BACK HERE
        self.gallery = [EclipseDeviation(group) for group in input_dict.get('gallery')]

def ExtendedStats(object):
    def __init__(self):
        self.views = None
        self.today = None
        self.shares = None
        self.downloads = None
        self.groups = None

