from models import session, Order
from flask import jsonify

def getOrders():
    try:
        # Query all orders
        orders = session.query(Order).all()

        # Serialize orders to a list of dictionaries
        orders_list = []
        for order in orders:
            orders_list.append({
                "id": order.id,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "status": order.status.value,  # Enum values
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": order.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "line_items": order.line_items,
                "tax_rate": order.tax_rate,
                "total_before_tax": order.total_before_tax,
                "tax_amount": order.tax_amount,
                "total_after_tax": order.total_after_tax
            })

        return jsonify(orders_list), 200
    except Exception as e:
        # In case of any error, return 500 and the error message
        return jsonify({"error": str(e)}), 500
