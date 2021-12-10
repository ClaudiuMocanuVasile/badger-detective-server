#!/bin/sh
# call the script to record the prices from emag for the link in the specified
# files

script_file="../price_grabber_script.py"
links="emag_link.txt"
dir=$(dirname $0)
# be sure we are in the write directory
[ "$dir" ] && cd $dir
echo $PWD

while read line
do
	$script_file $line
done < $links
