COLLAGE = $(shell find . -type d -name '*.collage')

all: $(COLLAGE:%.collage=%.collage.png)

%.collage.png:
	montage -mode concatenate -font Arial -pointsize 24 -label '%[basename]' -gravity center -border 5 -tile 2x -geometry 1200x300\>+10+10 "$*.collage/*.png" $@
