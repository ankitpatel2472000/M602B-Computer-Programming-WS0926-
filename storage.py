import json
import os

class FavoritesStorage:
    """Handles loading and saving favorite cities to a JSON file."""
    def __init__(self, filename: str = "favorites.json"):
        self.filename = filename

    def load_favorites(self) -> list[str]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    def save_favorite(self, city: str) -> bool:
        city_clean = city.strip().title()
        favorites = set(self.load_favorites())
        if city_clean and city_clean not in favorites:
            favorites.add(city_clean)
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(sorted(list(favorites)), file, indent=4)
            return True
        return False