import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from .models import Category, Post, Comment
from .models import Admin
from .extensions import db


fake = Faker('zh_CN')

def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Blog',
        blog_sub_title="No, I'm the real thing.",
        name='shui',
        about='你好，我是codershui，一名学过心理学的程序猿',
        password='123456'
    )
    db.session.add(admin)
    db.session.commit()

def fake_categories(count=10):
    category = Category(name=fake.word())
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=5000):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1,Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        #未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
        #管理员评论
        comment = Comment(
            author='shui',
            email='164635470@qq.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1,Post.query.count()))
        )
        db.session.add(comment)
    #回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1,Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()