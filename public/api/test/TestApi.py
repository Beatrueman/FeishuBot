from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/query/message', methods=['POST'])
def verify_address():
    data = request.get_json()
    challenge = data.get('challenge')
    return jsonify({'challenge': challenge})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)