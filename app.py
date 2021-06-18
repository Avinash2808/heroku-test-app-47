from flask import Flask, render_template, Response, request, jsonify
from services import GenerateDeviceID,getallData
import logging

app = Flask(__name__)

@app.route('/')
def hello_world():
    return ("Hello World")


@app.route('/register')
def register_user():
    # return render_template("Registration_del.html")
    return render_template("Registration.html")

@app.route('/gen_deviceId',methods=["POST"])
def gen_DeviceId():
    try:
        data=request.get_json()
        print(data)
        if  data["ecn"]=="" or data["location"]=="" or data["name"]=="":
            return jsonify({"status":"missing Field"})
        else:
            data= GenerateDeviceID(data)
            return jsonify({"data":data})
    except:
        logging.exception("An exception occured=====>>")

@app.route('/landing',methods=["POST","GET"])
def get_landing_data():
    try:
        if not request.args.get("id"):
            return jsonify({"result": "null"})
        else:
            print(request.args.get("id"))
            result=getallData(request.args.get("id"))
            # return{"result":result}
            return render_template("landing.html",data=result)
    except:
        logging.exception("An exception occured=====>>")

if __name__ == '__main__':
    # init_db()
    app.run(debug=True)