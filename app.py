from flask import Flask
from flask import jsonify
from flask import request
from pyfasttext import FastText

import rgs

app = Flask(__name__)

model = FastText('lid.176.bin')


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
    #print(request.value)
    print(json)
    text = json['text']

    result = rgs.isMarch(text)
    if result == False:
        return jsonify({'result': result})
    else:
        # name =  Guess().language_name(text)
        print('------------ Lan name-----')
        print(name)
        return jsonify({'result': name == 'text'})




@app.route('/detect', methods=['POST'])
def detect():

    json = request.get_json()
    text = json['text']

    result = {'result': False}
    try:
        res = model.predict_proba_single(text, k=1)
        
        lc = res[0][0]
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
