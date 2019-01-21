from flask import Flask
from flask import jsonify
from flask import request
from polyglot.detect import Detector

import rgs

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world!'


languageCodes = {
    "zh": "zh-CN",
    "zh_Hant": "zh-TW",
    "zh_Hans": "zh-CN"
}


@app.route('/verify', methods=['POST'])
def verify():
    json = request.get_json()
    text = json['text']

    result = rgs.isMarch(text)
    return jsonify({'result': result})


@app.route('/detect', methods=['POST'])
def detect():

    json = request.get_json()
    text = json['text']

    result = {'result': False}
    try:
        detector = Detector(text)
        lc = detector.language.code
        fixCode = lc
        if languageCodes.get(lc):
            fixCode = languageCodes[lc]

        result = {'result': True, 'text': text,
                  'language': detector.language.name, 'code': fixCode}
    except Exception as e:
        print(e)
    finally:
        pass

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
