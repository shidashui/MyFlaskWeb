import unittest

from app_shoutbox import app, db


class SayHelloTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False, #关闭csrf，方便测试post请求
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        db.create_all()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #测试程序实例是否存在
    def test_app_exist(self):
        self.assertFalse(app is None)

    #配置键TESTING是否为True
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
        