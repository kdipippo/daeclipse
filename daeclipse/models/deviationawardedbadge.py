"""Model to represent DeviantArt Eclipse Deviation Awarded Badges."""


class EclipseDeviationAwardedBadge(object):
    """Model to represent DeviantArt Eclipse Deviation Awarded Badges."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviationAwardedBadge.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviationAwardedBadge class attrs.
        """
        self.id = None
        self.type_id = None
        self.name = None
        self.title = None
        self.base_title = None
        self.description = None
        self.stack_count = None
        self.images = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviationAwardedBadge fields.
        """
        if input_dict is None:
            return
        self.id = input_dict.get('id')
        self.type_id = input_dict.get('typeId')
        self.name = input_dict.get('name')
        self.title = input_dict.get('title')
        self.base_title = input_dict.get('baseTitle')
        self.description = input_dict.get('description')
        self.stack_count = input_dict.get('stackCount')
        self.images = input_dict.get('images')
