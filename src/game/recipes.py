from enum import Enum, auto
from dataclasses import dataclass

class RecipeStepType(Enum):
    GET_ITEM = auto()
    BOIL = auto()
    STIR = auto()

class RecipeStep:
    def __init__(self, type: RecipeStepType, arg: any = None) -> None:
        self.type = type
        self.arg = arg

    def __or__(self, other):
        return RecipeChain((self,)) | other

    def incorrect(self, other):
        if self.type != other.type:
            return True
        elif self.type == RecipeStepType.GET_ITEM:
            return self.arg != other.arg
        elif self.type == RecipeStepType.BOIL or self.type == RecipeStepType.STIR:
            own_time: int = self.arg
            other_time: int = other.arg
            if(other_time > own_time * 1.25):
                return True
            if(other_time < own_time * 0.75):
                return True
        return False

    def __repr__(self):
        return f"{self.type}({repr(self.arg)})"

class RecipeChain:
    def __init__(self, steps: tuple[RecipeStep, ...]) -> None:
        self.steps = steps

    def __or__(self, other):
        if isinstance(other, RecipeStep):
            return RecipeChain(self.steps + (other,))
        elif isinstance(other, RecipeChain):
            return RecipeChain(self.steps + other.steps)
        elif isinstance(other, RecipeFinish):
            Recipe.register_recipe(Recipe(other.recipe_id, self.steps))
        elif isinstance(other, RecipeGetSteps):
            return Recipe("", self.steps)
        else:
            raise NotImplemented

class RecipeFinish:
    def __init__(self, recipe_id: str) -> None:
        self.recipe_id = recipe_id

class RecipeGetSteps: pass

recipe_table = {}

class Recipe:
    def __init__(self, recipe_id: str, steps: RecipeChain) -> None:
        self.id = recipe_id
        self.steps = steps

    @staticmethod
    def get_item(item_id: str) -> RecipeStep:
        return RecipeStep(RecipeStepType.GET_ITEM, item_id)

    @staticmethod
    def boil(seconds: int) -> RecipeStep:
        return RecipeStep(RecipeStepType.BOIL, seconds)

    @staticmethod
    def stir(seconds: int) -> RecipeStep:
        return RecipeStep(RecipeStepType.STIR, seconds)

    @staticmethod
    def finish(recipe_id: str) -> RecipeFinish:
        return RecipeFinish(recipe_id)

    @staticmethod
    def get_steps() -> RecipeGetSteps:
        return RecipeGetSteps()

    @staticmethod
    def register_recipe(recipe) -> None:
        recipe_table[recipe.id] = recipe

    @staticmethod
    def try_steps(tried) -> str | None:
        for rec in recipe_table.values():
            if len(tried.steps) != len(rec.steps):
                continue
            if any(r.incorrect(t) for r, t in zip(rec.steps, tried.steps)):
                continue
            return rec.id

        return None

