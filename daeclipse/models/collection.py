"""Model to represent DeviantArt Eclipse Collections."""

from daeclipse.models.collectioninfo import CollectionInfo
from daeclipse.models.deviation import Deviation
from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model


class Collection(Model):
    """Model to represent DeviantArt Eclipse Collections."""

    def __init__(self, attrs=None):
        """Initialize Collection.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.collection = None
        self.deviations = None
        self.groups = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Collection fields.
        """
        super().from_dict(attrs)
        self.collection = CollectionInfo(attrs.get('collection'))
        self.deviations = self.to_submodel_list(
            Deviation,
            attrs.get('deviations'),
        )
        self.groups = self.to_submodel_list(Gruser, attrs.get('groups'))
