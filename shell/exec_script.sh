#!/bin/sh
# call the script to record the prices from emag for the link in the specified
# files

script_file="../price_grabber_script.py"
links="emag_link.txt"
dir=$(dirname $0)
log_dir="logs"
# be sure we are in the write directory
[ "$dir" ] && cd $dir
echo $PWD
echo $(date) > "$log_dir/record_exec.txt"

[ -d "$log_dir" ] || mkdir "$log_dir"

while read line
do
	echo "$line"
	if [ ! $($script_file $line 2> "$log_dir/err.txt") ]
	then
		echo "$line" > "$log_dir/last_link.txt"
		exit 1
	fi
done < $links

echo "It should be done. Move the database \"product_prices.db\" where you need it"
