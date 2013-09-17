from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.markdown import Markdown

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"battlestar"}
app.config["SECRET_KEY"] = "kalashinikov"

db = MongoEngine(app)
md = Markdown(app)

def register_blueprints(app):
    from views import posts
    from admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)
app.debug=True

if __name__ == '__main__':
    app.run()


