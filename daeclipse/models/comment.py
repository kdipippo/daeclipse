"""Model to represent DeviantArt Eclipse Comments."""

from daeclipse.models.commentcontent import EclipseCommentContent
from daeclipse.models.gruser import EclipseGruser


class EclipseComment(object):
    """Model to represent DeviantArt Eclipse Comments."""

    def __init__(self, input_dict=None):
        """Initialize EclipseComment.

        Args:
            input_dict (dict, optional): Dict of EclipseComment class attrs.
        """
        self.comment_id = None
        self.type_id = None
        self.item_id = None
        self.parent_id = None
        self.posted = None
        self.edited = None
        self.replies = None
        self.is_owner = None
        self.is_violation = None
        self.is_admin_hidden = None
        self.is_hidden = None
        self.is_locked = None
        self.is_spam = None
        self.is_private = None
        self.is_annotation = None
        self.is_deleted = None
        self.is_peekable = None
        self.is_author = None
        self.is_author_highlighted = None
        self.is_admin_mode = None
        self.is_featured = None
        self.is_reportable = None
        self.is_liked = None
        self.likes = None
        self.hidden = None
        self.text_content = None
        self.signature = None
        self.author_info = None
        self.user = None
        self.legacy_text_edit_url = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseComment fields.
        """
        if input_dict is None:
            return
        self.comment_id = input_dict.get('commentId')
        self.type_id = input_dict.get('typeId')
        self.item_id = input_dict.get('itemId')
        self.parent_id = input_dict.get('parentId')
        self.posted = input_dict.get('posted')
        self.edited = input_dict.get('edited')
        self.replies = input_dict.get('replies')
        self.is_owner = input_dict.get('isOwner')
        self.is_violation = input_dict.get('isViolation')
        self.is_admin_hidden = input_dict.get('isAdminHidden')
        self.is_hidden = input_dict.get('isHidden')
        self.is_locked = input_dict.get('isLocked')
        self.is_spam = input_dict.get('isSpam')
        self.is_private = input_dict.get('isPrivate')
        self.is_annotation = input_dict.get('isAnnotation')
        self.is_deleted = input_dict.get('isDeleted')
        self.is_peekable = input_dict.get('isPeekable')
        self.is_author = input_dict.get('isAuthor')
        self.is_author_highlighted = input_dict.get('isAuthorHighlighted')
        self.is_admin_mode = input_dict.get('isAdminMode')
        self.is_featured = input_dict.get('isFeatured')
        self.is_reportable = input_dict.get('isReportable')
        self.is_liked = input_dict.get('isLiked')
        self.likes = input_dict.get('likes')
        self.hidden = input_dict.get('hidden')
        self.text_content = EclipseCommentContent(input_dict.get('textContent'))
        self.signature = input_dict.get('signature')
        self.author_info = input_dict.get('authorInfo')
        self.user = EclipseGruser(input_dict.get('user'))
        self.legacy_text_edit_url = input_dict.get('legacyTextEditUrl')
