#!/usr/bin/python
"""
     @author wangmeng <wangmeng@leadcoretech.com> and freek van tienen <freek.v.tienen@gmail.com>
     @usage:
         this is used to sign a file with PKCS 1.5 alg.
         by execute python sign.py file
         will gen a file with name file.signed which has a structure like blow:
         file-len<0-3>|padding<4-511>|signature<512-767>|rsapubkey<768-1291>|padding<1292-1535>|file<1536->

"""

import base64
import ssl
import struct
import sys

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python ' + sys.argv[0] + ' file'
        exit(1)

    f=sys.argv[1]

    f_src = open(f, 'rb')

    #write f_src len.
    f_src.seek(0, 0)
    file_len = struct.unpack('<I', f_src.read(4))[0]
    print 'file length:', file_len

    f_src.seek(512, 0)
    s = f_src.read(256)
    print '\nsignature in hex:',
    s_hex=''
    for i in xrange(len(s)):
        s_hex += ('%02x' % (ord(s[i])))
    print s_hex

    key_nwords = struct.unpack('<I',f_src.read(4))[0]
    key_N0inv = struct.unpack('<I',f_src.read(4))[0]
    print 'Key nwords:', key_nwords
    print 'Key N0inv:', key_N0inv

    print 'Key N: ',
    key_N = long(0)
    mul = long(1)
    for i in xrange(key_nwords):
        n = struct.unpack('<I', f_src.read(4))[0]
        key_N += n * mul
        mul = mul*0x100000000
        print n,
    print '\nKey calN: ', key_N

    print 'Key RR: ',
    key_RR = long(0)
    mul = long(1)
    for i in xrange(key_nwords):
        rr = struct.unpack('<I', f_src.read(4))[0]
        key_RR += rr * mul
        mul = mul*0x100000000
        print rr,
    print '\nKey calRR: ', key_RR

    key_e = struct.unpack('<I', f_src.read(4))[0]
    print 'Key E: ', key_e

    rsa_key = RSA.construct((key_N, long(key_e))).publickey()
    print 'Key:\n', rsa_key.exportKey()

    f_src.seek(1536, 0)
    h = SHA256.new(f_src.read(file_len))
    verifier = PKCS1_v1_5.new(rsa_key)
    if verifier.verify(h, s):
        print "\ntest verity:", True
    else:
        print "\ntest verity:", False


    f_src.seek(768, 0)
    h_efuse = SHA256.new(f_src.read(524))
    print 'Efuse Hash:', h_efuse.hexdigest()
    f_src.close()
