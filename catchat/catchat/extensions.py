from flask_login import LoginManager
from flask_moment import Moment
from flask_oauthlib.client import OAuth
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
socketio = SocketIO()
oauth = OAuth()


@login_manager.user_loader
def load_user(user_id):
    from catchat.models import User
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'