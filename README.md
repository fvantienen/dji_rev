# Reverse Engineering of DJI products
This repository contains tools for reverse engineering DJI products.
- `tools/image.py` is a tool to extract sig and image files
- `tools/derive_key.py` is a script that mimics the dji_derivekey binary
- `tools/sign_uboot.py` is a script that is capable of signing the secure U-boot parition
- `tools/check_uboot.py` is a script that checks the U-Boot signature and extracts it

## Image structure
- Header
  - 4B Magic ("IM*H")
  - 4B Version (Currenly only 1 is seen)
  - 8B ??
  - 4B Header size
  - 4B RSA signature size
  - 4B Payload size
  - 12B Unknown
  - 4B Auth key identifier
  - 4B Encryption key identifier
  - 16B Scramble key
  - 32B Image name
  - 60B ??
  - 4B Block count
  - 32B SHA256 payload
- Per Block info
  - 4B Name
  - 4B Start offset
  - 4B Output size
  - 4B Attributes (Last bit 0 means ecrypted)
  - 16B ??
- RSA Signature of the Header (Size and Auth key described in header)
- Actual block data (Start offset 0)