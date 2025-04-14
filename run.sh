#!/bin/bash


sed -i '/home\/o11/d' /etc/fstab
sleep 2

cat <<EOL >> /etc/fstab

tmpfs /home/o11/hls tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=70% 0 0
tmpfs /home/o11/dl tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=70% 0 0
EOL

mount -av

while true; do
  if ! pgrep "o11v4" > /dev/null; then

    /home/o11/o11v4 -p 8484 -noramfs -f /usr/bin/ffmpeg -path "/home/o11/" -noautostart -plstreamname "%s [%p]" &
    

    sleep 10
  fi
  
  sleep 20
done
