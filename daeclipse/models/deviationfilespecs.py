"""Model to represent DeviantArt Eclipse Deviation File Specs."""


class EclipseDeviationFileSpecs(object):
    """Model to represent DeviantArt Eclipse Deviation File Specs."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviationFileSpecs.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviationFileSpecs class attrs.
        """
        self.type = None
        self.width = None
        self.height = None
        self.filesize = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviationFileSpecs fields.
        """
        if input_dict is None:
            return
        self.type = input_dict.get('type')
        self.width = input_dict.get('width')
        self.height = input_dict.get('height')
        self.filesize = input_dict.get('filesize')
