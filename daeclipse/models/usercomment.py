"""Model to represent DeviantArt Eclipse User's Comment."""

from daeclipse.models.comment import Comment
from daeclipse.models.deviation import Deviation
from daeclipse.models.gruser import Gruser
from daeclipse.models.model import Model


class UserComment(Model):
    """Model to represent DeviantArt Eclipse User's Comment."""

    def __init__(self, attrs=None):
        """Initialize UserComment.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.comment = None
        self.subject_type = None
        self.subject = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing UserComment fields.
        """
        super().from_dict(attrs)
        self.comment = Comment(attrs.get('comment'))
        if attrs.get('subject').get('deviation'):
            self.subject_type = 'deviation'
            self.subject = Deviation(attrs.get('subject').get('deviation'))
        elif attrs.get('subject').get('profile'):
            self.subject_type = 'profile'
            # Note: Gruser will not contain the returned isSubscribed field.
            self.subject = Gruser(attrs.get('subject').get('profile'))
