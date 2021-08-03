"""Model to represent DeviantArt Eclipse Deviation Tags."""


class EclipseDeviationTag(object):
    """Model to represent DeviantArt Eclipse Deviation Tags."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviationTag.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviationTag class attrs.
        """
        self.name = None
        self.url = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviationTag fields.
        """
        if input_dict is None:
            return
        self.name = input_dict.get('name')
        self.url = input_dict.get('url')
