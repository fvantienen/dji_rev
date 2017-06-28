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
from ctypes import *
from time import gmtime, strftime, strptime
from calendar import timegm
from os.path import basename

# All found keys
keys = {
    # Encryption keys
    "RREK": bytes([0x37, 0xD6, 0xD9, 0x13, 0xE5, 0xD0, 0x80, 0x17, 0xE5, 0x12, 0x15, 0x45, 0x0C, 0x1E, 0x16, 0xE7]),
    "RIEK": bytes([0xF1, 0x69, 0xC0, 0xF3, 0x8B, 0x2D, 0x9A, 0xDC, 0x65, 0xEE, 0x0C, 0x57, 0x83, 0x32, 0x94, 0xE9]),
    "RUEK": bytes([0x9C, 0xDA, 0xF6, 0x27, 0x4E, 0xCB, 0x78, 0xF3, 0xED, 0xDC, 0xE5, 0x26, 0xBC, 0xEC, 0x66, 0xF8]),
    "PUEK": bytes([0x70, 0xe0, 0x03, 0x08, 0xe0, 0x4b, 0x0a, 0xe2, 0xce, 0x8e, 0x07, 0xd4, 0xd6, 0x21, 0x4b, 0xb6]),
    "DRAK": bytes([0x6f, 0x70, 0x7f, 0x29, 0x62, 0x35, 0x1d, 0x75, 0xbc, 0x08, 0x9a, 0xc3, 0x4d, 0xa1, 0x19, 0xfa]),
    "SAAK": bytes([0x6f, 0x40, 0x2f, 0xb8, 0x62, 0x52, 0x05, 0xce, 0x9b, 0xdd, 0x58, 0x02, 0x17, 0xd2, 0x18, 0xd8]),
}

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

class EncHeader(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('target', c_ubyte),                #0
                ('unk0', c_ubyte * 4),              #1 Allways 01000001
                ('version', c_ubyte * 4),           #5
                ('unk1', c_ubyte),                  #9
                ('size', c_uint),                   #10
                ('unk2', c_ubyte * 9),              #14
                ('scramble_key', c_ubyte * 16),     #23
                ('crc16', c_ushort)]                #39 end is 41

    def dict_export(self):
        d = dict()
        for (varkey, vartype) in self._fields_:
            #if not varkey.startswith('unk'):
            d[varkey] = getattr(self, varkey)
        return d

    def __repr__(self):
        d = self.dict_export()
        from pprint import pformat
        return pformat(d, indent=4, width=1)

    def getTarget(self):
        tg_kind = self.target & 31
        tg_model = (self.target >> 5) & 7
        return (str(tg_kind).zfill(2) + str(tg_model).zfill(2))

    def getVersion(self):
        return ('v' + str(self.version[3]).zfill(2) + '.' + str(self.version[2]).zfill(2) + '.' + str(self.version[1]).zfill(2) + '.' + str(self.version[0]).zfill(2))


def main(argv):
    filname_wo_ext = os.path.splitext(basename(argv[0]))[0]
    image_file = open(argv[0], "rb")

    # Decode the encrypt header
    header = EncHeader()
    if image_file.readinto(header) != sizeof(header):
        raise EOFError("Couldn't read image file header.")
    print(header)

    image_file.seek(0, os.SEEK_END)
    image_size = image_file.tell()

    print('Target: ' + header.getTarget())
    print('Version: ' + header.getVersion())
    print('Unk0: ' + bytes(header.unk0[:]).hex())
    print('Unk2: ' + bytes(header.unk2[:]).hex())
    print('Scramble key: ' + bytes(header.scramble_key[:]).hex())
    print('Filesize: ' + str(image_size) + ' header.size: ' + str(header.size) + ' Missing bytes: ' + str(image_size-16-41-header.size))

    # Calculate the md5
    image_file.seek(0, 0)
    buf = image_file.read(image_size - 16)
    md5_sum = hashlib.md5(buf).digest()

    image_file.seek(image_size-16, 0)
    file_md5 = image_file.read(16)
    print('MD5 calc: ' + md5_sum.hex() + ' file: ' + file_md5.hex())

    # Add padding
    image_file.seek(41, 0)
    enc_buffer = image_file.read(header.size)
    pad_cnt = (AES.block_size - len(enc_buffer) % AES.block_size) % AES.block_size
    enc_buffer = enc_buffer + ((bytes([0])) * pad_cnt)

    # Go through all keys
    print('\nTrying decrypt options...')
    for keyname in keys:
        key = keys[keyname]
        print ('  Decrypting using key ' + keyname + ': ' + key.hex())
        # Go through decoding options
        for j in range(0, 4):
            if j == 0:
                cipher = AES.new(key, AES.MODE_CBC, bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
                scramble_key = cipher.decrypt(header.scramble_key)
                cipher_scrmb = AES.new(scramble_key, AES.MODE_CBC, bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
                print ('    Method 0 key: ' + scramble_key.hex() + ' IV: 0')
            elif j == 1:
                cipher_scrmb = AES.new(key, AES.MODE_CBC, bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
                print ('    Method 1 key: ' + key.hex() + ' IV: 0')
            elif j == 2:
                cipher_scrmb = AES.new(header.scramble_key, AES.MODE_CBC, bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
                print ('    Method 2 key: ' + bytes(header.scramble_key[:]).hex() + ' IV: 0')
            else:
                cipher_scrmb = AES.new(key, AES.MODE_CBC, header.scramble_key)
                print ('    Method 3 key: ' + key.hex() + ' IV: ' + bytes(header.scramble_key[:]).hex())

            # Decrypt the data
            dec_buffer = cipher_scrmb.decrypt(enc_buffer)
            output_file = open(filname_wo_ext + '_' + keyname+ '_' + str(j) + '.bin', "wb")
            output_file.write(dec_buffer)
            output_file.close()

    image_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])