"""Base class for models."""


class Model(object):
    """Base class for models."""

    def __init__(self, attrs=None):
        """Initialize model.

        Args:
            attrs (dict, optional): Dict of model attributes.
        """
        if attrs is not None and isinstance(attrs, dict):
            self.from_dict(attrs)

    def from_dict(self, attrs):
        """Convert attrs values to class attributes.

        Args:
            attrs (dict): Dict containing DeviationRelatedStreams fields.
        """
        if attrs is None:
            return

    def to_submodel_list(self, submodel_class, submodel_attrs):
        """Return list of dictionaries as a list of specified objects.

        Args:
            submodel_class (`type`): Class instance to initialize.
            submodel_attrs (dict[]]): List of attribute dictionaries.

        Returns:
            submodel_class[]: List of specified submodel class instances.
        """
        if submodel_attrs is not None:
            return [submodel_class(entry) for entry in submodel_attrs]
