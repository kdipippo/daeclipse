"""Model to represent DeviantArt Eclipse Deviation Extended Content."""

from daeclipse.models.deviationawardedbadge import DeviationAwardedBadge
from daeclipse.models.deviationextendedstats import DeviationExtendedStats
from daeclipse.models.deviationfilespecs import DeviationFileSpecs
from daeclipse.models.deviationrelatedstreams import DeviationRelatedStreams
from daeclipse.models.deviationtag import DeviationTag
from daeclipse.models.deviationtypefacet import DeviationTypeFacet
from daeclipse.models.model import Model


class DeviationExtendedContent(Model):
    """Model to represent DeviantArt Eclipse Deviation Extended Content."""

    def __init__(self, attrs=None):
        """Initialize DeviationExtendedContent.

        Args:
            attrs (dict, optional): Dict of model attributes.
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
        super().__init__(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationExtendedContent fields.
        """
        super().from_dict(attrs)
        self.deviation_uuid = attrs.get('deviationUuid')
        self.can_user_add_to_group = attrs.get('canUserAddToGroup')
        self.group_list_url = attrs.get('groupListUrl')
        self.description = attrs.get('description')
        self.original_file = DeviationFileSpecs(attrs.get('originalFile'))
        self.tags = self.to_submodel_list(DeviationTag, attrs.get('tags'))
        self.subject_tags = self.to_submodel_list(
            DeviationTag,
            attrs.get('subjectTags'),
        )
        self.type_facet = DeviationTypeFacet(attrs.get('typeFacet'))
        self.license = attrs.get('license')
        self.download = DeviationFileSpecs(attrs.get('download'))
        self.related_streams = DeviationRelatedStreams(
            attrs.get('relatedStreams'),
        )
        self.stats = DeviationExtendedStats(attrs.get('stats'))
        self.report_url = attrs.get('reportUrl')
        self.awarded_badges = self.to_submodel_list(
            DeviationAwardedBadge,
            attrs.get('awardedBadges'),
        )
