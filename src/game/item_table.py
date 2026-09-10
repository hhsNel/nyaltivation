from game.items import Item, ItemManager
from game.loc import Loc

def setup_item_table(im: ItemManager) -> None:
    im.register_item(Item("sa-cicada", Loc(en="Spring-Autumn Cicada", nya="Meow-Purr Cicada")))
    im.register_item(Item("sa-soup", Loc(en="Spring-Autumn Soup", nya="Meow-Purr Soup")))

