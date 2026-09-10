from game.recipes import Recipe, RecipeManager

def setup_recipe_table(rm: RecipeManager) -> None:
    Recipe.get_item("sa-cicada") | Recipe.boil(30) | Recipe.stir(15) | Recipe.finish("sa-soup", rm)

