for each in mmcblk0boot0 mmcblk0boot1 mmcblk0p1 mmcblk0p10 mmcblk0p11 mmcblk0p12 mmcblk0p13 mmcblk0p14 mmcblk0p2 mmcblk0p3 mmcblk0p4 mmcblk0p5 mmcblk0p6 mmcblk0p7 mmcblk0p8 mmcblk0p9 mmcblk0rpmb; do  echo $each: ; busybox dd if=$each bs=1024 | busybox nc 192.168.42.3 1234; sleep 2 ; done

