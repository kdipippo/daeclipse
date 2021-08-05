"""Model to represent DeviantArt Eclipse Collections."""

import daeclipse.models.deviation
from daeclipse.models.collectioninfo import EclipseCollectionInfo
from daeclipse.models.gruser import EclipseGruser


class EclipseCollection(object):
    """Model to represent DeviantArt Eclipse Collections."""

    def __init__(self, input_dict=None):
        """Initialize EclipseCollection.

        Args:
            input_dict (dict, optional): Dict of EclipseCollection class attrs.
        """
        self.collection = None
        self.deviations = None
        self.groups = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseCollection fields.
        """
        if input_dict is None:
            return
        self.collection = EclipseCollectionInfo(input_dict.get('collection'))
        if input_dict.get('deviations') is not None:
            self.deviations = [daeclipse.models.deviation.EclipseDeviation(deviation) for deviation in input_dict.get('deviations')]
        if input_dict.get('groups') is not None:
            self.groups = [EclipseGruser(group) for group in input_dict.get('groups')]
