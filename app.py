from flask import Flask
from flask_smorest import Api
from extension import db
from recipes.recipe_api import blp as RecipesBlueprint
from mood.mood_api import blp as MoodBlueprint
from children_info.children_api import blp as ChildBlueprint
from meals.meal_api import blp as MealBlueprint
import config
from flask_cors import CORS
import os
from schemas.common import ErrorSchema

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    api = Api(app)
    
    components = api.spec.components
    
    if "Error" not in components.schemas:
        components.schema("Error", schema=ErrorSchema)

    if "DEFAULT_ERROR" not in components.responses:
        components.response(
            "DEFAULT_ERROR",
            {
                "description": "Default error response",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Error"}
                    }
                },
            },
        )

    # ---- Global tags (these are the groups you’ll see in Swagger UI)
    api.spec.tag({"name": "recipes", "description": "Recipe Recommander API"})
    api.spec.tag({"name": "mood", "description": "Children Emotion API"})
    api.spec.tag({"name": "children", "description": "Children Info Management API"})
    api.spec.tag({"name": "meal", "description": "Children Meal Management API"})

    api.register_blueprint(RecipesBlueprint)
    api.register_blueprint(MealBlueprint)
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
