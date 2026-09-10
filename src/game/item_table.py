from item import Item
from loc import Loc

item_table: dict[str, Item] = {}

def register_item(it: Item) -> None:
    item_table[it.id] = it

register_item(Item("sa-cicada", Loc(en="Spring-Autumn Cicada", nya="Meow-Purr Cicada")))

