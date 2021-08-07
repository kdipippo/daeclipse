"""Model to represent DeviantArt Eclipse Comment Content."""


class CommentContent(object):
    """Model to represent DeviantArt Eclipse Comment Content."""

    def __init__(self, input_dict=None):
        """Initialize CommentContent.

        Args:
            input_dict (dict, optional): Dict of CommentContent class attrs.
        """
        self.excerpt = None
        self.html = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing CommentContent fields.
        """
        if input_dict is None:
            return
        self.excerpt = input_dict.get('excerpt')
        self.html = input_dict.get('html')
