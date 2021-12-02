#!/usr/bin/python3
# Imports

import urllib.request
import sqlite3
import sys

# display usage message
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

def get_string(start, end, string):
    """This function receives three strings as arguments and returns the
       characters found in the string between start and end substrings
    """

    found_string = (string.split(start))[1].split(end)[0]

    return found_string

def return_product_links(string):
    """This function receives an url as an argument, finds the number of products,
       computes the number of pages used for product pagination in a subcategory,
       iterates through all the pages, creates a list with all the product links
       and returns them
    """

    # Get number of pages in a subcategory

    pages = [string]

    page_as_string = page_to_string(string)

    num_of_pages = get_string('<span class="title-phrasing title-phrasing-sm">', ' de produse</span>', page_as_string)

    num_of_pages = int(num_of_pages)//60 if int(num_of_pages) % 60 == 0 else int(num_of_pages)//60 + 1

    # For each page, create the link to the page, then get all product links

    for i in range(2, num_of_pages + 1):
        temp = string.split("/c?ref=search_menu_category")[0]
        temp = temp + "/p" + str(i) + "/c?ref=search_menu_category"
        pages.append(temp)

    return pages

# get price of a product
# @product: string, the <div class="card-v2"> stuff
# @return: int, the price as int
def get_price(product):
    row = product.split("class=\"product-new-price\">")
    if len(row) > 1:
        row = row[1].split('\n')[0]
    else:
        # pret "de la"
        row = product.split("class=\"product-new-price unfair-price\">")[1]
        row = row.split("</span>")[1]
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
# @tag_str: string, the tag like p for <p>
# @type_str: string, the rest of the arguments inside the tag like class=...
# @return list of strings from inside tags '<tag_str type_str>'
def izolate_html_class(page_str, tag_str, type_str):
    target=f'<{tag_str} class="{type_str}">'
    pp = page_str.split(target)[1:]

    opened=f"<{tag_str}"
    closed=f"</{tag_str}>"
    res = []
    for p in pp:
        line = ""
        count = 1
        for word in p.split(" "):
            if len(line) > 0:
                line += " "
            if opened in word:
                count += word.count(opened)
            if closed in word:
                count -= word.count(closed)
            if count == 0:
                break
            line += word
        res.append(line)
    return res

# short test for izolate_html_class
def test():
    f = open("/tmp/clip", "r")
    page = f.read()
    f.close()
    iz = izolate_html_class(page, "div", "class=\"card-v2\"")
    print(iz)

# Main
def main():

    if len(sys.argv) != 2:
        usage(sys.argv[0])
        return

    links = return_product_links(sys.argv[1])

    for link in links:
        print(link)
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
