"""Model to represent DeviantArt Eclipse Deviation Media."""

from daeclipse.models.model import Model


class DeviationMedia(Model):
    """Model to represent DeviantArt Eclipse Deviation Media."""

    def __init__(self, attrs=None):
        """Initialize DeviationMedia.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.base_uri = None
        self.pretty_name = None
        self.token = None
        self.types = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationMedia fields.
        """
        super().from_dict(attrs)
        self.base_uri = attrs.get('baseUri')
        self.pretty_name = attrs.get('prettyName')
        self.token = attrs.get('token')
        self.types = attrs.get('types')
