#! /bin/bash
IMAGE=$1
BASENAME=$(sed -Ee 's/(.*)\.[A-Za-z0-9]+$/\1/' <<< $IMAGE)
EXT=$(sed -Ee 's/.*\.([A-Za-z0-9]+)$/\1/' <<< $IMAGE)

convert $IMAGE -crop 20%x20% -resize 128x128 +repage result/${BASENAME}_%02d.$EXT
