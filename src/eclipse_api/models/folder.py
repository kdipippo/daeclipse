#!/usr/bin/env python
"""Model to represent DeviantArt Eclipse Group Folder."""

from deviation import EclipseDeviation
from user import EclipseUser

class EclipseFolder:
    """Model to represent DeviantArt Eclipse Group Folder."""

    def __init__(self, input_dict = None):
        self.folder_id = None
        self.gallection_uuid = None
        self.parent_id = None
        self.type = None
        self.name = None
        self.description = None
        self.owner = None
        self.comment_count = None
        self.size = None
        self.thumb = None
        self.has_sub_folders = None
        self.total_item_count = None
        if input_dict is not None and isinstance(input_dict, dict):
            self.from_dict(input_dict)

    def __repr__(self):
        return self.folder_id

    def from_dict(self, input_dict):
        """Convert input_dict values to class attributes.

        Args:
            input_dict (dict): Dict containing EclipseFolder fields.
        """
        if 'folderId' in input_dict:
            self.folder_id = input_dict['folderId']
        if 'gallectionUuid' in input_dict:
            self.gallection_uuid = input_dict['gallectionUuid']
        if 'parentId' in input_dict:
            self.parent_id = input_dict['parentId']
        if 'type' in input_dict:
            self.type = input_dict['type']
        if 'name' in input_dict:
            self.name = input_dict['name']
        if 'description' in input_dict:
            self.description = input_dict['description']
        if 'owner' in input_dict:
            self.owner = EclipseUser()
            self.owner.from_dict(input_dict['owner'])
        if 'commentCount' in input_dict:
            self.comment_count = input_dict['commentCount']
        if 'size' in input_dict:
            self.size = input_dict['size']
        if 'thumb' in input_dict:
            self.thumb = EclipseDeviation()
            self.thumb.from_dict(input_dict['thumb'])
        if 'hasSubfolders' in input_dict:
            self.has_sub_folders = input_dict['hasSubfolders']
        if 'totalItemCount' in input_dict:
            self.total_item_count = input_dict['totalItemCount']
