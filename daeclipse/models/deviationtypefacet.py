"""Model to represent DeviantArt Eclipse Deviation Type Facet."""

from daeclipse.models.model import Model


class DeviationTypeFacet(Model):
    """Model to represent DeviantArt Eclipse Deviation Type Facet."""

    def __init__(self, attrs=None):
        """Initialize DeviationTypeFacet.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        self.link_to = None
        self.url_fragment = None
        self.display_name_en = None
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationTypeFacet fields.
        """
        super().from_dict(attrs)
        self.link_to = attrs.get('linkTo')
        self.url_fragment = attrs.get('urlFragment')
        self.display_name_en = attrs.get('displayNameEn')
