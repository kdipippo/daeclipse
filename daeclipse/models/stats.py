"""Model to represent DeviantArt Eclipse Deviation Stats."""

from daeclipse.models.model import Model


class Stats(Model):
    """Model to represent DeviantArt Eclipse Deviation Stats."""

    def __init__(self, attrs=None):
        """Initialize Stats.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.comments = None
        self.favourites = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Stats fields.
        """
        super().from_dict(attrs)
        self.comments = attrs.get('comments')
        self.favourites = attrs.get('favourites')
