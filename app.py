from flask import Flask
from flask import jsonify
from flask import request
import fasttext

import rgs

app = Flask(__name__)

model = fasttext.load_model('lid.176.bin')


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
    print('---------------------  Verify ------------------------')
    json = request.get_json()
    # print(request.value)
    print(json)
    text = json['text']

    result = rgs.isMarch(text)
    if result == False:
        return jsonify({'result': result})
    else:
        return jsonify({'result':  True})


@app.route('/detect', methods=['POST'])
def detect():

    json = request.get_json()
    text = json['text']
    print('---------------- TEXT ----------')
    print(text)
    result = {'result': False}
    try:
        res = model.predict(text, k=1)
        print('---------- DETECT RESULT ------------')
        print(res)
        lc = res[0][0]
        if lc.startswith('__label__'):
            lc = lc.strip('__label__')
        print(lc)
        fixCode = lc
        if languageCodes.get(lc):
            fixCode = languageCodes[lc]

        result = {'result': True, 'text': text,
                  'language': lc, 'code': fixCode}
    except Exception as e:
        print(e)
    finally:
        pass

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
