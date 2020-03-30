#!/usr/bin/python3

import os,base64

def base64_to_image(img_name,base_64_code):
    imagedata = base64.b64decode(base_64_code)
    file = open(img_name, "wb")
    file.write(imagedata)
    file.close()