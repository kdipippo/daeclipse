"""Model to represent DeviantArt Eclipse Comments."""

import json

from draftjs_exporter.html import HTML

from daeclipse.models.commentcontent import CommentContent
from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model


class Comment(Model):
    """Model to represent DeviantArt Eclipse Comments."""

    def __init__(self, attrs=None):
        """Initialize Comment.

        Args:
            attrs (dict, optional): Dict of model attributes.
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
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Comment fields.
        """
        super().from_dict(attrs)
        self.comment_id = attrs.get('commentId')
        self.type_id = attrs.get('typeId')
        self.item_id = attrs.get('itemId')
        self.parent_id = attrs.get('parentId')
        self.posted = attrs.get('posted')
        self.edited = attrs.get('edited')
        self.replies = attrs.get('replies')
        self.is_owner = attrs.get('isOwner')
        self.is_violation = attrs.get('isViolation')
        self.is_admin_hidden = attrs.get('isAdminHidden')
        self.is_hidden = attrs.get('isHidden')
        self.is_locked = attrs.get('isLocked')
        self.is_spam = attrs.get('isSpam')
        self.is_private = attrs.get('isPrivate')
        self.is_annotation = attrs.get('isAnnotation')
        self.is_deleted = attrs.get('isDeleted')
        self.is_peekable = attrs.get('isPeekable')
        self.is_author = attrs.get('isAuthor')
        self.is_author_highlighted = attrs.get('isAuthorHighlighted')
        self.is_admin_mode = attrs.get('isAdminMode')
        self.is_featured = attrs.get('isFeatured')
        self.is_reportable = attrs.get('isReportable')
        self.is_liked = attrs.get('isLiked')
        self.likes = attrs.get('likes')
        self.hidden = attrs.get('hidden')
        self.text_content = CommentContent(attrs.get('textContent'))
        self.signature = attrs.get('signature')
        self.author_info = attrs.get('authorInfo')
        self.user = Gruser(attrs.get('user'))
        self.legacy_text_edit_url = attrs.get('legacyTextEditUrl')

    def get_text(self):
        """Return text of comment.

        Returns:
            str: Text of comment.
        """
        # Writer means text_content stored as string in markup.
        if self.text_content.html.get('type') == 'writer':
            return self.text_content.html.get('markup')

        # Draft means text_content stored as Draft.js dictionary in markup.
        draftjs = json.loads(self.text_content.html.get('markup'))
        return draftjs_to_html(draftjs)


def draftjs_to_html(draftjs):
    """Return HTML markdown of given Draft.js dictionary.

    Args:
        draftjs (dict): Draft.js dictionary.

    Returns:
        str: HTML-formatted string.
    """
    exporter = HTML(
        {
            'entity_decorators': {
                'LINK': 'link',
                'IMAGE': 'image',
                'HORIZONTAL_RULE': 'hr',
                'DA_OFF_EMOTE': 'span',
            },
            'block_map': {
                'unstyled': 'p',
                'header-three': 'h3',
                'header-four': 'h4',
                'ordered-list-item': {
                    'element': 'li',
                    'wrapper': 'ol',
                },
                'unordered-list-item': {
                    'element': 'li',
                    'wrapper': 'ul',
                    'wrapper_props': {
                        'class': 'bullet-list',
                    },
                },
            },
            'style_map': {
                'BOLD': 'strong',
                'ITALIC': {
                    'element': 'em',
                    'props': {
                        'class': 'u-font-italic',
                    },
                },
            },
        },
    )

    html = exporter.render(draftjs)
    remove_p_tags = [
        ('</p><p>', '\n'),
        ('<p>', ''),
        ('</p>', ''),
    ]
    for remove_tag in remove_p_tags:
        html = html.replace(remove_tag[0], remove_tag[1])
    return html.strip()
