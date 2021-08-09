"""Model to represent DeviantArt Eclipse Deviation Related Streams."""

from daeclipse.models.collection import Collection
from daeclipse.models.deviation import Deviation
from daeclipse.models.model import Model


class DeviationRelatedStreams(Model):
    """Model to represent DeviantArt Eclipse Related Streams."""

    def __init__(self, attrs=None):
        """Initialize DeviationRelatedStreams.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.gallery = None
        self.recommended = None
        self.collections = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationRelatedStreams fields.
        """
        super().from_dict(attrs)
        self.gallery = self.to_submodel_list(Deviation, attrs.get('gallery'))
        self.recommended = self.to_submodel_list(
            Deviation,
            attrs.get('recommended'),
        )
        self.collections = self.to_submodel_list(
            Collection,
            attrs.get('collections'),
        )
