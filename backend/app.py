from flask import Flask, jsonify
from flask_cors import CORS

from config.app_config import APP_PORT

app = Flask(__name__)
CORS(app)


@app.route('/api/message')
def get_message():
    return jsonify({'message': 'Hello from Flask backend!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)
