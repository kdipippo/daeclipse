"""Model to represent DeviantArt Eclipse Deviation."""

from daeclipse.models.deviationmedia import DeviationMedia
from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model
from daeclipse.models.stats import Stats


class Deviation(Model):
    """Model to represent DeviantArt Eclipse Deviation."""

    def __init__(self, attrs=None):
        """Initialize Deviation.

        Args:
            attrs (dict, optional): Dict of model attributes.
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
        super().__init__(attrs)

    def __repr__(self):
        """Representation of Deviation.

        Returns:
            string: Deviation representation.
        """
        return self.deviation_id

    def from_dict(self, attrs):  # noqa: WPS231
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Deviation fields.
        """
        super().from_dict(attrs)
        self.deviation_id = attrs.get('deviationId')
        self.type = attrs.get('type')
        self.type_id = attrs.get('typeId')
        self.print_id = attrs.get('printId')
        self.url = attrs.get('url')
        self.title = attrs.get('title')
        self.is_journal = attrs.get('isJournal')
        self.is_video = attrs.get('isVideo')
        self.is_purchasable = attrs.get('isPurchasable')
        self.is_favouritable = attrs.get('isFavouritable')
        self.published_time = attrs.get('publishedTime')
        self.is_text_editable = attrs.get('isTextEditable')
        self.legacy_text_edit_url = attrs.get('legacyTextEditUrl')
        self.is_shareable = attrs.get('isShareable')
        self.is_commentable = attrs.get('isCommentable')
        self.is_favourited = attrs.get('isFavourited')
        self.is_deleted = attrs.get('isDeleted')
        self.is_mature = attrs.get('isMature')
        self.is_downloadable = attrs.get('isDownloadable')
        self.is_antisocial = attrs.get('isAntisocial')
        self.is_blocked = attrs.get('isBlocked')
        self.is_published = attrs.get('isPublished')
        self.is_daily_deviation = attrs.get('isDailyDeviation')
        self.has_private_comments = attrs.get('hasPrivateComments')
        self.block_reasons = attrs.get('blockReasons')
        self.author = Gruser(attrs.get('author'))
        self.stats = Stats(attrs.get('stats'))
        self.media = DeviationMedia(attrs.get('media'))
