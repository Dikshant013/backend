from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum as PyEnum

# Define the base for declarative models
Base = declarative_base()

# Define the OrderStatus Enum
class OrderStatus(PyEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

# Define the Order model
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    line_items = Column(JSON, nullable=False)
    tax_rate = Column(Float, nullable=False)
    total_before_tax = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    total_after_tax = Column(Float, nullable=False)

    def __init__(self, customer_name, customer_email, status, line_items, tax_rate, total_before_tax, tax_amount, total_after_tax):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.status = status
        self.line_items = line_items
        self.tax_rate = tax_rate
        self.total_before_tax = total_before_tax
        self.tax_amount = tax_amount
        self.total_after_tax = total_after_tax

        # Calculate totals based on line_items and tax_rate
        self.calculate_totals()

    def calculate_totals(self):
        """Calculates total_before_tax, tax_amount, and total_after_tax based on line_items and tax_rate."""
        total_before_tax = sum(item['total_price'] for item in self.line_items)
        self.tax_amount = total_before_tax * self.tax_rate
        self.total_before_tax = total_before_tax
        self.total_after_tax = total_before_tax + self.tax_amount

# Create an SQLite engine for an in-memory database
engine = create_engine('sqlite:///orders.db', echo=True)  # This will create a file-based SQLite DB

# Create all tables in the in-memory database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()