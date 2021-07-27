# Python Documentation

## Classes

**[SelectedAssets](SelectedAssets.md)**: Class to handle list of colors and images gif creation. 

**[DeviantArtEclipseAPI](DeviantArtEclipseAPI.md)**: Class to handle making calls to the DeviantArt Eclipse API. 

**[EclipseUser](EclipseUser.md)**: Model to represent DeviantArt Eclipse User. 

**[EclipseDeviation](EclipseDeviation.md)**: Model to represent DeviantArt Eclipse Deviation. 

**[EclipseFolder](EclipseFolder.md)**: Model to represent DeviantArt Eclipse Group Folder. 

**[EclipseStats](EclipseStats.md)**: Model to represent DeviantArt Eclipse Deviation Stats. 


## Functions

### gif_preset


Generate an animated pixel icon gif based on a stored preset. 




### gif_random


Generate an animated pixel icon gif with randomized assets. 




### add_art_to_groups


Submit DeviantArt deviation to groups. 
#### Parameters
name | description | default
--- | --- | ---
save |  | 





### get_username_from_url


Regex parse deviation URL to retrieve username.   
Args: deviation_url (string): Deviation URL.   
Raises: RuntimeError: If username is not present in URL string.   
Returns: string: DeviantArt username. 
#### Parameters
name | description | default
--- | --- | ---
deviation_url |  | 





### get_group_names


Return list of group names from list of dicts.   
Args: groups (dict[]): List of dicts containing group information.   
Returns: string[]: List of group names. 
#### Parameters
name | description | default
--- | --- | ---
groups |  | 





### get_folder_names


Return list of folder names from list of EclipseFolder objects.   
Args: folders (EclipseFolder[]): List of EclipseFolder objects.   
Returns: string[]: List of folder names. 
#### Parameters
name | description | default
--- | --- | ---
folders |  | 





### handle_selected_group


Submit DeviantArt deviation to group and return response.   
Args: eclipse (Eclipse): Eclipse API class instance. group_name (string): Group name. group_id (int): Group ID. deviation_url (string): Deviation URL.   
Returns: boolean, string: success status and result message. 
#### Parameters
name | description | default
--- | --- | ---
eclipse |  | 
group_name |  | 
group_id |  | 
deviation_url |  | 





### format_msg


Return formatted status message for CLI output.   
Args: group_name (string): Group name. folder_name (string): Folder name. message (string): Status message.   
Returns: string: Formatted status message containing all arguments. 
#### Parameters
name | description | default
--- | --- | ---
group_name |  | 
folder_name |  | 
message |  | 





### bob_down


Returns whether the sprite is bobbing down, false if bobbing up.   
Args: frame_num (int): Current frame number.   
Returns: boolean: True if sprite is bobbing down, false if bobbing up. 
#### Parameters
name | description | default
--- | --- | ---
frame_num |  | 





### translate_image


Return a translated image.   
Args: image (Image): Image object. direction (string): "left", "right", "up", or "down". pixels (int): Number of pixels to translate.   
Returns: Image: Translated Image object. 
#### Parameters
name | description | default
--- | --- | ---
image |  | 
direction |  | 
pixels |  | 





### get_filename


Returns path to the given image asset.   
Args: image_type (string): Type of image, i.e. 'hairfront', 'eyes'. asset_name (string): Asset name, may have position letter, i.e. '00A'.   
Returns: string: Path to image asset. 
#### Parameters
name | description | default
--- | --- | ---
image_type |  | 
asset_name |  | 





### get_custom_asset


Get the Image object for a custom asset.   
Args: image_type (string): Type of image, i.e. 'hairfront', 'eyes'. asset_name (string): Asset number, i.e. '00'. frame_num (int): Current frame number.   
Returns: Image: Requested Image object. 
#### Parameters
name | description | default
--- | --- | ---
image_type |  | 
asset_name |  | 
frame_num |  | 





### get_2frame_asset


Get Image object for a 2-frame asset.   
Args: image_type (string): Type of image, i.e. 'hairfront', 'eyes'. asset_name (string): Asset number, i.e. '00'. frame_num (int): Current frame number.   
Returns: Image: Requested Image object. 
#### Parameters
name | description | default
--- | --- | ---
image_type |  | 
asset_name |  | 
frame_num |  | 





### get_rgba_from_hex


Convert hex color string to rgba color tuple.   
Args: hex_string (string): hex color string, i.e. 79ede2.   
Returns: tuple: 4-entry int tuple representing rgba, i.e. (121, 237, 226, 255). 
#### Parameters
name | description | default
--- | --- | ---
hex_string |  | 





### update_palette


Recolor given image with array of 'before' colors to array of 'after'.   
Args: before_img (Image): Image object with mode 'RGBA' to be recolored. before_colors (list(tuple)): RGBA colors that will be recolored. after_colors (list(tuples)): RGBA colors to be used for recoloring.   
Returns: Image: Recolored Image object. 
#### Parameters
name | description | default
--- | --- | ---
before_img |  | 
before_colors |  | 
after_colors |  | 





### make_transparent


Return image with a transparent background.   
Args: img (Image): Image object.   
Returns: Image: Image object with a transparent background. 
#### Parameters
name | description | default
--- | --- | ---
img |  | 





### change_color


Recolor an image with a provided palette of colors.   
Args: img (Image): Image object. color_dict (dict): Dict that maps palette name to string of hex colors. default_color (string): Before palette name for asset, i.e. 'pink'. new_color (string): After palette name to recolor asset, i.e. 'orange'.   
Returns: Image: Recolored Image object. 
#### Parameters
name | description | default
--- | --- | ---
img |  | 
color_dict |  | 
default_color |  | 
new_color |  | 





### get_frame


Assemble a single frame of the gif.   
Args: frame_num (int): Current frame number. assets (SelectedAssets): SelectedAssets object.   
Returns: Image: Frame as an Image object. 
#### Parameters
name | description | default
--- | --- | ---
frame_num |  | 
assets |  | 





### get_gif


Assemble and combine list of frames and save gif.   
Args: assets (SelectedAssets): SelectedAssets object. current_time (string): Current time, i.e. '2020-03-16_12:02:08AM'. 
#### Parameters
name | description | default
--- | --- | ---
assets |  | 
current_time |  | 





### get_random_asset_list


Randomize and return the list of colors and components.   
Args: assets_json (dict): Parsed assets.json file as a dictionary.   
Returns: SelectedAssets: SelectedAssets object. 
#### Parameters
name | description | default
--- | --- | ---
assets_json |  | 





### get_preset_asset_list


Convert preset dict to SelectedAssets object.   
Args: preset (dict): Dict containing colors and images specification.   
Returns: SelectedAssets: SelectedAssets object. 
#### Parameters
name | description | default
--- | --- | ---
preset |  | 





### get_json


Create a json file with the generated asset settings.   
Args: assets (SelectedAssets): SelectedAssets object. current_time (string): Current time, i.e. '2020-03-16_12:02:08AM'. 
#### Parameters
name | description | default
--- | --- | ---
assets |  | 
current_time |  | 





### load_assets


Return the contents of assets.yaml as a dict.   
Returns: dict: assets.yaml contents. 




### get_presets


Return the list of preset names.   
Returns: string[]: List of preset names stored in assets.yaml. 




### create_gif_preset


Generate an animated pixel icon gif based on a stored preset.   
Returns: string: Full path to the gif result. 
#### Parameters
name | description | default
--- | --- | ---
preset_name |  | 





### create_gif_random


Generate an animated pixel icon gif with randomized assets.   
Returns: string: Full path to the gif result. 




### get_deviation_id


Extract the deviation_id from the full deviantart image URL.   
Args: deviation_url (string): Deviation URL. 
#### Parameters
name | description | default
--- | --- | ---
deviation_url |  | 





### get_csrf


Scrape deviation page for CSRF token.   
Args: deviation_url (string): Deviation URL. cookie (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.   
Returns: string: CSRF validation token. 
#### Parameters
name | description | default
--- | --- | ---
deviation_url |  | 
cookies |  | 





### query_string


Convert a dictionary into a query string URI.   
Args: query_dict (dict): Dictionary of query keys and values.   
Returns: string: Query string, i.e. ?query1=value&query2=value. 
#### Parameters
name | description | default
--- | --- | ---
query_dict |  | 




