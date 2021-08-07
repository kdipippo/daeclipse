"""Model to represent DeviantArt Eclipse Deviation Tags."""


class DeviationTag(object):
    """Model to represent DeviantArt Eclipse Deviation Tags."""

    def __init__(self, input_dict=None):
        """Initialize DeviationTag.

        Args:
            input_dict (dict, optional): Dict of DeviationTag class attrs.
        """
        self.name = None
        self.url = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing DeviationTag fields.
        """
        if input_dict is None:
            return
        self.name = input_dict.get('name')
        self.url = input_dict.get('url')
