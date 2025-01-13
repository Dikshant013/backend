from flask import jsonify, request
from models import session
from service.create_order_request import CreateOrderRequest

def createOrder():
    try:
        # Instantiate the request object
        create_order_request = CreateOrderRequest(request.json)

        # Validate the input data
        if not create_order_request.validate():
            return jsonify({"error": "Invalid input. Ensure customer_name, customer_email, line_items, and tax_rate are provided correctly."}), 400

        # Create the order object using the request class
        new_order = create_order_request.create_order()

        print("Order req")

        # Add the new order to the session
        session.add(new_order)
        session.commit()

        # Return the response
        return jsonify({
            "id": new_order.id,
            "customer_name": new_order.customer_name,
            "customer_email": new_order.customer_email,
            "status": new_order.status.name,
            "line_items": new_order.line_items,
            "tax_rate": new_order.tax_rate,
            "total_before_tax": new_order.total_before_tax,
            "tax_amount": new_order.tax_amount,
            "total_after_tax": new_order.total_after_tax,
            "created_at": new_order.created_at,
            "updated_at": new_order.updated_at
        }), 200

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": str(e)}), 500
