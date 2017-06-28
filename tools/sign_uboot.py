#!/usr/bin/python
"""
     @author wangmeng <wangmeng@leadcoretech.com>
     @usage:
         this is used to sign a file with PKCS 1.5 alg.
         by execute python sign.py signkey.pub signkey.priv file
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

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

def dump_key(key, f=None):
    #N
    N = rsa_key.n
    #nwords
    nwords = N.bit_length() / 32
    B = 0x100000000
    N0inv = B - modinv(N, B)

    R = 2 ** (N.bit_length())
    RR = (R * R) % N

    print 'dump public key:', nwords, '|', N0inv, '|',
    if f:
        f.write(struct.pack('<I',nwords))
        f.write(struct.pack('<I',N0inv))

    #N
    for i in xrange(nwords):
        n = N % B
        print n,
        if f:
            f.write(struct.pack('<I',n))
        N = N/B
    #RR
    print '|',
    for i in xrange(nwords):
        rr = RR % B
        print rr,
        if f:
            f.write(struct.pack('<I',rr))
        RR = RR / B
    #E
    E = rsa_key.e
    print '|', E
    if f:
        f.write(struct.pack('<I',E))

# write n p to f, p should: 0 <= p < 2^32
def padding(f, n, p):
    for i in xrange(n):
        f.write(struct.pack('<I', p))

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python ' + sys.argv[0] + ' pubkey privatekey file'
        exit(1)

    p_key=sys.argv[1]
    s_key=sys.argv[2]
    f=sys.argv[3]

    f_src = open(f, 'rb')
    f_out = open(f+'.signed', 'wb')

    #write f_src len.
    f_src.seek(0, 2)
    print 'file length=', f_src.tell()
    f_out.write(struct.pack('<I', f_src.tell())) # 0-3
    padding(f_out, 127, 0x0) # padding 4-511
    f_src.seek(0, 0)

    rsa_key = RSA.importKey(open(p_key, "rb").read())
    print rsa_key
    rsa_s = RSA.importKey(open(s_key, "rb").read())
    print rsa_s

    h = SHA256.new(f_src.read())
    signer = PKCS1_v1_5.new(rsa_s)
    print signer
    s=signer.sign(h)

    print 'file ' + f + ' HASH256 is:', h.hexdigest()
    print '\nsignater in hex:',
    s_hex=''
    for i in xrange(len(s)):
        s_hex += ('%02x' % (ord(s[i])))
    print s_hex
    #write signature
    f_out.write(s) # 512-767

    print '\nRSAPublicKey e=', rsa_key.e
    print '\nRSAPublicKey n=', rsa_key.n
    #write pulic key
    dump_key(rsa_key, f_out) #768-1291
    padding(f_out, 61, 0x0) #1292-1535

    f_src.seek(0, 0)
    #write file
    f_out.write(f_src.read())
    f_src.close()
    f_out.close()

    verifier = PKCS1_v1_5.new(rsa_key)
    if verifier.verify(h, s):
        print "\ntest verity:", True
    else:
        print "\ntest verity:", False
 
    #hp = SHA256.new(rsa_key.)
    #print 'pubkey hash256 is:', hp.hexdigest()

