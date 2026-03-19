from flask import Flask, jsonify
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://tuancopywriter_db_user:toilaai123@30daysofpython.aa0nav9.mongodb.net/?appName=30DaysOfPython")
db = client["shopify"]
collection = db["products"]

@app.route("/products")
def get_products():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)