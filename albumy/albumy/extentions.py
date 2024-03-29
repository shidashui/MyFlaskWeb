from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
dropzone = Dropzone()
csrf = CSRFProtect()
avatars = Avatars()
whooshee = Whooshee()  #全文搜索


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
# login_manager.login_message = '请登录'
login_manager.login_message_category = 'warning'

#对话不新鲜跳转的端点
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message = u'为了保护你的账户安全，请重新登录。'
login_manager.needs_refresh_message_category = 'warning'


#匿名用户的权限管理
class Guest(AnonymousUserMixin):
    @property
    def is_admin(selfs):
        return False

    def can(self, permission_name):
        return False

login_manager.anonymous_user = Guest