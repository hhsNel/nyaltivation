from game.loc import Loc

class Item:
    def __init__(self, id: str, name: Loc) -> None:
        self.id = id
        self.name = name

class ItemManager:
    def __init__(self) -> None:
        self.item_table: dict[str, Item] = {}

    def register_item(self, it: Item) -> None:
        self.item_table[it.id] = it

    def item_exists(self, item_id: str) -> bool:
        return item_id in self.item_table.keys()

    def get_item(self, item_id: str) -> Item:
        return self.item_table[item_id]

