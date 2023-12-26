""" Functions for managing products in the database.
/db/products.py

"""

from src.db.schemas import Product, Category
from src.utils.products import import_products
from sqlalchemy.orm import Session as DBSession
from datetime import datetime

from src.utils.config import Config


# Functions used for managing categories.
def add_category(db_session: DBSession, name: str, icon_path: str) -> Category:
    """Add a category to the database."""
    category = Category(name=name, icon_path=icon_path)
    db_session.add(category)
    db_session.commit()
    return category


def remove_category(db_session: DBSession, category_id: int) -> None:
    """Remove a category from the database."""
    category = db_session.query(Category).filter(Category.id == category_id).first()
    db_session.delete(category)
    db_session.commit()
    return


def get_category_by_id(db_session: DBSession, category_id: int) -> Category:
    """Get a category by its ID."""
    return db_session.query(Category).filter(Category.id == category_id).first()


# Functions used for managing products.
def add_product(
    db_session: DBSession,
    name: str,
    description: str,
    category_id: int,
    price: int,
    ingredients: str = "",
    unlock_time: datetime | None = None,
) -> Product:
    """Add a product to the database."""
    product = Product(
        name=name,
        description=description,
        category=category_id,
        price=price,
        ingredients=ingredients,
        unlock_time=unlock_time,
    )
    db_session.add(product)
    db_session.commit()
    return product


def remove_product(db_session: DBSession, product_id: int) -> None:
    """Remove a product from the database."""
    product = db_session.query(Product).filter(Product.id == product_id).first()
    db_session.delete(product)
    db_session.commit()
    return


def get_product_by_id(db_session: DBSession, product_id: int) -> Product:
    """Get a product by its ID."""
    return db_session.query(Product).filter(Product.id == product_id).first()


def load_products_from_yaml(db_session: DBSession) -> None:
    """Load products from a yaml file configured in the config."""

    products = import_products(Config.product_config_path) # type: ignore
    for category in products:
        if db_session.query(Category).filter(Category.name == category.name).first():
            category_db: Category = db_session.query(Category).filter(Category.name == category.name).first()
            print(f"Category {category.name} already exists.")
        else:
            category_db = add_category(db_session, category.name, category.icon_path)
        if category_db is None:
            raise ValueError("Category could not be created.")
        for product in category.products:
            if not db_session.query(Product).filter(Product.name == product.name).first():
                add_product(
                    db_session,
                    product.name,
                    product.description,
                    category_db.id,
                    product.price,
                    "\n".join([f"{ingredient}:{amount}" for ingredient, amount in product.ingredients.items()]),
                    product.unlock_time,
                )
            else:
                print(f"Product {product.name} already exists.")


def get_all_products(db_session: DBSession) -> list[Product]:
    """Get all products from the database."""
    return db_session.query(Product).all()