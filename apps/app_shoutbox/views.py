from flask import flash, redirect, url_for, render_template

from apps.app_shoutbox import app, db
from apps.app_shoutbox.models import Message
from apps.app_shoutbox.forms import HelloForm


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        new_message = Message(body=body, name=name)
        db.session.add(new_message)
        db.session.commit()
        flash('你的留言已经发送到世界！')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=messages)
