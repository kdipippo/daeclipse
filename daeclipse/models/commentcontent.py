"""Model to represent DeviantArt Eclipse Comment Content."""

from daeclipse.models.model import Model


class CommentContent(Model):
    """Model to represent DeviantArt Eclipse Comment Content."""

    def __init__(self, attrs=None):
        """Initialize CommentContent.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.excerpt = None
        self.html = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing CommentContent fields.
        """
        super().from_dict(attrs)
        self.excerpt = attrs.get('excerpt')
        self.html = attrs.get('html')
