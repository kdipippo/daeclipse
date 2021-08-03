"""Model to represent DeviantArt Eclipse Deviation Extended Stats."""


class EclipseDeviationExtendedStats(object):
    """Model to represent DeviantArt Eclipse Deviation Stats."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviationExtendedStats.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviationExtendedStats class attrs.
        """
        self.views = None
        self.today = None
        self.shares = None
        self.downloads = None
        self.groups = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviationExtendedStats fields.
        """
        if input_dict is None:
            return
        self.views = input_dict.get('views')
        self.today = input_dict.get('today')
        self.shares = input_dict.get('shares')
        self.downloads = input_dict.get('downloads')
        self.groups = input_dict.get('groups')
