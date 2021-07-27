"""Model to represent DeviantArt Eclipse Group Folder."""

from daeclipse.models.deviation import EclipseDeviation
from daeclipse.models.gruser import EclipseGruser


class EclipseFolder(object):  # noqa: WPS230
    """Model to represent DeviantArt Eclipse Group Folder."""

    def __init__(self, input_dict=None):
        """Initialize EclipseFolder.

        Args:
            input_dict (dict, optional): Dict of EclipseFolder class attrs.
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
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def __repr__(self):
        """Representation of EclipseFolder.

        Returns:
            string: EclipseFolder representation.
        """
        return self.folder_id

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseFolder fields.
        """
        if input_dict is None:
            return
        self.folder_id = input_dict.get('folderId')
        self.gallection_uuid = input_dict.get('gallectionUuid')
        self.parent_id = input_dict.get('parentId')
        self.type = input_dict.get('type')
        self.name = input_dict.get('name')
        self.description = input_dict.get('description')

        self.owner = EclipseGruser()
        self.owner.from_dict(input_dict.get('owner'))

        self.comment_count = input_dict.get('commentCount')
        self.size = input_dict.get('size')

        self.thumb = EclipseDeviation()
        self.thumb.from_dict(input_dict.get('thumb'))

        self.has_sub_folders = input_dict.get('hasSubfolders')
        self.total_item_count = input_dict.get('totalItemCount')
