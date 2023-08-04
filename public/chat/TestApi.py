from flask import Flask, request, jsonify
import conf

app = Flask(__name__)

@app.route('/query/message', methods=['POST'])
def verify_address():
    data = request.get_json()
    challenge = data.get('challenge')
    return jsonify({'challenge': challenge})

if __name__ == "__main__":
    ngrok_url =  conf.NGROK_URL# 替换成你的ngrok公网地址
    app.run(host='0.0.0.0', port=5000)