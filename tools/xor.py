#!/usr/bin/env python2
######################
# Powershell XOR 2 Files
# xor.py
# Jul 2016
# Website: http://www.Megabeets.net
# Use: ./xor.py file1 file2 outputFile
# Example: ./xor.py C:\a.txt C:\b.txt C:\result.txt
#######################
 
import sys
 
# Read two files as byte arrays
file1_b = bytearray(open(sys.argv[1], 'rb').read())
file2_b = bytearray(open(sys.argv[2], 'rb').read())
 
# Set the length to be the smaller one
size = len(file1_b) if file1_b < file2_b else len(file2_b)
xord_byte_array = bytearray(size)
 
# XOR between the files
byte_cnt = [0] * 256
for i in range(size):
	xord_byte_array[i] = file1_b[i] ^ file2_b[i]
	byte_cnt[file1_b[i]] = byte_cnt[file1_b[i]]+1

for i in range(256):
	print str(i) + " " + str(byte_cnt[i])
 
# Write the XORd bytes to the output file	
open(sys.argv[3], 'wb').write(xord_byte_array)
 
print "[*] %s XOR %s\n[*] Saved to \033[1;33m%s\033[1;m."%(sys.argv[1], sys.argv[2], sys.argv[3])
