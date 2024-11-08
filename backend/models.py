from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()

class OrderStatusEnum(enum.Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    
class Customer(db.Model):
    __tablename__ = 'customers_4'
    
    customer_id = Column(Integer, primary_key=True , autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15))
    address = Column(String(255))

    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
    cart = relationship("Cart", back_populates="customer", uselist=False)

class Shop(db.Model):
    __tablename__ = 'shops_1'
    
    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admins_1.admin_id'), nullable=False)  # References admin ID
    shop_name = Column(String(100), nullable=False)
    shop_address = Column(String(255))
    phone_number = Column(String(15))
    email = Column(String(100))
    owner_name = Column(String(100))

    admin = relationship("Admin", back_populates="shop")  # Reflects the admin relationship
    products = relationship("Product", back_populates="shop")
    orders = relationship("Order", back_populates="shop")

class Admin(db.Model):
    __tablename__ = 'admins_1'
    
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15))

    shop = relationship("Shop", back_populates="admin")  # One-to-one if each admin manages one shop
    products = relationship("Product", back_populates="admin")

class Product(db.Model):
    __tablename__ = 'products_1'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    shop_id = Column(Integer, ForeignKey('shops_1.shop_id'))
    price = Column(DECIMAL(10, 2))
    stock_quantity = Column(Integer)
    admin_id = Column(Integer, ForeignKey('admins_1.admin_id'))
    added_date = Column(DateTime)

    shop = relationship("Shop", back_populates="products")
    admin = relationship("Admin", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("Cart", back_populates="product")
    reviews = relationship("Review", back_populates="product")

class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime)
    total_amount = Column(DECIMAL(10, 2))
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending)
    customer_id = Column(Integer, ForeignKey('customers_4.customer_id'))
    shop_id = Column(Integer, ForeignKey('shops_1.shop_id'))

    customer = relationship("Customer", back_populates="orders")
    shop = relationship("Shop", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    subtotal = Column(DECIMAL(10, 2))
    product_id = Column(Integer, ForeignKey('products_1.product_id'))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

class Cart(db.Model):
    __tablename__ = 'cart'
    
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers_4.customer_id'))
    total_items = Column(Integer)
    total_price = Column(DECIMAL(10, 2))
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey('products_1.product_id'))
    subtotal = Column(DECIMAL(10, 2))

    customer = relationship("Customer", back_populates="cart")
    product = relationship("Product", back_populates="cart_items")

class Review(db.Model):
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers_4.customer_id'))
    product_id = Column(Integer, ForeignKey('products_1.product_id'))
    shop_id = Column(Integer, ForeignKey('shops_1.shop_id'))
    rating = Column(Integer)
    comment = Column(Text)
    review_date = Column(DateTime)

    customer = relationship("Customer", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()