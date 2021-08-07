"""Model to represent DeviantArt Eclipse Deviation Extended Stats."""

from daeclipse.models.model import Model


class DeviationExtendedStats(Model):
    """Model to represent DeviantArt Eclipse Deviation Stats."""

    def __init__(self, attrs=None):
        """Initialize DeviationExtendedStats.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.views = None
        self.today = None
        self.shares = None
        self.downloads = None
        self.groups = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationExtendedStats fields.
        """
        super().from_dict(attrs)
        self.views = attrs.get('views')
        self.today = attrs.get('today')
        self.shares = attrs.get('shares')
        self.downloads = attrs.get('downloads')
        self.groups = attrs.get('groups')
