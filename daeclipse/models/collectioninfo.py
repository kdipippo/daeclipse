"""Model to represent DeviantArt Eclipse Collection Info."""

import daeclipse.models.deviation
from daeclipse.models.gruser import Gruser


class CollectionInfo(object):
    """Model to represent DeviantArt Eclipse Deviation Info."""

    def __init__(self, input_dict=None):
        """Initialize CollectionInfo.

        Args:
            input_dict (dict, optional): Dict of CollectionInfo class attrs.
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
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing CollectionInfo fields.
        """
        if input_dict is None:
            return
        self.folder_id = input_dict.get('folderId')
        self.gallection_uuid = input_dict.get('gallectionUuid')
        self.parent_id = input_dict.get('parentId')
        self.type = input_dict.get('type')
        self.name = input_dict.get('name')
        self.description = input_dict.get('description')
        self.owner = Gruser(input_dict.get('owner'))
        self.comment_count = input_dict.get('commentCount')
        self.size = input_dict.get('size')
        self.thumb = daeclipse.models.deviation.Deviation(input_dict.get('folderId'))
