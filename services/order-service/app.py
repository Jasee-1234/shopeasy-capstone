from flask import Flask, jsonify, request
import boto3
import os
import uuid
import time

app = Flask(__name__)

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "shopeasy-transactions")
dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1"))


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/orders", methods=["POST"])
def create_order():
    body = request.get_json(force=True, silent=True) or {}
    order = {
        "transaction_id": str(uuid.uuid4()),
        "product_id": str(body.get("product_id", "")),
        "quantity": str(body.get("quantity", 1)),
        "created_at": str(int(time.time())),
    }
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=order)
    return jsonify(order=order), 201


@app.route("/")
def root():
    return jsonify(service="order-service", message="ShopEasy order API"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
