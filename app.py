from flask import Flask, jsonify
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

client = pymongo.MongoClient(MONGO_URI)
db = client["shopify"]
collection = db["products"]

print(MONGO_URI)

@app.route("/products")
def get_products():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)