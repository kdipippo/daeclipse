"""Model to represent DeviantArt Eclipse Comments List."""

from daeclipse.models.comment import Comment
from daeclipse.models.model import Model


class CommentsList(Model):
    """Model to represent DeviantArt Eclipse Comments List."""

    def __init__(self, attrs=None):
        """Initialize CommentsList.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        super().__init__(attrs)
        self.has_more = None
        self.has_less = None
        self.next_offset = None
        self.cursor = None
        self.prev_cursor = None
        self.total = None
        self.can_post_comment = None
        self.commentable_typeid = None
        self.commentable_itemid = None
        self.thread = None

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing CommentsList fields.
        """
        super().from_dict(attrs)
        self.has_more = attrs.get('hasMore')
        self.has_less = attrs.get('hasLess')
        self.next_offset = attrs.get('nextOffset')
        self.cursor = attrs.get('cursor')
        self.prev_cursor = attrs.get('prevCursor')
        self.total = attrs.get('total')
        self.can_post_comment = attrs.get('canPostComment')
        self.commentable_typeid = attrs.get('commentableTypeid')
        self.commentable_itemid = attrs.get('commentableItemid')
        self.thread = self.to_submodel_list(Comment, attrs.get('thread'))
