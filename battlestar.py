from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"battlestar"}
app.config["SECRET_KEY"] = "kalashinikov"

db = MongoEngine(app)

def register_blueprints(app):
    from views import posts
    from bridge import bridge
    app.register_blueprint(posts)
    app.register_blueprint(bridge)

register_blueprints(app)
app.debug=True

if __name__ == '__main__':
    app.run()


