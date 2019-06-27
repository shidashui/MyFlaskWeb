from datetime import datetime
from app_shoutbox import db

#可以考虑后期添加用户或者游客以及邮箱的字段，还有可回复的功能
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    name = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)