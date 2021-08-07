"""Model to represent DeviantArt Eclipse Deviation File Specs."""

from daeclipse.models.model import Model


class DeviationFileSpecs(Model):
    """Model to represent DeviantArt Eclipse Deviation File Specs."""

    def __init__(self, attrs=None):
        """Initialize DeviationFileSpecs.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.url = None
        self.type = None
        self.width = None
        self.height = None
        self.filesize = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationFileSpecs fields.
        """
        super().from_dict(attrs)
        self.url = attrs.get('url')
        self.type = attrs.get('type')
        self.width = attrs.get('width')
        self.height = attrs.get('height')
        self.filesize = attrs.get('filesize')
