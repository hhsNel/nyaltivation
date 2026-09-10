from game.recipes import RecipeStep, RecipeChain, Recipe
from enum import Enum
import time

class PlayerRefiningStateAction(Enum):
    IDLE = "idle"
    BOILING = "boiling"
    STIRRING = "stirring"

class PlayerRefiningState:
    def __init__(self, player) -> None:
        self.player = player
        self.recipe = None
        self.action: PlayerRefiningStateAction = PlayerRefiningStateAction.IDLE
        self.time = 0

    def push_step(self, step: RecipeStep) -> None:
        if self.recipe is None:
            self.recipe = step
        else:
            self.recipe = self.recipe | step

    def check_previous(self) -> None:
        if self.action == PlayerRefiningStateAction.BOILING:
            self.push_step(Recipe.boil(int(time.time()) - self.time))
            self.action = PlayerRefiningStateAction.IDLE
        elif self.action == PlayerRefiningStateAction.STIRRING:
            self.push_step(Recipe.stir(int(time.time()) - self.time))
            self.action = PlayerRefiningStateAction.IDLE

    def finish(self) -> Recipe | None:
        self.check_previous()
        if self.recipe is None:
            return None
        rec = self.recipe | Recipe.get_steps()
        self.recipe = None
        return rec

    def stop_action(self) -> None:
        self.check_previous()

    def add_item(self, item_id: str) -> None:
        self.check_previous()
        self.push_step(Recipe.get_item(item_id))

    def boil(self) -> None:
        self.check_previous()
        self.action = PlayerRefiningStateAction.BOILING
        self.time = int(time.time())

    def stir(self) -> None:
        self.check_previous()
        self.action = PlayerRefiningStateAction.STIRRING
        self.time = int(time.time())

