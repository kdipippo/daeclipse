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

        # Constants for locations of user comments.
        self.DEVIATION = 0
        self.PROFILE = 1
        self.DELETED = 2
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing UserComment fields.
        """
        super().from_dict(attrs)
        self.comment = Comment(attrs.get('comment'))
        subject = attrs.get('subject')
        if not subject:
            # Some comments may be retrieved that show as deleted
            self.subject_type = self.DELETED
        elif subject.get('deviation'):
            self.subject_type = self.DEVIATION
            self.subject = Deviation(subject.get('deviation'))
        elif subject.get('profile'):
            self.subject_type = self.PROFILE
            self.subject = Gruser(subject.get('profile'))

    def get_url(self):
        """Return the URL of the comment.

        Returns:
            string: URL pointed to comment.
        """
        if self.subject_type == self.DEVIATION:
            return 'https://www.deviantart.com/comments/1/{0}/{1}'.format(
                self.subject.deviation_id,
                self.comment.comment_id,
            )
        if self.subject_type == self.PROFILE:
            return 'https://www.deviantart.com/comments/4/{0}/{1}'.format(
                self.subject.user_id,
                self.comment.comment_id,
            )
        return 'ID {0} Deleted'.format(self.comment.comment_id)

    def get_text(self):
        """Return text of comment.

        Returns:
            string: Text of comment.
        """
        return self.comment.get_text()
