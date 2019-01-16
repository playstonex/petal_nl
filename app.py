from flask import Flask
from flask import jsonify
from polyglot.detect import Detector

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world!'


languageCodes = {
    "zh": "zh-CN",
    "zh_Hant": "zh-TW",
    "zh_Hans": "zh-CN"
}


@app.route('/detect/<text>')
def detect(text):
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
