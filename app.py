from service.get_order import getOrders
from service.create_order import createOrder
from service.update_order import updateOrderStatus
from service.delete_order import deleteOrder
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify(message="Welcome to orders!")

@app.route('/orders', methods=['GET'])
def get_orders():
    return  getOrders()

@app.route('/orders', methods=['POST'])
def create_order():
    return createOrder()

@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status_route(order_id):
    data = request.json

    if 'status' not in data:
        return jsonify({"error": "Status field is required."}), 400

    new_status = data['status']
    return updateOrderStatus(order_id, new_status)

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order_route(order_id):
    return deleteOrder(order_id)

if __name__ == '__main__':
    app.run(port=7005, debug=True)
