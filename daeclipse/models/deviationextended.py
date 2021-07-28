"""Model to represent DeviantArt Eclipse Extended Deviation."""

from daeclipse.models.deviation import EclipseDeviation


class EclipseDeviationExtended(object):
    """Model to represent DeviantArt Eclipse Extended Deviation."""

    def __init__(self, input_dict=None):
        """Initialize EclipseDeviationExtended.

        Args:
            input_dict (dict, optional): Dict of EclipseDeviationExtended class attrs.
        """
        self.deviation = None
        self.view_mode = None
        self.comments = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseDeviation fields.
        """
        if input_dict is None:
            return
        self.deviation = EclipseDeviation(input_dict.get('deviation'))
        self.view_mode = input_dict.get('viewMode')
        self.comments = EclipseCommentsList(input_dict.get('comments'))
