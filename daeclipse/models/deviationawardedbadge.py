"""Model to represent DeviantArt Eclipse Deviation Awarded Badges."""

from daeclipse.models.model import Model


class DeviationAwardedBadge(Model):
    """Model to represent DeviantArt Eclipse Deviation Awarded Badges."""

    def __init__(self, attrs=None):
        """Initialize DeviationAwardedBadge.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.id = None
        self.type_id = None
        self.name = None
        self.title = None
        self.base_title = None
        self.description = None
        self.stack_count = None
        self.images = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationAwardedBadge fields.
        """
        super().from_dict(attrs)
        self.id = attrs.get('id')
        self.type_id = attrs.get('typeId')
        self.name = attrs.get('name')
        self.title = attrs.get('title')
        self.base_title = attrs.get('baseTitle')
        self.description = attrs.get('description')
        self.stack_count = attrs.get('stackCount')
        self.images = attrs.get('images')
