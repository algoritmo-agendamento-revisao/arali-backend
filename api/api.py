from flask import Flask, request, jsonify
from ambiente.ambiente import Ambiente

app = Flask(__name__)
ambiente = Ambiente()

@app.route('/estudo', methods=['POST'])
def receive_info():
    data = request.json
    response_obj = ambiente.obter_proxima_repeticao(data)
    print(response_obj)
    return jsonify(response_obj)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)