from flask import url_for

from albumy.extentions import db
from albumy.models import Notification


#推送关注提醒
def push_follow_notification(follower, receiver):
    message = '用户<a href="%s">%s</a>关注了你' % (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


#推送评论提醒
def push_comment_notification(photo_id, receiver, page=1):
    message = '<a href="%s#comments">图片</a>有新的评论/回复'%(url_for('main.show_photo', photo_id=photo_id, page=page))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


#推送收藏提醒
def push_collect_notification(collector, photo_id, receiver):
    message = '用户<a href="%s">%s</a>收藏了你的<a href="%s">图片</a>' % \
              (url_for('user.index', username=collector.username), collector.username, url_for('main.show_photo', photo_id=photo_id))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()