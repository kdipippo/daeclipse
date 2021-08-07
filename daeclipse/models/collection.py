"""Model to represent DeviantArt Eclipse Collections."""

import daeclipse.models.deviation
from daeclipse.models.collectioninfo import CollectionInfo
from daeclipse.models.gruser import Gruser


class Collection(object):
    """Model to represent DeviantArt Eclipse Collections."""

    def __init__(self, input_dict=None):
        """Initialize Collection.

        Args:
            input_dict (dict, optional): Dict of Collection class attrs.
        """
        self.collection = None
        self.deviations = None
        self.groups = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing Collection fields.
        """
        if input_dict is None:
            return
        self.collection = CollectionInfo(input_dict.get('collection'))
        if input_dict.get('deviations') is not None:
            self.deviations = [daeclipse.models.deviation.Deviation(deviation) for deviation in input_dict.get('deviations')]
        if input_dict.get('groups') is not None:
            self.groups = [Gruser(group) for group in input_dict.get('groups')]
