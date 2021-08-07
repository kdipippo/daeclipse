"""Model to represent DeviantArt Eclipse Extended Deviation."""

from daeclipse.models.commentslist import CommentsList
from daeclipse.models.deviationextended import DeviationExtended
from daeclipse.models.model import Model


class DeviationExtendedResult(Model):
    """Model to represent DeviantArt Eclipse Extended Deviation."""

    def __init__(self, attrs=None):
        """Initialize DeviationExtendedResult.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.deviation = None
        self.view_mode = None
        self.comments = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Deviation fields.
        """
        super().from_dict(attrs)
        self.deviation = DeviationExtended(attrs.get('deviation'))
        self.view_mode = attrs.get('viewMode')
        self.comments = CommentsList(attrs.get('comments'))
