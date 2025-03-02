'''
Author: Bryan x23399937@student.ncirl.ie
Date: 2025-03-01 12:24:24
LastEditors: Bryan x23399937@student.ncirl.ie
LastEditTime: 2025-03-01 15:55:33
FilePath: /base64_bytesio/src/base64_bytesio/base64_bytesio.py
Description: 
using base64 format as image
you may handle image data from API json
Copyright (c) 2025 by Bryan Jiang, All Rights Reserved. 
'''
import base64
import uuid
import io
import six
import filetype

class Base64BytesIO:
    """
    input a base64 image string return readable io and randomly file name
    """
    def __init__(self, data):
        self.data = data
        self.decoded_file = None
        self.file_name = None
        self.file_extension = None
        
    def get_file_extension(self, decoded_file):
        """
        determine the file extension from the decoded file's MIME type
        """
        kind = filetype.guess(decoded_file)
        if kind is None:
            return None
        extension = kind.extension
        return "jpg" if extension == "jpeg" else extension

    def decode_base64_file(self):
        """
        to convert base 64 to readable IO bytes and auto-generate file name with extension
        """
        # Check if this is a base64 string
        if isinstance(self.data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in self.data and ';base64,' in self.data:
                # Break out the header from the base64 content
                header, self.data = self.data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(self.data)
            except TypeError:
                TypeError('invalid_image')

            # Generate file name:
            self.file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            self.file_extension = self.get_file_extension(self.decoded_file)

            complete_file_name = "%s.%s" % (self.file_name, self.file_extension,)

            return io.BytesIO(self.decoded_file), complete_file_name