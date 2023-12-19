import yaml
import pathlib

def check_drinks(file_path: pathlib.Path) -> bool:
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path.absolute()} not found")
    with open(file_path, "r") as drinks_file:
        data = yaml.full_load(drinks_file)
        
        # Category checks
        if not "categories" in data:
            raise KeyError("No categories defined in 'categories' key!")
        categories: list[dict[str, dict[str, str]]] = data["categories"]
        if not isinstance(categories, list):
            raise TypeError("'categories' key must be a list!")
        if not categories:
            raise ValueError("'categories' key must not be empty!")
        for category in categories:
            if not isinstance(category, dict):
                raise TypeError(f"Category name must be a string!")
            if not category:
                raise ValueError("Category name must not be empty!")
            if not "icon" in category:
                raise KeyError(f"No icon defined in category '{category}'!")
            
        

if __name__ == "__main__":
    check_drinks(pathlib.Path("./drinks.yaml"))