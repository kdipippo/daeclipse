"""Model to represent DeviantArt Eclipse User's Comments List."""

from daeclipse.models.model import Model
from daeclipse.models.usercomment import UserComment


class UsersCommentsList(Model):
    """Model to represent DeviantArt Eclipse User's Comments List."""

    def __init__(self, attrs=None):
        """Initialize UsersCommentsList.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.has_more = None
        self.next_offset = None
        self.comments = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing UsersCommentsList fields.
        """
        super().from_dict(attrs)
        self.has_more = attrs.get('hasMore')
        self.next_offset = attrs.get('nextOffset')
        self.comments = self.to_submodel_list(
            UserComment,
            attrs.get('results'),
        )
