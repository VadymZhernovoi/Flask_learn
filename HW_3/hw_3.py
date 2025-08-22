from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

""" Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти."""

db = 'sqlite:///hw_3.db'
engine = create_engine(db)

""" Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок. """

Session = sessionmaker(bind=engine)

"""
Задача 3: Определите модель продукта Product со следующими типами колонок:
    id: числовой идентификатор
    name: строка (макс. 100 символов)
    price: числовое значение с фиксированной точностью
    in_stock: логическое значение
"""

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    in_stock = Column(Boolean, default=False)
    # Установите связь между таблицами Product и Category с помощью колонки category_id.
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')

"""
Задача 4: Определите связанную модель категории Category со следующими типами колонок:
    id: числовой идентификатор
    name: строка (макс. 100 символов)
    description: строка (макс. 255 символов)
"""

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    products = relationship('Product', back_populates='category')


# потренироваться
Base.metadata.create_all(engine)

with Session() as s:
    pr_1 = Product(name='Product 1', price=24.23, in_stock=True, category_id=2)
    pr_2 = Product(name='Product 2', price=100.01, in_stock=True, category_id=2)
    pr_3 = Product(name='Product 3', price=0.99, in_stock=False, category_id=3)
    pr_4 = Product(name='Product 4', price=1000.03, in_stock=False, category_id=1)
    pr_5 = Product(name='Product 5', price=10.53, in_stock=False, category_id=2)

    ct_1 = Category(name="Computer", description="Computers")
    ct_2 = Category(name="Mobile", description="Mobile devices")
    ct_3 = Category(name="Accessory", description="Accessories")

    s.add(pr_1)
    s.add(pr_2)
    s.add(pr_3)
    s.add(pr_4)
    s.add(pr_5)
    s.add(ct_1)
    s.add(ct_2)
    s.add(ct_3)

    s.commit()

from sqlalchemy import MetaData
metadata = MetaData()
engine = create_engine(db)
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()

print(metadata.tables)

Prod = Base.classes.products
print(Prod)
Cat = Base.classes.categories
print(Cat)

