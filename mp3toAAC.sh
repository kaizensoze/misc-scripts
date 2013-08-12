#!/usr/bin/env zsh

for x in *.mp3; do
    eval "ffmpeg -n -i '$x' -c:a libfaac '${x:r}.m4a'"
    mv $x ~/.Trash/$x
done

