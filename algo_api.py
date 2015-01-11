from flask import Flask, url_for
from flask import json
from flask import request

app = Flask(__name__)

wave0 = [];
wave1 = [];
wave2 = [];
wave3 = [];
wave4 = [];
wave5 = [];
wave6 = [];
wave7 = [];
time = [];
attention_native = [];
meditation_native = [];

@app.route('/')
def api_root():
	return 'Welcome'

@app.route('/post_waves', methods = ['POST'])
def api_post_waves():
	data = request.get_json()
	data2 = json.dumps(data)
	data2 = json.loads(data2)
	for d in data2:
		time.append(d[0])
		wave0.append((d[1])['wave0'])
		wave1.append((d[1])['wave1'])
		wave2.append((d[1])['wave2'])
		wave3.append((d[1])['wave3'])
		wave4.append((d[1])['wave4'])
		wave5.append((d[1])['wave5'])
		wave6.append((d[1])['wave6'])
		wave7.append((d[1])['wave7'])
		attention_native.append((d[1])['attention'])
		meditation_native.append((d[1])['meditation'])
	return json.dumps(data)

@app.route('/get_results', methods = ['GET'])
def api_get_results():
	return time

if __name__ == '__main__':
	app.debug = True
	app.run()
