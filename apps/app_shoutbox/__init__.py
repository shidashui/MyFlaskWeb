from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True #去除模板上的空格
app.jinja_env.lstrip_blocks = True #同上

#初始化
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
toolbar = DebugToolbarExtension(app)

"""
因为这些模块也需要从构造文件中导入程序实例，
所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
"""
from app_shoutbox import views, commands