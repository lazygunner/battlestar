from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"battlestar"}
app.config["SECRET_KEY"] = "kalashinikov"

db = MongoEngine(app)

def register_blueprints(app):
    from battlestar.views import posts
    app.register_blueprint(posts)

register_blueprints(app)

if __name__ == '__main__':
    app.run()


