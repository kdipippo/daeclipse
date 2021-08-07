"""Model to represent DeviantArt Eclipse Group or User."""


class Gruser(object):  # noqa: WPS230
    """Model to represent DeviantArt Eclipse Group or User."""

    def __init__(self, input_dict=None):
        """Initialize Gruser.

        Args:
            input_dict (dict, optional): Dict of Gruser class attrs.
        """
        self.user_id = None
        self.userid_uuid = None
        self.username = None
        self.usericon = None
        self.type = None
        self.is_watching = None
        self.is_new_deviant = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def __repr__(self):
        """Representation of Gruser.

        Returns:
            string: Gruser representation.
        """
        return self.user_id

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing Gruser fields.
        """
        if input_dict is None:
            return
        self.user_id = input_dict.get('userId')
        self.userid_uuid = input_dict.get('useridUuid')
        self.username = input_dict.get('username')
        self.usericon = input_dict.get('usericon')
        self.type = input_dict.get('type')
        self.is_watching = input_dict.get('isWatching')
        self.is_new_deviant = input_dict.get('isNewDeviant')
