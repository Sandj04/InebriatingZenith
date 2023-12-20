import pathlib
import datetime
import yaml

from typing import Any

# TODO Add logging to module.


class ProductCategory:
    name: str
    icon_path: str
    products: list["Product"]

    def __init__(self, name: str, icon_path: str) -> None:
        self.name = name
        self.icon_path = icon_path
        self.products = []

    def add_product(self, product: "Product") -> None:
        product._change_category(self)
        self.products.append(product)

    def __repr__(self) -> str:
        return f"DrinkCategory(name: {self.name}, icon_path: {self.icon_path}, products: [{len(self.products)} products...])"


class Product:
    name: str
    __category: ProductCategory | None
    description: str
    price: int  # Price represented in hundreds. 125 == 1,25
    __ingredients: dict[str, int]
    unlock_time: datetime.datetime | None

    def __init__(
        self,
        name: str,
        description: str,
        price: int,
        unlock_time: datetime.datetime | None,
    ) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.unlock_time = unlock_time

        self.__category = None
        self.__ingredients = dict()

    def add_ingredient(self, name: str, parts: int) -> None:
        assert name not in self.__ingredients
        self.__ingredients[name] = parts
        return

    def remove_ingredient(self, name: str) -> None:
        # TODO Should this be strict? Add an assert? (J08K, 12-dec-23)
        if name in self.__ingredients:
            self.__ingredients.pop(name)

    def _change_category(self, category: ProductCategory) -> None:
        """Changes the current category of the drink.
        Should only be used by the `DrinkCategory` class.
        """
        self.__category = category

    @property
    def real_price(self) -> float:
        return self.price / 100

    def __repr__(self) -> str:
        return f"Drink(name: {self.name}, desc: {self.description[:20]}, price: {self.real_price}, ingredients: [{len(self.__ingredients)}], unlocks_at: {self.unlock_time})"

    @property
    def ingredients(self) -> dict[str, int]:
        return self.__ingredients.copy()

    @property
    def category(self) -> ProductCategory | None:
        return self.__category


def import_products(filepath: pathlib.Path) -> list[ProductCategory]:
    """Imports the drink data from a .yaml file.
    Assumes that the .yaml file is valid.
    """  # TODO Maybe add safety measures? Or easy debugging?
    data: dict[str, dict[str, Any]]
    with open(filepath, "r") as product_file:
        data = yaml.full_load(product_file)

    categories: dict[str, ProductCategory] = dict()
    for cat_name, cat_data in data["categories"].items():
        categories[cat_name] = ProductCategory(cat_name, cat_data["icon"])

    for product_name, product_data in data["drinks"].items():
        cur_product = Product(
            product_name,
            product_data["description"],
            int(product_data["price"] * 100),
            datetime.datetime.strptime(product_data["unlocks_at"], "%Y-%m-%d %H:%M")
            if "unlocks_at" in product_data
            else None,
        )

        # Add drink to category
        # Assumes the category exists.
        categories[product_data["category"]].add_product(cur_product)

    return list(categories.values())


if __name__ == "__main__":
    data = import_products(pathlib.Path("./drinks.yaml"))
    for cat in data:
        print(cat)
        for dr in cat.products:
            print(f" - {dr}")
