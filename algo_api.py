from flask import Flask, url_for
from flask import json
from flask import request

app = Flask(__name__)

delta = [];
high_alpha = [];
high_beta = [];
low_alpha = [];
low_beta = [];
low_gamma = [];
mid_gamma = [];
theta = [];
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
		delta.append((d[1])['wave0'])
		high_alpha.append((d[1])['wave1'])
		high_beta.append((d[1])['wave2'])
		low_alpha.append((d[1])['wave3'])
		low_beta.append((d[1])['wave4'])
		low_gamma.append((d[1])['wave5'])
		mid_gamma.append((d[1])['wave6'])
		theta.append((d[1])['wave7'])
		attention_native.append((d[1])['attention'])
		meditation_native.append((d[1])['meditation'])
	return json.dumps(data)

@app.route('/get_results', methods = ['GET'])
def api_get_results():
	return time

if __name__ == '__main__':
	app.debug = True
	app.run()
