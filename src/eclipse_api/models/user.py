"""Model to represent DeviantArt Eclipse User."""

class EclipseUser:
    """Model to represent DeviantArt Eclipse User."""

    def __init__(self, input_dict = None):
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
        return self.user_id

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseUser fields.
        """
        if 'userId' in input_dict:
            self.user_id = input_dict['userId']
        if 'useridUuid' in input_dict:
            self.userid_uuid = input_dict['useridUuid']
        if 'username' in input_dict:
            self.username = input_dict['username']
        if 'usericon' in input_dict:
            self.usericon = input_dict['usericon']
        if 'type' in input_dict:
            self.type = input_dict['type']
        if 'isWatching' in input_dict:
            self.is_watching = input_dict['isWatching']
        if 'isNewDeviant' in input_dict:
            self.is_new_deviant = input_dict['isNewDeviant']
