from flask import Flask
from flask_smorest import Api
from extension import db
from recipes.recipe_api import blp as RecipesBlueprint
from mood.mood_api import blp as MoodBlueprint
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    # db.init_app(app)
    api = Api(app)

    api.register_blueprint(RecipesBlueprint)
    api.register_blueprint(MoodBlueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
