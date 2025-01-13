from models import session, Order, OrderStatus
from flask import jsonify

def updateOrderStatus(order_id, new_status):
    try:
        # Find the order by its ID
        order = session.query(Order).filter_by(id=order_id).first()

        if not order:
            return jsonify({"error": f"Order with id {order_id} not found."}), 404

        # Check if the new status is a valid OrderStatus enum value
        if new_status not in OrderStatus.__members__:
            return jsonify({"error": f"Invalid status: {new_status}. Valid statuses are: {list(OrderStatus.__members__.keys())}"}), 400

        # Update the order status
        order.status = OrderStatus[new_status]

        # Commit the changes to the database
        session.commit()

        return jsonify({"message": "Order status updated successfully", "order_id": order.id, "new_status": order.status.value}), 200

    except Exception as e:
        session.rollback()  # In case of an error, roll back the changes
        return jsonify({"error": str(e)}), 500
