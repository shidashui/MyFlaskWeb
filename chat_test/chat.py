#!/bin/env python
from chat_test.app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
