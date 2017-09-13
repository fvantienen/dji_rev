# Reverse Engineering of DJI products
This repository contains tools for reverse engineering DJI products.
- `tools/image.py` is a tool to extract sig and image files
- `tools/derive_key.py` is a script that mimics the dji_derivekey binary
- `tools/sign_uboot.py` is a script that is capable of signing the secure U-boot parition
- `tools/check_uboot.py` is a script that checks the U-Boot signature and extracts it
- `tools/fw_dec.py` is a tool to analyse FC and ESC firmware and try different key schedules

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

### #DeejayeyeHackingClub information repos aka "The OG's" (Original Gangsters)
http://dji.retroroms.info/ - "Wiki"

https://github.com/fvantienen/dji_rev - This repository contains tools for reverse engineering DJI product firmware images.

https://github.com/Bin4ry/deejayeye-modder - APK "tweaks" for settings & "mods" for additional / altered functionality

https://github.com/hdnes/pyduml - Assistant-less firmware pushes and DUMLHacks referred to as DUMBHerring when used with "fireworks.tar" from RedHerring. DJI silently changes Assistant? great... we will just stop using it.

https://github.com/MAVProxyUser/P0VsRedHerring - RedHerring, aka "July 4th Independence Day exploit", "FTPD directory transversal 0day", etc. (Requires Assistant). We all needed a *public* root exploit... why not burn some 0day?

https://github.com/MAVProxyUser/dji_system.bin - Current Archive of dji_system.bin files that compose firmware updates referenced by MD5 sum. These can be used to upgrade and downgrade, and root your I2, P4, Mavic, Spark, Goggles, and Mavic RC to your hearts content. (Use with pyduml or DUMLDore)

https://github.com/MAVProxyUser/firm_cache - Extracted contents of dji_system.bin, in the future will be used to mix and match pieces of firmware for custom upgrade files. This repo was previously private... it is now open.

https://github.com/MAVProxyUser/DUMLrub - Ruby port of PyDUML, and firmware cherry picking tool. Allows rolling of custom firmware images.  

https://github.com/jezzab/DUMLdore - Even windows users need some love, so DUMLDore was created to help archive, and flash dji_system.bin files on windows platforms.

https://github.com/MAVProxyUser/DJI_ftpd_aes_unscramble - DJI has modified the GPL Busybox ftpd on Mavic, Spark, & Inspire 2 to include AES scrambling of downloaded files... this tool will reverse the scrambling

https://github.com/darksimpson/jdjitools - Java DJI Tools, a collection of various tools/snippets tied in one CLI shell-like application
