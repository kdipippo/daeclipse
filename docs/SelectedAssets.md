# SelectedAssets


Class to handle list of colors and images gif creation. 

## Methods


### add_color


Assign the selected palette to the component to recolor.   
Args: color_type (string): Component the recolor applies to, i.e. 'hair'. selected_type (string): Palette to recolor to, i.e. 'blonde'. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
color_type |  | 
selected_type |  | 





### add_image


Assign selected image type to image num when gif parts are layered.   
Args: image_type (string): Image layer being added, i.e. 'hairbackshort'. image_num (string): Asset number for the image layer, i.e. '00A'. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
image_type |  | 
image_num |  | 





### store_json


Store the full, parsed assets.json file for reference.   
Args: assets_json (dict): Dictionary result from loading assets.json. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
assets_json |  | 





### update_json


Manually override the colors and images dictionaries.   
Args: override (dict): A combined dict with keys 'colors' and 'images'. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
override |  | 





### get_json


Return the colors and images dicts as one combined dict.   
Returns: dict: A combined dict with keys 'colors' and 'images'. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### get_sorted_layers


Returns list of type layers in lowest to highest 'order' value.   
Returns: list(string): List of image type layers. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 




