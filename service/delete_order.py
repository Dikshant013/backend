from models import session, Order
from flask import jsonify

def deleteOrder(order_id):
    try:
        # Find the order by its ID
        order = session.query(Order).filter_by(id=order_id).first()

        if not order:
            return jsonify({"error": f"Order with id {order_id} not found."}), 404

        # Delete the order
        session.delete(order)
        session.commit()

        return jsonify({"message": f"Order with id {order_id} deleted successfully."}), 200

    except Exception as e:
        session.rollback()  # Roll back in case of an error
        return jsonify({"error": str(e)}), 500
