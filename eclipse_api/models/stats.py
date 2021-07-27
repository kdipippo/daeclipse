"""Model to represent DeviantArt Eclipse Deviation Stats."""


class EclipseStats:
    """Model to represent DeviantArt Eclipse Deviation Stats."""

    def __init__(self, input_dict=None):
        self.comments = None
        self.favourites = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseStats fields.
        """
        if input_dict is None:
            return
        if 'comments' in input_dict:
            self.comments = input_dict['comments']
        if 'favourites' in input_dict:
            self.favourites = input_dict['favourites']
