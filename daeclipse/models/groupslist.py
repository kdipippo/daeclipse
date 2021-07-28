"""Model to represent DeviantArt Eclipse Groups List."""


class EclipseGroupsList(object):
    """Model to represent DeviantArt Eclipse Groups List."""

    def __init__(self, input_dict=None):
        """Initialize EclipseGroupsList.

        Args:
            input_dict (dict, optional): Dict of EclipseGroupsList class attrs.
        """
        self.has_more = None
        self.next_offset = None
        self.total = None
        self.groups = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseStats fields.
        """
        if input_dict is None:
            return
        self.has_more = input_dict.get('hasMore')
        self.next_offset = input_dict.get('nextOffset')
        self.total = input_dict.get('total')
        self.groups = [EclipseGruser(group) for group in input_dict.get('results')]
