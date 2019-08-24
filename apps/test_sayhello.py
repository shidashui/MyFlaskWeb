import unittest

from flask import abort

from app_shoutbox import app, db
from app_shoutbox.commands import forge
from app_shoutbox.models import Message


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

    #测试请求
    def test_404_page(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('404 Error', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    def test_500_page(self):
        @app.route('/500')
        def internal_server_error_for_test():
            abort(500)

        response = self.client.get('/500')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn('500 Error', data)
        self.assertIn('Go Back', data)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('留言板', data)

    def test_create_message(self):
        response = self.client.post('/', data=dict(
            name='test_shui',
            body='hello, this is a test'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('你的留言已经发送到世界！', data)
        self.assertIn('hello, this is a test', data)

    def test_form_validation(self):
        response = self.client.post('/',data=dict(
            name=' ',
            body='hello world'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('This field is required.', data)

    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Created 20 fake message', result.output)
        self.assertEqual(Message.query.count(), 50)

    def test_forge_command_with_count(self):
        result = self.runner.invoke(forge, ['--count', '50'])
        self.assertIn('Created 50 fake message', result.output)
        self.assertEqual(Message.query.count(), 50)

if __name__ == '__main__':
    unittest.main()