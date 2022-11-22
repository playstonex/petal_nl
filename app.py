# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from zhconv import convert
import fasttext
from datetime import datetime

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
    time1 = datetime.now()
    isNormal = not rgs.isMarch(text)
    if isNormal:
        isNormal = rgs.is_normal_text(text=text)
    time2 = datetime.now()
    print('-------------- VERIFY USE TIME -----------')
    print((time2 - time1).microseconds)
    return jsonify({'result': isNormal})

# simplified and traditional convert


@app.route('/chineseconvert', methods=['POST'])
def chineseconvert():

    json = request.get_json()
    text = json['text']
    # to = json['to']
    result = text
    simpleText = convert(text, 'zh-cn')

    if simpleText == text:
        result = convert(text, 'zh-tw')
    else:
        result = simpleText

    print(result)
    return jsonify({'result': result})


@app.route('/chinese', methods=['POST'])
def chinese():

    json = request.get_json()
    text = json['text']
    to = json['to']
    result = text
    # simpleText = convert(text, 'zh-cn')

    if to == 'zh-CN':
        result = convert(text, 'zh-cn')
    else:
        result = convert(text, 'zh-tw')

    print(result)
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

    if len(text) > 100:
        text = text[0:99]

    print('---------------- TEXT ----------')
    print(text)
    result = {'result': False}
    try:
        time1 = datetime.now()
        res = model.predict(text, k=3)
        time2 = datetime.now()
        print('---------- DETECT USE TIME ----------')
        print((time2 - time1).microseconds)

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

        if detectLanguage == 'zh-CN':
            simpleText = convert(text, 'zh-cn')
            if text != simpleText:
                detectLanguage = 'zh-TW'

        result = {'result': True, 'text': text,
                  'language': detectLanguage, 'code': detectLanguage}
    except Exception as e:
        print(e)
    finally:
        pass

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
