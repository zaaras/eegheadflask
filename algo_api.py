from flask import Flask, url_for
from flask import json
from flask import request

app = Flask(__name__)

@app.route('/')
def api_root():
	return 'Welcome'

@app.route('/post_waves', methods = ['POST'])
def api_post_waves():
	return "JSON Message: " + json.dumps(request.json)

if __name__ == '__main__':
	app.debug = True
	app.run()
