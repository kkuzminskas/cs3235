from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# changed
from flask_socketio import SocketIO, emit


# end changed


app = Flask(__name__)
app.config.from_object('config')

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
from app import views



# if __name__ == '__main__':
#     socketio.run(app)
