"""Class to handle list of colors and images gif creation."""


class SelectedAssets(object):
    """Class to handle list of colors and images gif creation."""

    def __init__(self):
        """Initialize SelectedAssets class."""
        self.colors = {}
        self.images = {}
        self.json = None

    def add_color(self, color_type, selected_type):
        """Assign the selected palette to the component to recolor.

        Args:
            color_type (str): Component the recolor applies to, i.e. 'hair'.
            selected_type (str): Palette to recolor to, i.e. 'blonde'.
        """
        self.colors[color_type] = selected_type

    def add_image(self, image_type, image_num):
        """Assign selected image type to image num when gif parts are layered.

        Args:
            image_type (str): Image layer being added, i.e. 'hairbackshort'.
            image_num (str): Asset number for the image layer, i.e. '00A'.
        """
        self.images[image_type] = '{0:02d}'.format(image_num)

    def store_json(self, assets_json):
        """Store the full, parsed assets.json file for reference.

        Args:
            assets_json (dict): Dictionary result from loading assets.json.
        """
        self.json = assets_json

    def update_json(self, override):
        """Manually override the colors and images dictionaries.

        Args:
            override (dict): A combined dict with keys 'colors' and 'images'.
        """
        self.colors = override['colors']
        self.images = override['images']

    def as_json(self):
        """Return the colors and images dicts as one combined dict.

        Returns:
            dict: A combined dict with keys 'colors' and 'images'.
        """
        return {
            'colors': self.colors,
            'images': self.images,
        }

    def get_sorted_layers(self):
        """Return list of type layers in lowest to highest 'order' value.

        Returns:
            list (str): List of image type layers.
        """
        return sorted(
            self.json['imageTypes'].items(),
            key=lambda image_type: image_type[1]['order'],
        )
