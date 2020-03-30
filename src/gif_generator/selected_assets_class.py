#!/usr/bin/env python
"""Class to handle the list of colors and images randomly generated for gif creation."""

class SelectedAssets:
    """Class to handle the list of colors and images randomly generated for gif creation."""

    colors = {}
    images = {}
    json = None

    def add_color(self, color_type, selected_type):
        """Assign the selected palette to the component to recolor.

        Args:
            color_type (string): Component the recolor applies to, i.e. 'skin'.
            selected_type (string): Palette to recolor the component to, i.e. 'pale'.
        """
        self.colors[color_type] = selected_type

    def add_image(self, image_type, image_num):
        """Assign the selected image asset to the image layer when gif parts are layered.

        Args:
            image_type (string): Image layer being added, i.e. 'hairbackshort'.
            image_num (string): Asset number for the image layer, i.e. '00A'.
        """
        self.images[image_type] = "{:02d}".format(image_num)

    def store_json(self, assets_json):
        """Store the full, parsed assets.json file for reference.

        Args:
            assets_json (dict): Dictionary result from loading assets.json.
        """
        self.json = assets_json

    def debug_override(self, override):
        """Manually override the colors and images dictionaries.

        Args:
            override (dict): A combined dict with keys 'colors' and 'images'.
        """
        self.colors = override['colors']
        self.images = override['images']

    def debug(self):
        """Print out the stored colors and images settings."""
        for color in self.colors.keys():
            print(f"COLOR {color} = {self.colors[color]}")
        for image in self.images.keys():
            print(f"IMAGE {image} = {self.images[image]}")

    def get_json(self):
        """Return the colors and images dicts as one combined dict.

        Returns:
            dict: A combined dict with keys 'colors' and 'images'.
        """
        return {
            'colors': self.colors,
            'images': self.images
        }

    def get_sorted_layers(self):
        """Returns the list of image type layers in lowest to highest 'order' value.

        Returns:
            list(string): List of image type layers.
        """
        return sorted(self.json['imageTypes'].items(), key=lambda x: x[1]['order'])
