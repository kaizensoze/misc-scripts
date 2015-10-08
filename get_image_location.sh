#!/bin/sh

if [ "$#" -ne 1 ]; then
  echo "usage: $0 [image]"
  exit 1
fi

# latitude
lat_part1=`identify -verbose $1 | grep 'GPSLatitude:' | awk -F',|:' '{ print $3, $4, $5 }'`
lat_part2=`identify -verbose $1 | grep 'GPSLatitudeRef:' | awk '{ print $2 }'`

if [ -z "$lat_part1" ]; then
  echo "No location data found."
  exit 1
fi

lat1=`echo $lat_part1 | awk '{ print "scale=0; "$1 }' | bc -l`
lat2=`echo $lat_part1 | awk '{ print "scale=0; "$2 }' | bc -l`
lat3=`echo $lat_part1 | awk '{ print "scale=4; "$3 }' | bc -l`

lat="$lat1\xc2\xb0 $lat2' $lat3\" $lat_part2"

# longitude
lng_part1=`identify -verbose $1 | grep 'GPSLongitude:' | awk -F',|:' '{ print $3, $4, $5 }'`
lng_part2=`identify -verbose $1 | grep 'GPSLongitudeRef:' | awk '{ print $2 }'`

lng1=`echo $lng_part1 | awk '{ print "scale=0; "$1}' | bc -l`
lng2=`echo $lng_part1 | awk '{ print "scale=0; "$2}' | bc -l`
lng3=`echo $lng_part1 | awk '{ print "scale=4; "$3}' | bc -l`

lng="$lng1\xc2\xb0 $lng2' $lng3\" $lng_part2"

lat_stripped="${lat//[[:space:]]/}"
lng_stripped="${lng//[[:space:]]/}"

url="https://www.google.com/maps/place/$lat_stripped+$lng_stripped"

echo $url
