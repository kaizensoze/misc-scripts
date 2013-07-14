#!/bin/zsh

src="$HOME/Downloads/Adobe CS6 Master Collection (Mac)/amtlib.framework"

paths=(/Applications/Adobe*CS6 "/Applications/Adobe Acrobat X Pro")

for x in $paths; do
    for y in $x/*.app; do
        sudo cp -Rv $src $y/Contents/Frameworks/
    done
done
