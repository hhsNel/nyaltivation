from recipes import Recipe

Recipe.get_item("sa-cicada") | Recipe.boil(30) | Recipe.stir(15) | Recipe.finish("sa-soup")

