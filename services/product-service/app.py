from flask import Flask, jsonify
import os

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Garden Hose 20m", "price": 45.99},
    {"id": 2, "name": "Cordless Drill", "price": 129.00},
    {"id": 3, "name": "Paint Roller Set", "price": 18.50},
]


@app.route("/health")
def health():
    # ALB target group health checks hit this endpoint every 30s
    return jsonify(status="ok"), 200


@app.route("/products")
def list_products():
    return jsonify(products=PRODUCTS), 200


@app.route("/")
def root():
    return jsonify(service="product-service", message="ShopEasy product catalog API"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
