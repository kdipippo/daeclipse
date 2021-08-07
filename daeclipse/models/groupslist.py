"""Model to represent DeviantArt Eclipse Groups List."""

from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model


class GroupsList(Model):
    """Model to represent DeviantArt Eclipse Groups List."""

    def __init__(self, attrs=None):
        """Initialize GroupsList.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.has_more = None
        self.next_offset = None
        self.total = None
        self.groups = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Stats fields.
        """
        super().from_dict(attrs)
        self.has_more = attrs.get('hasMore')
        self.next_offset = attrs.get('nextOffset')
        self.total = attrs.get('total')
        self.groups = self.to_submodel(Gruser, attrs.get('results'))
