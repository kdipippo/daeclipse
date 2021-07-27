# DeviantArtEclipseAPI


Class to handle making calls to the DeviantArt Eclipse API. 

## Methods


### __init__


Initialize API by fetching Chrome's DeviantArt-related cookies. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### get_cookies


Return the logged-in DeviantArt user's cookies.   
Returns: http.cookiejar.CookieJar: .deviantart.com Cookie Jar. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### get_groups


Return a subset of the user's joined DeviantArt groups.   
Args: username (string): DeviantArt username of user. offset (int): Offset to start with API call. limit (int, optional): Limit of results to return. Defaults to 24.   
Returns: dict: Raw API response from API call.   
Raises: ValueError: If `limit` is greater than 24. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
username |  | 
offset |  | 
limit |  | 24





### get_group_folders


Returns folder information for the provided group_id ONLY, if cookies belong to a member of the group.   
Args: group_id (int): Group ID.   
Returns: EclipseFolder[]: List of EclipseFolder objects.   
Raises: RuntimeError: If API call returns an error payload. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
group_id |  | 
deviation_url |  | 





### add_deviation_to_group


Submit deviation to the specified folder in group.   
Args: group_id (int): Group ID. folder_id (int): Folder ID. deviation_url (string): Deviation URL.   
Returns: string: Success message of result.   
Raises: RuntimeError: If API call returns an error payload. 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
group_id |  | 
folder_id |  | 
deviation_url |  | 




