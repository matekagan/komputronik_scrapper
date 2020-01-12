from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

database_url = "sqlite:///komputronik.db"
db = create_engine(database_url)
DataModel = declarative_base()
DB_session = sessionmaker(bind=db)
session = DB_session()


class Category(DataModel):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    products = relationship('Product', backref='category')

    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name


class Product(DataModel):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    price = Column(Float(), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id


class PriceChange(DataModel):
    __tablename__ = 'price_change'
    id = Column(Integer, primary_key=True)
    old_price = Column(Float(), nullable=False)
    new_price = Column(Float(), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, product_id, old_price, new_price):
        self.old_price = old_price
        self.new_price = new_price
        self.product_id = product_id


def create_category(category_id, name):
    category = session.query(Category).get(category_id)
    if category is None:
        category = Category(category_id, name)
        session.add(category)


def add_product(name, price, category_id):
    product = Product(name, price, category_id)
    session.add(product)


def update_product_price(product, new_price):
    change = PriceChange(product.id, product.price, new_price)
    product.price = new_price
    session.add(change)


def create_or_update_product(name, price, category_id):
    product = session.query(Product).filter_by(name=name).first()
    if product:
        update_product_price(product, price)
    else:
        add_product(name, price, category_id)
    session.commit()


if __name__ == "__main__":
    DataModel.metadata.create_all(db)
