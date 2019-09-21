from run import app
from flask import jsonify


@app.route("/")
def index():
    return jsonify({'message': 'Hello, World!'})


#context = ('server.crt', 'server.key')
#app.run(host='127.0.0.1', port=5000, ssl_context=context, threaded=True, debug=True)
#app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
