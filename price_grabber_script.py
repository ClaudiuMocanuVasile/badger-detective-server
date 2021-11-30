# Imports

import urllib.request
import sqlite3


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

    product_links = get_product_links(string)

    # Get number of pages in a subcategory

    page_as_string = page_to_string(string)

    num_of_pages = get_string('<span class="title-phrasing title-phrasing-sm">', ' de produse</span>', page_as_string)

    num_of_pages = int(num_of_pages)//60 if int(num_of_pages) % 60 == 0 else int(num_of_pages)//60 + 1

    # For each page, create the link to the page, then get all product links

    for i in range(2, num_of_pages + 1):
        temp = string.split("/c?ref=search_menu_category")[0]
        temp = temp + "/p" + str(i) + "/c?ref=search_menu_category"
        product_links.extend(get_product_links(temp))
    
    return product_links



def get_product_links(string):
    """This function receives an url as an argument and returns
       all the product links in a single product grid page
    """

    page_as_string = page_to_string(string)

    start = '<div class="pad-hrz-xs">'
    end = '" class="card-v2-title'

    temp = page_as_string.split(start)

    links = []

    temp = temp[1:] # get rid of the cluster of HTML before the first link

    for item in temp:
        links.append(item.split(end)[0].strip()[9:]) # get rid of <a href=""

    return links



def return_prices(string):
    """This function receives the url of a product's page and returns
       the PRP and price of the product
    """

    # Transform page into string
    page_as_string = page_to_string(string)

    # PRP
    prp_price = get_prp_price(page_as_string).replace("&#46;","")

    print("PRP: " + prp_price + " Lei")

    # Discounted price
    discounted_price = get_price(page_as_string, prp_price).replace("&#46;","")

    print("Price: " + discounted_price + " Lei")

    if prp_price != " ":
        print("You save: " + str(float(prp_price) - float(discounted_price)) + " Lei")
    
    return prp_price, discounted_price



def get_prp_price(string):
    """This function receives a webpage's HTML code as a string, extracts the PRP
       (price recommended by producer) of a product, if it has one, and returns it
    """

    integer = ""

    # Separate string with PRP
    prp = get_string('"pricing rrp-lp30d"', "</P", string)

    # Rare case when there's no PRP, but the "lowest price in the last 30 days" is displayed (allegedly, we'll see about that)
    if "<s>" in prp and "</s>" in prp:
        prp = "<custom>" + get_string('<s>', "</s>", string)
        print(prp)
        # Get integer of PRP
        integer = get_string("<custom>", "<sup>", prp)
    elif prp.strip() == ">":
        # Some products don't have PRP
        return " "
    elif "Separat" in prp:
        integer = get_string("Separat: ", "<sup>", prp)
    else:
        # Get integer of PRP
        integer = get_string("PRP: ", "<sup>", prp)
    
    # Get decimals of PRP
    decimals = get_string("<sup>", "</sup>", prp)
    
    return integer + "." + decimals



def get_price(string, prp):
    """This function receives a webpage's HTML code as a string, extracts the price
       of a product and returns it
    """

    # Separate string with discounted price
    if prp == " ":
        discounted_price = get_string('"product-new-price"', "<span>", string)
    else:
        discounted_price = get_string('"product-new-price has-deal"', "<span>", string)

    # Get decimals of discounted price
    decimals = get_string("<sup>", "</sup>", discounted_price)

    # Get integer of discounted price
    integer = get_string('>', '<sup', discounted_price)

    return integer + "." + decimals



# Main

if __name__ == "__main__":

    
    product_submenu_link = "https://www.emag.ro/telefoane-mobile/c?ref=search_menu_category"

    product_links = return_product_links(product_submenu_link)

    for item in product_links:
        print(item)
        return_prices(item)