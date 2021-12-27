#!/usr/bin/python3
# use emag api
import urllib.request
import json
import sqlite3
import sys
from datetime import datetime, timedelta
import time
import os

# look at my amazing global variable
db_file_name = "product_prices.db"

def page_to_string(url):
    """This function receives an url as argument, converts the HTML code
       of the web page to a python string and returns it.
    """

    try:
        fp = urllib.request.urlopen(url)
        url = fp.read()
        string = url.decode("utf8")
        fp.close()

        return string
    except:
        return None


def parse_page(page_str):
    parsed = json.loads(page_str);
    print(parsed["data"]["title"]);

    connection = sqlite3.connect(db_file_name)

    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS products (id TEXT primary key, name TEXT, url TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS prices (pk integer primary key, id TEXT, price REAL, date TEXT)")

    time = datetime.today().strftime("%d-%m-%Y")

    try:
        for p in parsed["data"]["items"]:
            price = p["offer"]["price"]["current"]
            name = p["name"]
            id = p["part_number_key"]
            
            rows = cursor.execute("SELECT name, url FROM products WHERE id = ?", (id,)).fetchall()
            if not len(rows):
                cursor.execute("INSERT INTO products VALUES (?, ?, ?)", (id, name, "mesaj bun"))
                cursor.execute("INSERT INTO prices(id, price, date) VALUES (?, ?, ?)", (id, price, time))
            else:
                rows = cursor.execute("SELECT price FROM prices WHERE id = ? ORDER BY date DESC LIMIT 1;", (id,)).fetchall()
                if rows[0][0] != price:
                    cursor.execute("INSERT INTO prices(id, price, date) VALUES (?, ?, ?)", (id, price, time))

        connection.commit()
    except:
        return 0;
    
    return len(parsed["data"]["items"]);

def do_the_category(cat_no, offset = 0):
    link = f"https://sapi.emag.ro/search-by-filters-with-redirect?source_id=7&templates[]=full&is_eab344=false&listing_display_id=2&page[limit]=100&page[offset]={offset}&filters[category][]={cat_no}";
    page_str = page_to_string(link);
    if page_str is None:
        pass
        print("Got empty page")
        return offset
    n = parse_page(page_str);
    while n == 100:
        offset += 100
        link = f"https://sapi.emag.ro/search-by-filters-with-redirect?source_id=7&templates[]=full&is_eab344=false&listing_display_id=2&page[limit]=100&page[offset]={offset}&filters[category][]={cat_no}";
        page_str = page_to_string(link);
        if page_str is None:
            pass
            print("Got empty page")
            return offset
        n = parse_page(page_str);
        print("offset: " + str(offset));
    return None

def main():
    # aici functia principala
    print("salutare lume!!");
    log_file = "last_accesed"
    line = 0
    offset = 0
    f = open("emag_links_2021_12_27.txt");
    page = f.readlines()
    for (i, line) in enumerate(page[line:]):
        cat_no = int(line.strip().split(" ")[-2]);
        res = do_the_category(cat_no, offset);
        if res is not None:
            f = open(log_file, "w")
            f.write(f"{i} {res}")
            f.close()
            return
        offset = 0
        time.sleep(1);
    os.remove(log_file);


if( __name__ == "__main__"):
    main();
