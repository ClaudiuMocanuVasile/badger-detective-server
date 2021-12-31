#!/bin/sh
# get the basic information about products from emag.ro like the name, url and price

usage()
{
	echo "Usage $(basename $1) URL"
	echo "\tMake sure the URL is a category page not a product"
	exit 1
}

[ $# -ne 1 ] && usage $0
URL=${1?'Unde plm e URL-ul ala???'}

file="/tmp/produse.html"
wget -O $file $URL

# change the html code with a dot
sed -i 's/&#46;/./g' $file
# get the produs name, url and price
sed -n 's|\s*<a href="\([^"]*\)" class="card-v2-title [^>]*>\([^<]*\)</a>|URL: \1\nName: \2|p;
s|\s*</P><p class="product-new-price">\([0-9.]*\)<sup>\([0-9.]*\)</sup>.*|Price: \1.\2|p' < $file

# clean up
rm $file
