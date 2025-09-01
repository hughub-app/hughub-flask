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

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "ingredient_id": self.ingredient_id,
            "ingredient_name": self.ingredient_name,
            "category": self.category
        }

class Recipe(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(255), nullable=False)
    recipe_type = db.Column(db.String(50), nullable=True)
    cuisine_type = db.Column(db.String(50), nullable=True)
    dietary_preferences = db.Column(db.String(100), nullable=True)
    cooking_steps = db.Column(db.Text, nullable=True)
    servings_veg_legumes_beans = db.Column(db.Numeric(4, 2), nullable=True)
    servings_fruit = db.Column(db.Numeric(4, 2), nullable=True)
    servings_grain = db.Column(db.Numeric(4, 2), nullable=True)
    servings_meat_fish_eggs_nuts_seeds = db.Column(db.Numeric(4, 2), nullable=True)
    servings_milk_yoghurt_cheese = db.Column(db.Numeric(4, 2), nullable=True)

    recipe_ingredients = db.relationship(   
        'RecipeIngredient',
        back_populates='recipe',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "recipe_id": self.recipe_id,
            "recipe_name": self.recipe_name,
            "recipe_type": self.recipe_type,
            "cuisine_type": self.cuisine_type,
            "dietary_preferences": self.dietary_preferences,
            "cooking_steps": self.cooking_steps,
            "servings_veg_legumes_beans": float(self.servings_veg_legumes_beans) if self.servings_veg_legumes_beans is not None else None,
            "servings_fruit": float(self.servings_fruit) if self.servings_fruit is not None else None,
            "servings_grain": float(self.servings_grain) if self.servings_grain is not None else None,
            "servings_meat_fish_eggs_nuts_seeds": float(self.servings_meat_fish_eggs_nuts_seeds) if self.servings_meat_fish_eggs_nuts_seeds is not None else None,
            "servings_milk_yoghurt_cheese": float(self.servings_milk_yoghurt_cheese) if self.servings_milk_yoghurt_cheese is not None else None
        }


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    recipe_ingredient_id = db.Column(db.Integer, primary_key=True)  
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id', ondelete='CASCADE'), nullable=False)
    grams = db.Column(db.Integer, nullable=True) 

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient')

    def to_dict(self):
        return {
            "recipe_ingredient_id": self.recipe_ingredient_id,
            "recipe_id": self.recipe_id,
            "ingredient_id": self.ingredient_id,
            "grams": self.grams,
            "recipe_name": self.recipe.recipe_name if self.recipe else None,
            "ingredient_name": self.ingredient.ingredient_name if self.ingredient else None
        }




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
