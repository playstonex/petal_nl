# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from zhconv import convert, issimp
from fastlid import fastlid
import hanzidentifier
from datetime import datetime

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

    l1 = 'zh' if 'zh' in l1 else l1
    l2 = 'zh' if 'zh' in l2 else l2
    if len(text) > 100:
        text = text[0:99]

    print('---------------- TEXT ----------')
    print(text)
    result = {'result': False}
    try:
        time1 = datetime.now()
        ls = []
        if len(l1) > 0:
            ls.append(l1)
        if len(l2) > 0:
            ls.append(l2)

        if len(ls) > 0:
            fastlid.set_languages = ls
        else:
            fastlid.set_languages = None
        res = fastlid(text, k=3)
        # res = model.predict(text, k=3)
        time2 = datetime.now()
        print('---------- DETECT USE TIME ----------')
        print((time2 - time1).microseconds)

        print('---------- DETECT RESULT ------------')
        print(res)
        detectLanguage = res[0][0] if type(res[0]) is list else res[0]
        if detectLanguage == 'zh':
            detectLanguage = 'zh_CN' if hanzidentifier.is_simplified(
                text) else 'zh_TW'

        result = {'result': True, 'text': text,
                  'language': detectLanguage, 'code': detectLanguage}
    except Exception as e:
        print(e)
    finally:
        pass

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
