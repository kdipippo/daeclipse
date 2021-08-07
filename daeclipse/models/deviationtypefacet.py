"""Model to represent DeviantArt Eclipse Deviation Type Facet."""


class DeviationTypeFacet(object):
    """Model to represent DeviantArt Eclipse Deviation Type Facet."""

    def __init__(self, input_dict=None):
        """Initialize DeviationTypeFacet.

        Args:
            input_dict (dict, optional): Dict of DeviationTypeFacet class attrs.
        """
        self.link_to = None
        self.url_fragment = None
        self.display_name_en = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing DeviationTypeFacet fields.
        """
        if input_dict is None:
            return
        self.link_to = input_dict.get('linkTo')
        self.url_fragment = input_dict.get('urlFragment')
        self.display_name_en = input_dict.get('displayNameEn')
