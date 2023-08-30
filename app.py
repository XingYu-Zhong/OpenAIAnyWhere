
from flask import Flask, request
import requests
import json


with open('config.json', 'r') as config_file:
    config = json.load(config_file)
import os
os.environ['http_proxy'] = f'http://{config["proxy_ip"]}:{config["proxy_port"]}'
os.environ['https_proxy'] = f'http://{config["proxy_ip"]}:{config["proxy_port"]}'
app = Flask(__name__)


TARGET_URL = config["target_url"]


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    resp = requests.request(
        method=request.method,
        url=f"{TARGET_URL}/{path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    return resp.content


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config["flask_port"])
