from game.items import Item
from game.db import Database
from game.loc import Language
import typing
from enum import Enum
from game.player_actions.refining import PlayerRefiningState

class PlayerActionType(Enum):
    IDLE = "idle"
    REFINING = "refining"

class Player:
    def __init__(self, uid: int, db: Database) -> None:
        self.uid = uid
        self.db = db
        self.state: PlayerActionType = PlayerActionType.IDLE
        self.refining_data: PlayerRefiningState = PlayerRefiningState(self)

    async def load_all(self) -> None:
        await self.load_inv()
        await self.load_loc()

    async def save_inv(self) -> None:
        await self.db.set_value(self.uid, "inventory", self.inventory)
        
    async def load_inv(self) -> None:
        self.inventory = await self.db.get_value(self.uid, "inventory", typing.cast(dict[str, int], {}))

    async def save_loc(self) -> None:
        await self.db.set_value(self.uid, "loc", self.loc)

    async def load_loc(self) -> None:
        self.loc = await self.db.get_value(self.uid, "loc", Language.EN)

    def get_inventory_item(self, item_id: str) -> int:
        return self.inventory.get(item_id, 0)

    async def change_inventory_item(self, item_id: str, amount: int) -> None:
        qty = self.get_inventory_item(item_id)
        qty += amount
        if(qty != 0):
            self.inventory[item_id] = qty
        else:
            del self.inventory[item_id]
        await self.save_inv()

    async def set_language(self, lang: Language) -> None:
        self.loc = lang
        await self.save_loc()

    def assert_state(self, action: PlayerActionType) -> bool:
        if self.state == PlayerActionType.IDLE:
            self.state = action
            return True
        return self.state == action

    def become_idle(self) -> None:
        self.state = PlayerActionType.IDLE

class PlayerManager:
    def __init__(self, db: Database):
        self.db = db
        self.player_table: dict[int, Player] = {}

    async def get_player(self, uid: int):
        if uid not in self.player_table.keys():
            self.player_table[uid] = Player(uid, self.db)
            await self.player_table[uid].load_all()
        return self.player_table[uid]

