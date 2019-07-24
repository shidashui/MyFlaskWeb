from flask_mail import Message
from app import mail
...
message = Message(subject='Hello, World!', recipients=['164635470@qq.com'], body='Across the Great Wall we can reach every corner in the world.')
mail.send(message)