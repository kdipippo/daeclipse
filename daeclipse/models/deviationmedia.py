"""Model to represent DeviantArt Eclipse Deviation Media."""


class DeviationMedia(object):
    """Model to represent DeviantArt Eclipse Deviation Media."""

    def __init__(self, input_dict=None):
        """Initialize DeviationMedia.

        Args:
            input_dict (dict, optional): Dict of DeviationMedia class attrs.
        """
        self.base_uri = None
        self.pretty_name = None
        self.token = None
        self.types = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing DeviationMedia fields.
        """
        if input_dict is None:
            return
        self.base_uri = input_dict.get('baseUri')
        self.pretty_name = input_dict.get('prettyName')
        self.token = input_dict.get('token')
        self.types = input_dict.get('types')
