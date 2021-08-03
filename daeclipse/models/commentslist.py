"""Model to represent DeviantArt Eclipse Comments List."""

from daeclipse.models.comment import EclipseComment


class EclipseCommentsList(object):
    """Model to represent DeviantArt Eclipse Comments List."""

    def __init__(self, input_dict=None):
        """Initialize EclipseCommentsList.

        Args:
            input_dict (dict, optional): Dict of EclipseCommentsList class attrs.
        """
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
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseCommentsList fields.
        """
        if input_dict is None:
            return
        self.has_more = input_dict.get('hasMore')
        self.has_less = input_dict.get('hasLess')
        self.next_offset = input_dict.get('nextOffset')
        self.cursor = input_dict.get('cursor')
        self.prev_cursor = input_dict.get('prevCursor')
        self.total = input_dict.get('total')
        self.can_post_comment = input_dict.get('canPostComment')
        self.commentable_typeid = input_dict.get('commentableTypeid')
        self.commentable_itemid = input_dict.get('commentableItemid')
        if input_dict.get('thread') is not None:
            self.thread = [EclipseComment(comment_dict) for comment_dict in input_dict.get('thread')]
