"""Model to represent DeviantArt Eclipse Deviation Extended Content."""

from daeclipse.models.deviationawardedbadge import DeviationAwardedBadge
from daeclipse.models.deviationextendedstats import DeviationExtendedStats
from daeclipse.models.deviationfilespecs import DeviationFileSpecs
from daeclipse.models.deviationrelatedstreams import DeviationRelatedStreams
from daeclipse.models.deviationtag import DeviationTag
from daeclipse.models.deviationtypefacet import DeviationTypeFacet


class DeviationExtendedContent(object):
    """Model to represent DeviantArt Eclipse Deviation Extended Content."""

    def __init__(self, input_dict=None):
        """Initialize DeviationExtendedContent.

        Args:
            input_dict (dict, optional): Dict of DeviationExtendedContent class attrs.
        """
        self.deviation_uuid = None
        self.can_user_add_to_group = None
        self.group_list_url = None
        self.description = None
        self.original_file = None
        self.tags = None
        self.subject_tags = None
        self.type_facet = None
        self.license = None
        self.download = None
        self.related_streams = None
        self.stats = None
        self.report_url = None
        self.awarded_badges = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing DeviationExtendedContent fields.
        """
        if input_dict is None:
            return
        self.deviation_uuid = input_dict.get('deviationUuid')
        self.can_user_add_to_group = input_dict.get('canUserAddToGroup')
        self.group_list_url = input_dict.get('groupListUrl')
        self.description = input_dict.get('description')
        self.original_file = DeviationFileSpecs(input_dict.get('originalFile'))
        if input_dict.get('tags') is not None:
            self.tags = [DeviationTag(tag) for tag in input_dict.get('tags')]
        if input_dict.get('subjectTags') is not None:
            self.subject_tags = [DeviationTag(tag) for tag in input_dict.get('subjectTags')]
        self.type_facet = DeviationTypeFacet(input_dict.get('typeFacet'))
        self.license = input_dict.get('license')
        self.download = DeviationFileSpecs(input_dict.get('download'))
        self.related_streams = DeviationRelatedStreams(input_dict.get('relatedStreams'))
        self.stats = DeviationExtendedStats(input_dict.get('stats'))
        self.report_url = input_dict.get('reportUrl')
        if input_dict.get('awardedBadges') is not None:
            self.awarded_badges = [DeviationAwardedBadge(badge) for badge in input_dict.get('awardedBadges')]
