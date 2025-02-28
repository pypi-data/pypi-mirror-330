#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'haoyang'
__date__ = '2025/1/24 08:48'

import io
import time

import pyzipper

def add_file_to_zip(file_name, file_bytes:[], password=None) -> io.BytesIO:
  zip_filename = "{}}_{}.zip".format(file_name, time.strftime('%Y-%m-%d_%H-%M-%S-%s', time.localtime(time.time())))
  zipFile = io.BytesIO()
  with pyzipper.AESZipFile(zipFile, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
    if password: zipf.setpassword(password.encode('utf-8'))
    for file in file_bytes:
      zipf.writestr(zip_filename, file)
  zipFile.seek(0)
  return zipFile
