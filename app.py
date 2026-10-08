from datetime import datetime
import json
import sqlite3
from bs4 import BeautifulSoup
import requests

DB_NAME="price_tracker.db"

def initialize_database():
    conn= sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute( """
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE
        )                
""")

    cursor.execute (""" 
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            date TEXT,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )

""")

    conn.commit()
    conn.close()

def track_product(url):
    initialize_database()

    headers = {
        "User-Agent":(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) """
            "AppleWebKit/537.36 (KHTML, like Gecko)"""
            " Chrome/155.0.0.0 ""Safari/537.36 OPR/136.0.0.0"
        ), 
        "Accept-Language": "en-US,en;q=0.9" ,
    }

    title = None
    price = None

    try:
        print ("\n[+] Connecting to the website...")
        response= requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup=BeautifulSoup(response.text, "html.parser")

            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get("@type") == "Product":
                        title = data.get("name")
                        offers = data.get("offers")
                        if isinstance(offers, dict):
                            price = float(offers.get("price"))
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("@type") == "Product":
                                title = item.get("name")
                                offers = item.get("offers")
                                if isinstance(offers, dict):
                                    price = float(offers.get("price"))
                except Exception:
                    continue

                if not title:
                    og_title =soup.find("meta", property="og:title")
                    if og_title:
                        title=og_title.get("content")

                if not price:
                    og_price=soup.find("meta", property="og:title") or soup.find("meta", property="og:price:amount")
                    if og_price:
                        try:
                            price=float(og_price.get("content"))
                        except ValueError:
                            pass
    except Exception as e:
        print (f"[-] Network notice: {e}")

    if not price:
        print(
            "\n[!] Website security blocked automatic price reading (Anti-bot"
            " protection)."
        )
        print(
        "[i] Don't worry! You can type the current price manually to log it"
        " into SQLite."
        )

        if not title:
            title= input("enter product name manually: "). strip()

        while True:
            try:
                price_input=input(
                    "enter current price"
                ).strip()
                price=float(price_input)
                break
            except ValueError:
                print ("[-] Invalid number. Please only digits")
    else:
        if not title:
            title="tracked product"  


    print(f"\n[+] Product: {title}")
    print(f"[+] Price Logged: {price}")

      #database things
    conn.sqlite3.connect(DB_NAME)
    cursor.conn.cursor()

    cursor.execute("SELECT id FROM products WHERE url = ?", (url,))
    result = cursor.fetchone()

    if result:
        product_id=result[0]
        print("[+] Product already exists in database. Adding new price entry...")
    else:
        cursor.execute(
            "INSERT INTO products (title, url) VALUES (?, ?)", (title, url)
        )
        product_id=cursor.lastrowid
        print("[+] Added new product to database.")

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "INSERT INTO price_history (product_id, price, date) VALUES (?, ?, ?)",
        (product_id, price, current_date),
  )

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Price saved successfully in SQLite at {current_date}!\n")


if __name__ == "__main__":
    user_url = input("Paste your product URL here and press Enter: ").strip()

    if user_url:
        track_product(user_url)
    else:
        print("[!] No URL entered.")


