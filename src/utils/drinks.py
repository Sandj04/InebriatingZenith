import pathlib
import datetime
import yaml

from typing import Any

# TODO Add logging to module.


class DrinkCategory:
    name: str
    icon_path: str
    drinks: list["Drink"]

    def __init__(self, name: str, icon_path: str) -> None:
        self.name = name
        self.icon_path = icon_path
        self.drinks = []

    def add_drink(self, drink: "Drink") -> None:
        drink._change_category(self)
        self.drinks.append(drink)

    def __repr__(self) -> str:
        return f"DrinkCategory(name: {self.name}, icon_path: {self.icon_path}, drinks: [{len(self.drinks)} drinks...])"


class Drink:
    name: str
    __category: DrinkCategory | None
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

    def _change_category(self, category: DrinkCategory) -> None:
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
    def category(self) -> DrinkCategory | None:
        return self.__category


def import_drinkslist(filepath: pathlib.Path) -> list[DrinkCategory]:
    """Imports the drink data from a .yaml file.
    Assumes that the .yaml file is valid.
    """  # TODO Maybe add safety measures? Or easy debugging?
    data: dict[str, dict[str, Any]]
    with open(filepath, "r") as drinks_file:
        data = yaml.full_load(drinks_file)

    categories: dict[str, DrinkCategory] = dict()
    for cat_name, cat_data in data["categories"].items():
        categories[cat_name] = DrinkCategory(cat_name, cat_data["icon"])

    for drink_name, drink_data in data["drinks"].items():
        cur_drink = Drink(
            drink_name,
            drink_data["description"],
            int(drink_data["price"] * 100),
            datetime.datetime.strptime(drink_data["unlocks_at"], "%Y-%m-%d %H:%M")
            if "unlocks_at" in drink_data
            else None,
        )

        # Add drink to category
        # Assumes the category exists.
        categories[drink_data["category"]].add_drink(cur_drink)

    return list(categories.values())


if __name__ == "__main__":
    data = import_drinkslist(pathlib.Path("./drinks.yaml"))
    for cat in data:
        print(cat)
        for dr in cat.drinks:
            print(f" - {dr}")
