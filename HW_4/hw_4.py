"""
Задача 1: Наполнение данными.
    Добавьте в базу данных следующие категории и продукты.
    Добавление категорий: Добавьте в таблицу categories следующие категории:
        Название: "Электроника", Описание: "Гаджеты и устройства."
        Название: "Книги", Описание: "Печатные книги и электронные книги."
        Название: "Одежда", Описание: "Одежда для мужчин и женщин."
    Добавление продуктов: Добавьте в таблицу products следующие продукты,
    убедившись, что каждый продукт связан с соответствующей категорией:
        Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
        Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
        Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
        Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
        Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда
"""
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

db = 'sqlite:///hw_4.db'
engine = create_engine(db) #, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    in_stock = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')

    def __str__(self):
        return f'{self.id=} {self.name=} {self.price=} {self.in_stock=} {self.category_id=}'

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    products = relationship('Product', back_populates='category')

    def __str__(self):
        return f'{self.id=} {self.name=} {self.description=} {self.products=}'

Product.category = relationship("Category", back_populates="products")

Base.metadata.create_all(engine)
#
categories = [
    Category(name='Электроника', description='Гаджеты и устройства.'),
    Category(name='Книги', description='Печатные книги и электронные книги.'),
    Category(name='Одежда', description='Одежда для мужчин и женщин.')
]
products = [
        Product(name='Смартфон', price=299.99, in_stock=True, category_id=1),
        Product(name='Ноутбук', price=499.99, in_stock=True, category_id=1),
        Product(name='Научно-фантастический роман', price=15.99, in_stock=True, category_id=2),
        Product(name='Джинсы', price=40.50, in_stock=True, category_id=3),
        Product(name='Футболка', price=20.00, in_stock=True, category_id=3)
]

with Session() as session:
    session.add_all(categories)
    session.add_all(products)
    session.commit()

    # Задача 2: Чтение данных
    #     Извлеките все записи из таблицы categories.
    #     Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.

    # не по заданию, но чтобы наглядно было, добавлю ещё одну категорию "Спорт" в которой не будет товаров
    session.add(Category(name='Спорт', description='Товары для спорта.'))
    session.commit()

    categories = session.query(Category)
    print("\nСписок всех категорий:")
    for category in categories.all():
        print(f"Категория: {category.name} ({category.description})")
        if category.products:
            print("\tТовары:")
            for product in category.products:
                print(f"\t\t- {product.name}, цена: {product.price:.2f}")
        else:
            print(f"\tВ категории {category.name} товары отсутствуют.")


    # Задача 3: Обновление данных
    #     Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.

    # не по заданию, но чтобы наглядно было, добавлю ещё один 'Смартфон' price=863.01
    session.add(Product(name='Смартфон', price=863.01, in_stock=True, category_id=1))
    session.commit()

    product_name = 'Смартфон'
    price_new = 349.99
    product = session.query(Product).filter(Product.name == product_name).first()
    if product:
        print(f"\nНайден первый товар: {product.name} (цена: {product.price:.2f})")
        price_old = product.price   # для информации
        product.price = price_new   # изменяем цену
        session.commit()            # фиксируем изменение
        # проверяем
        product = session.query(Product).get(product.id)
        print(f"Цена товара: {product.name} изменена (старая цена: {price_old:.2f}, новая цена: {product.price:.2f})")
    else:
        print(f"\nПродукт: {product_name} не найден")

    # Задача 4: Агрегация и группировка
    #     Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.

    # если понимать дословно (там не сказано использовать JOIN), то наверное так:
    total_products = (
            session.query(Product.category_id, func.count(Product.id).label('total_products'))
                            .group_by(Product.category_id)
        )
    print()
    for product in total_products:
        print(f"Категория ID: {product.category_id}, товаров: {product.total_products}")
    # но так без названия категории

    # чтобы увидеть все категории (также у которых нет продуктов) я бы сделал так:
    categories = (
        session.query(Category.name, func.count(Product.id).label('total_products'))
                        .outerjoin(Product)
                        .group_by(Category.name)
    )
    print("\nВсе категории")
    for category in categories:
        print(f"\tКатегория: {category.name}, товаров: {category.total_products}")

    # Задача 5: Группировка с фильтрацией
    #     Отфильтруйте и выведите только те категории, в которых более одного продукта.
    total_products = (
        session.query(Product.category_id, func.count(Product.id).label('total_products'), Category.name.label('category_name'))
        .group_by(Product.category_id)
        .join(Category)
        .having(func.count(Product.id) > 1)
    )
    print("\nКатегории, в которых более одного продукта")
    for product in total_products:
        print(f"\tКатегория: {product.category_name}, товаров: {product.total_products}")


