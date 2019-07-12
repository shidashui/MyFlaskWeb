from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from blog.extensions import mail



#异步发送
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_async_mail(subject, to, html):
    app = current_app._get_current_object()  #获取被代理的真实对象
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app,message])
    thr.start()
    return thr


def send_mail(subject, to , html):
    pass

def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True)+'#comments'
    send_mail(subject='新评论', to=current_app.config['BLUELOG_ADMIN_EMAIL'],
              html='<p>关于文章<i>%s</i>的评论，点击下面链接查看：</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">不要回复。</small></p>'%(post.title,post_url,post_url))

def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True)+'#comments'
    send_mail(subject='新回复',to=comment.email,
              html='<p>关于文章<i>%s</i>的新回复，点击下面链接查看：</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">不用回复。</small></p>'%(comment.post.title, post_url,post_url))