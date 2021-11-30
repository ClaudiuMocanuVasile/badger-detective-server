#!/usr/bin/python3
# Imports

import urllib.request
import sqlite3
import sys

def usage(prog):
    print(f"Usage: {prog} URL")
    print("The URL has to be from a category page, not a product page")
    sys.exit(1)


# Functions

def page_to_string(url):
    """This function receives an url as argument, converts the HTML code
       of the web page to a python string and returns it.
    """

    fp = urllib.request.urlopen(url)
    url = fp.read()
    string = url.decode("utf8")
    fp.close()

    return string

# get price of a product
# @product: string, the <div class="card-v2"> stuff
# @return: int, the price as int
def get_price(product):
    row = product.split("class=\"product-new-price\">")[1].split('\n')[0]
    money = row.split("<sup>");
    hi = money[0].replace("&#46;","")
    lo = money[1].split("<")[0]
    return float(f"{hi}.{lo}")

# get the name of product
# @product: string
# @return: string, the name
def get_name(product):
    row = product.split("data-zone=\"title\">")[1]
    return row.split("</a>")[0];

# get the url of product
# @product: string
# @return: string, the url
def get_url(product):
    row = product.split("card-v2-info\"><a href=\"")[1]
    url = row.split('"')[0]
    return url

# izolates the tags of the specified class
# @page_str: string, the html page
# @return list of strings of '<div class="card-v2">'
def izolate_html_class(page_str, tag_str, class_str):
    """
    Bug: Doesn't look for the closing </tag>
    So you may not get what you expect
    """
    target=f"<{tag_str} class=\"{class_str}\">"
    pp = page_str.split(target)[1:]
    return pp

# Main
def main():
    
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        return

    link = sys.argv[1]
    page = page_to_string(link)
    products = izolate_html_class(page, "div", "card-v2");
    for p in products:
        price = get_price(p);
        name = get_name(p);
        url = get_url(p);
        print(f"URL: {url}")
        print(f"Name: {name}")
        print(f"Price: {price}")

if __name__ == "__main__":
   main() 
