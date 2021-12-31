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
echo $(date) >> "$log_dir/record_exec.txt"

[ -d "$log_dir" ] || mkdir "$log_dir"

call_script()
{
	while read line
	do
		echo "$line"
		if [ ! $($script_file $line 2> "$log_dir/err.txt") ]
		then
			echo "$line" > "$log_dir/last_link.txt"
			exit 1
		fi
	done
}

# if there was an error get the last accessed link and start from there
if [ -f "$log_dir/last_link.txt" ]
then
	last_link=$(cat "$log_dir/last_link.txt")
	line=$(grep -n "$last_link" "$links" | cut -f1 -d":")
	echo "Last link line: $line"
	sed -n "$line,\$ p" $links | call_script
else
	call_script < $links
fi

echo "It should be done. Move the database \"product_prices.db\" where you need it"
[ -f "$log_dir/last_link.txt" ] && rm "$log_dir/last_link.txt" 
