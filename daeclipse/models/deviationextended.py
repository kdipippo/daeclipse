"""Model to represent DeviantArt Eclipse Extended Deviation."""

from daeclipse.models.deviation import Deviation
from daeclipse.models.deviationextendedcontent import DeviationExtendedContent


class DeviationExtended(Deviation):
    """Model to represent DeviantArt Eclipse Extended Deviation."""

    def __init__(self, attrs=None):
        """Initialize DeviationExtended.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.extended = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing Deviation fields.
        """
        super().from_dict(attrs)
        self.extended = DeviationExtendedContent(attrs.get('extended'))

    def get_tag_names(self):
        """Return list of tag names for extended Deviation object.

        Returns:
            str[]: List of tag names.
        """
        if self.extended is None:
            return []
        if self.extended.tags is None:
            return []
        return [tag.name for tag in self.extended.tags]
