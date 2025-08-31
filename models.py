from extension import db
from datetime import date


class DietaryGuidelines(db.Model):
    __tablename__ = 'dietary_guidelines'

    guideline_id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(50), nullable=False)
    age_group = db.Column(db.String(50), nullable=False)
    servings_veg_legumes_beans = db.Column(db.Float, nullable=True)
    servings_fruit = db.Column(db.Float, nullable=True)
    servings_grain = db.Column(db.Float, nullable=True)
    servings_meat_fish_eggs_nuts_seeds = db.Column(db.Float, nullable=True)
    servings_milk_yoghurt_cheese = db.Column(db.Float, nullable=True)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "guideline_id": self.guideline_id,
            "gender": self.gender,
            "age_group": self.age_group,
            "serving_veg_legumes_beans": self.servings_veg_legumes_beans,
            "servings_fruit": self.servings_fruit,
            "servings_grain": self.servings_grain,
            "servings_meat_fish_eggs_nuts_seeds": self.servings_meat_fish_eggs_nuts_seeds,
            "servings_milk_yoghurt_cheese": self.servings_milk_yoghurt_cheese,
            "min_age": self.min_age,
            "max_age": self.max_age,
        }

# class Ingredient(db.Model):
#     __tablename__ = 'ingredient'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     category = db.Column(db.String, nullable=True)

# class Recipe(db.Model):
#     __tablename__ = 'recipes'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     description = db.Column(db.Text, nullable=True)

#     # relationship to recipe_ingredient
#     ingredients = db.relationship('RecipeIngredient', back_populates='recipe')

# class RecipeIngredient(db.Model):
#     __tablename__ = 'recipe_ingredient'

#     id = db.Column(db.Integer, primary_key=True)
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
#     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
#     quantity = db.Column(db.String, nullable=True)

#     recipe = db.relationship('Recipe', back_populates='ingredients')
#     ingredient = db.relationship('Ingredient')



class Child:
    def __init__(self, name, dateOfBirth, gender, heightCm=None, weightKg=None):
        self.id = None
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.heightCm = heightCm
        self.weightKg = weightKg

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dateOfBirth": self.dateOfBirth.isoformat(),
            "gender": self.gender,
            "heightCm": self.heightCm,
            "weightKg": self.weightKg,
        }
