# flask_web/app.py

from flask import Flask
from flask import request
from flask import jsonify
import ocrCode
import DeprecatedOCRrun
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def spreadArray(words):
    words = words.split(",")
    sum = ""
    for word in words:
        sum += " " + word 

@app.route("/")
def hello():
    imgFilePath = request.args.get('imgFilePath')
    words = request.args.get('words')
    
    #return words.split(",")[0]
    words = words.split(",")
    results=dict()
    for word in words:
        results.update(DeprecatedOCRrun.runOCR(wordToSearch=word,imgFilePath=imgFilePath) )

    return jsonify(results)
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)