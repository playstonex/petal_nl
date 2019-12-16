# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from hanziconv import HanziConv
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


# simplified and traditional convert
@app.route('/chineseconvert', methods=['POST'])
def chineseconvert():
    json = request.get_json()
    text = json['text']
    to = json['to']
    result = text
    if to == 'zh-CN':
        result = HanziConv.toSimplified(text)
    else:
        result = HanziConv.toTraditional(text)
    return jsonify({'result': result})


@app.route('/detect', methods=['POST'])
def detect():

    json = request.get_json()
    keys = json.keys()
    print(keys)

    text = json['text']
    l1 = ''
    if 'l1' in json:
        l1 = json['l1']
    l2 = ''
    if 'l2' in json:
        l2 = json['l2']

    if languageCodes.get(l1):
        l1 = languageCodes[l1]

    if languageCodes.get(l2):
        l2 = languageCodes[l2]

    print('---------------- TEXT ----------')
    print(text)
    result = {'result': False}
    try:
        res = model.predict(text, k=3)
        print('---------- DETECT RESULT ------------')
        print(res)
        detectLanguage = ''

        dls = []
        for dl in res[0]:
            if dl.startswith('__label__'):
                l = dl[len('__label__'):len(dl)]
                if languageCodes.get(l):
                    l = languageCodes[l]
                dls.append(l)

        for dl in dls:
            if dl == l1:
                detectLanguage = dl
                break

        if detectLanguage == '':
            for dl in dls:
                if dl == l2:
                    detectLanguage = dl
                    break

        if detectLanguage == '':
            detectLanguage = dls[0]

        result = {'result': True, 'text': text,
                  'language': detectLanguage, 'code': detectLanguage}
    except Exception as e:
        print(e)
    finally:
        pass

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
