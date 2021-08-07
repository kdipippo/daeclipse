"""Model to represent DeviantArt Eclipse Group Folder."""

from daeclipse.models.deviation import Deviation
from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model


class Folder(Model):
    """Model to represent DeviantArt Eclipse Group Folder."""

    def __init__(self, attrs=None):
        """Initialize Folder.

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
        self.has_sub_folders = None
        self.total_item_count = None
        super().__init__(attrs)

    def __repr__(self):
        """Representation of Folder.

        Returns:
            string: Folder representation.
        """
        return self.folder_id

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Folder fields.
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
        self.thumb = Deviation(attrs.get('thumb'))
        self.has_sub_folders = attrs.get('hasSubfolders')
        self.total_item_count = attrs.get('totalItemCount')
