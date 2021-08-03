"""Model to represent DeviantArt Eclipse Deviation Related Streams."""

import daeclipse.models.deviation
from daeclipse.models.collection import EclipseCollection


class EclipseDeviationRelatedStreams(object):
    """Model to represent DeviantArt Eclipse Related Streams."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviationRelatedStreams.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviationRelatedStreams class attrs.
        """
        self.gallery = None
        self.recommended = None
        self.collections = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviationRelatedStreams fields.
        """
        if input_dict is None:
            return
        if input_dict.get('gallery') is not None:
            self.gallery = [daeclipse.models.deviation.EclipseDeviation(group) for group in input_dict.get('gallery')]
        if input_dict.get('recommended') is not None:
            self.recommended = [daeclipse.models.deviation.EclipseDeviation(group) for group in input_dict.get('recommended')]
        if input_dict.get('collections') is not None:
            self.collections = [EclipseCollection(group) for group in input_dict.get('collections')]
