"""Model to represent DeviantArt Eclipse Extended Deviation."""

import daeclipse.models.deviation
from daeclipse.models.commentslist import CommentsList


class DeviationExtended(object):
    """Model to represent DeviantArt Eclipse Extended Deviation."""

    def __init__(self, input_dict=None):
        """Initialize DeviationExtended.

        Args:
            input_dict (dict, optional): Dict of DeviationExtended class attrs.
        """
        self.deviation = None
        self.view_mode = None
        self.comments = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing Deviation fields.
        """
        if input_dict is None:
            return
        self.deviation = daeclipse.models.deviation.Deviation(input_dict.get('deviation'))
        self.view_mode = input_dict.get('viewMode')
        self.comments = CommentsList(input_dict.get('comments'))
