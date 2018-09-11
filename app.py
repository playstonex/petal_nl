from flask import Flask
from flask import jsonify
from polyglot.detect import Detector

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world!'


@app.route('/detect/<text>')
def detect(text):
    result = {'result':False}
    try:
        detector = Detector(text)
        result = {'result':True, 'text':text,'language': detector.language.name, 'code':detector.language.code}
    except Exception as e:
        print(e)
    finally:
        pass

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)