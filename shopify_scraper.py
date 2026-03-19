import requests
import pymongo
import csv
import os

stores = [
    "https://gymshark.com",
    "https://fashionnova.com",
    "https://colourpop.com"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_products(store, page):
    url = f"{store}/products.json?page={page}"
    res = requests.get(url, headers=headers)
    return res.json()

def scrape_store(store):
    page = 1
    all_products = []

    while True:
        data = fetch_products(store, page)
        products = data.get("products", [])

        if not products:
            break

        for p in products:
            item = {
                "store": store,
                "title": p.get("title"),
                "handle": p.get("handle"),
                "price": p["variants"][0]["price"] if p.get("variants") else None,
                "image": p["images"][0]["src"] if p.get("images") else None
            }
            all_products.append(item)

        print(f"{store} - page {page} done")
        page += 1
    
    return all_products

def scrape_all_store():
    all_data = []

    for store in stores:
        print(f"Scraping {store}...")
        data = scrape_store(store)
        all_data.extend(data)
    
    return all_data

client = pymongo.MongoClient("mongodb+srv://tuancopywriter_db_user:toilaai123@30daysofpython.aa0nav9.mongodb.net/?appName=30DaysOfPython")
db = client["shopify"]
collection = db["products"]

def save_to_db(products):
    if products:
        collection.insert_many(products)

def export_csv(products):
    if not products:
        print("No data")
        return 
    
    with open("shopify_product.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    
    print("CSV saved")

if __name__ == "__main__":
    data = scrape_all_store()
    save_to_db(data)
    export_csv(data)
    print("Save at:", os.getcwd())
    print(len(data))

