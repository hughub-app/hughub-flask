from flask import Flask
from flask_smorest import Api
from extension import db
from recipes.recipe_api import blp as RecipesBlueprint
from mood.mood_api import blp as MoodBlueprint
from children_info.children import blp as ChildBlueprint
import config
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    api = Api(app)

    api.register_blueprint(RecipesBlueprint)
    api.register_blueprint(MoodBlueprint)
    api.register_blueprint(ChildBlueprint)
    app.url_map.strict_slashes = False
    
    frontend_urls = os.getenv("FRONTEND_URL", "http://localhost:8081").split(",")
    CORS(
        app,
        origins=frontend_urls,
        supports_credentials=True
    )

    return app

app = create_app() 

if __name__ == "__main__":
    app.run(debug=True)
