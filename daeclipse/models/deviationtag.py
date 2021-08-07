"""Model to represent DeviantArt Eclipse Deviation Tags."""

from daeclipse.models.model import Model


class DeviationTag(Model):
    """Model to represent DeviantArt Eclipse Deviation Tags."""

    def __init__(self, attrs=None):
        """Initialize DeviationTag.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.name = None
        self.url = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationTag fields.
        """
        super().from_dict(attrs)
        self.name = attrs.get('name')
        self.url = attrs.get('url')
