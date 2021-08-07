"""Model to represent DeviantArt Eclipse Collection Info."""

from daeclipse.models.deviation import Deviation
from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model


class CollectionInfo(Model):
    """Model to represent DeviantArt Eclipse Deviation Info."""

    def __init__(self, attrs=None):
        """Initialize CollectionInfo.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.folder_id = None
        self.gallection_uuid = None
        self.parent_id = None
        self.type = None
        self.name = None
        self.description = None
        self.owner = None
        self.comment_count = None
        self.size = None
        self.thumb = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing CollectionInfo fields.
        """
        super().from_dict(attrs)
        self.folder_id = attrs.get('folderId')
        self.gallection_uuid = attrs.get('gallectionUuid')
        self.parent_id = attrs.get('parentId')
        self.type = attrs.get('type')
        self.name = attrs.get('name')
        self.description = attrs.get('description')
        self.owner = Gruser(attrs.get('owner'))
        self.comment_count = attrs.get('commentCount')
        self.size = attrs.get('size')
        self.thumb = Deviation(attrs.get('folderId'))
