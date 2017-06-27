#!/usr/bin/env python3
#
# Copyright (C) 2017  Freek van Tienen <freek.v.tienen@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import sys
import getopt
import re
import os
import hashlib
import binascii
import configparser
import itertools
from Crypto.Cipher import AES

def main(argv):
    key = bytes.fromhex(argv[0])
    text = bytes(argv[1], 'utf-8')  

    if len(key) < 16:
        key = key + ((bytes([0])) * (16 - len(key)))

    if len(text) < 32:
        text = text + ((bytes([32 - len(text)])) * (32 - len(text)))
    elif len(text) > 32:
        text = hashlib.sha256(text).digest()

    cipher = AES.new(key, AES.MODE_CBC, bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    print(cipher.encrypt(text).hex()[:-32])

if __name__ == "__main__":
    main(sys.argv[1:])
