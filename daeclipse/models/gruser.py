"""Model to represent DeviantArt Eclipse Group or User."""

from daeclipse.models.model import Model


class Gruser(Model):
    """Model to represent DeviantArt Eclipse Group or User."""

    def __init__(self, attrs=None):
        """Initialize Gruser.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.user_id = None
        self.userid_uuid = None
        self.username = None
        self.usericon = None
        self.type = None
        self.is_watching = None
        self.is_new_deviant = None
        super().__init__(attrs)

    def __repr__(self):
        """Representation of Gruser.

        Returns:
            string: Gruser representation.
        """
        return self.user_id

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Gruser fields.
        """
        super().from_dict(attrs)
        self.user_id = attrs.get('userId')
        self.userid_uuid = attrs.get('useridUuid')
        self.username = attrs.get('username')
        self.usericon = attrs.get('usericon')
        self.type = attrs.get('type')
        self.is_watching = attrs.get('isWatching')
        self.is_new_deviant = attrs.get('isNewDeviant')
