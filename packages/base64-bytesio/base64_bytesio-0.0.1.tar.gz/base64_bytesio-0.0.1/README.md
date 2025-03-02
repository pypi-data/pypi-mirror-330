<!--
 * @Author: Bryan x23399937@student.ncirl.ie
 * @Date: 2025-03-01 12:23:20
 * @LastEditors: Bryan x23399937@student.ncirl.ie
 * @LastEditTime: 2025-03-01 15:56:14
 * @FilePath: /base64_bytesio/README.md
 * @Description: 
 * readme
 * Copyright (c) 2025 by Bryan Jiang, All Rights Reserved. 
-->
# base64_bytesio

This library provides functionality to decode base64 encoded files and return them as `BytesIO` objects.

## Scenario

When your website using base64 as image format. And front-end will upload some images to your django back-end.
In django framework mostly using file object to recieve image. In this moment, you may need to convert base64 to a bytes io object. Meantime, In our scenario I don't need to save my file on server. Just upload AWS s3 bucket that will fine.

## Installation

You can install the library via pip:

```bash
pip install base64_bytesio
```

## Usages

Example of using the library
```
from base64_bytesio import Base64BytesIO

data = "data:image/jpeg;base64,..."
decoder = Base64BytesIO()
file_object, filename = decoder.decode(data)
```