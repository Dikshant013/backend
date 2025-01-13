from flask import request
from models import OrderStatus, Order
from typing import List, Dict

class CreateOrderRequest:
    def __init__(self, data: Dict):
        self.data = data
        self.customer_name = data.get('customer_name')
        self.customer_email = data.get('customer_email')
        self.line_items = data.get('line_items', [])
        self.tax_rate = data.get('tax_rate', 0)
        self.status = data.get('status', 'PENDING')

    def validate(self) -> bool:
        if not self.customer_name or not self.customer_email or not self.line_items or self.tax_rate is None:
            return False
        
        if not isinstance(self.line_items, list):
            return False
        
        try:
            self.tax_rate = float(self.tax_rate)
        except ValueError:
            return False
        return True

    def calculate_totals(self):
        total_before_tax = sum(item['total_price'] for item in self.line_items)
        tax_amount = total_before_tax * self.tax_rate
        total_after_tax = total_before_tax + tax_amount
        return total_before_tax, tax_amount, total_after_tax

    def create_order(self):
        total_before_tax, tax_amount, total_after_tax = self.calculate_totals()

        # Create a new order
        new_order = Order(
            customer_name=self.customer_name,
            customer_email=self.customer_email,
            status=OrderStatus[self.status],  # Default to PENDING status
            line_items=self.line_items,
            tax_rate=self.tax_rate,
            total_before_tax=total_before_tax,
            tax_amount=tax_amount,
            total_after_tax=total_after_tax
        )
        
        return new_order
