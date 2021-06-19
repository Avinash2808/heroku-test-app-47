# author:Prathamesh Deogharkar
import threading
from database_config import init_db
from detect_face import detectentry
# from delete_face import delete_embedding
import pickle
import os
from services import *
import socket
from flask import Flask, render_template, Response, request, jsonify
from flask_jsglue import JSGlue
import cv2
import numpy as np
from train_model import train_embedding
import logging

app = Flask(__name__)
JSGlue(app)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
path = os.path.dirname(os.path.realpath(__file__))
recognizer = pickle.loads(open(path + "/recognizer.pickle", "rb").read())
le = pickle.loads(open(path + "/le.pickle", "rb").read())
lelock = threading.Lock()
dataLock = threading.Lock()

print("Recognizer============>>",recognizer)
print("Le===================>>",le)

@app.route('/')
def hello_world():
    return ("Hello World")


@app.route('/register')
def register_user():
    # return render_template("Registration_del.html")
    return render_template("Registration.html")

@app.route('/recognize',methods=["POST"])
def recognize_face():
    try:
        data=request.form.getlist("image")
        lowAcc=request.form.get("low_acc")
        comment=request.form.get("comment")
        # print("Location======>>",request.form.get("location"))
        # print("action=======>>",request.form.get("config"))
        print("Date=======>>", request.form.get("location"),request.form.get("deviceID"))
        if(len(data)>0):
            result=detectentry(data,recognizer,le,lelock,int(lowAcc),request.form.get("location"),request.form.get("deviceID"),request.form.get("config"),request.form.get("date"),comment)
            return jsonify({"result": "Done","value":result[0],"name":result[1]})
        else:
            return jsonify({"result":"Error"})
    except:
        print()

@app.route('/detect_face_in',methods=["GET","POST"])
def detect_face_in():
    try:
        if request.method=="GET":
            return render_template("Recognize.html",data="3117TS202106060243")
        else:
            data=request.form.get("deviceID")
            # data1=request.form.get("lastname")
            loc = request.form.get("loc")
            comment = request.form.get("data")
            # data1=request.form.get("lastname")
            print("DeviceID=========>>", data, loc, comment)
            return render_template("Recognize.html",data=data,loc=loc,comment=comment)
    except:
        logging.exception("An exception occured=====>>")

@app.route('/detect_face_out',methods=["GET","POST"])
def detect_face_out():
    try:
        if request.method=="GET":
            return render_template("Recognize_out.html",data="3117TS202106060243")
        else:
            data=request.form.get("deviceID")
            loc=request.form.get("loc")
            comment=request.form.get("data")
            # data1=request.form.get("lastname")
            print("DeviceID=========>>",data,loc,comment)
            return render_template("Recognize_out.html",data=data,loc=loc,comment=comment)
    except:
        logging.exception("An exception occured=====>>")



@app.route('/train',methods=["GET"])
def train():
    return Response(train_embedding(recognizer, le, lelock, dataLock, "/EmployeeDataset"),content_type='text/event-stream')

@app.route('/auth_device',methods=["POST"])
def auth_device():
    try:
        data=request.get_json()
        # print("Data=======>>",data["deviceID"],data["date"])
        if data["deviceID"] != "":
            resp=auth_deviceID(data["deviceID"])
            print("Controler value====>",resp)
            if(resp[0]):
                return jsonify({"data":"true","config":resp[1]})
            else:
                return jsonify({"data": "false","config":resp[1]})
        else:
            return jsonify({"data": "false","config":""})
    except:
        logging.exception("An exception occured=====>>")


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


@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.form.getlist('image')
        ecn = request.form.get('ecn')
        lable = request.form.get('number')
        return jsonify(create_user_dataset(data, lable, ecn))
    except Exception as ex:
        logging.exception("An exception occured=====>>")
        return jsonify({"result": "Error", "status": 500})
    # for a in range(10):
    #     frame = cv2.imdecode(
    #         np.frombuffer(base64.b64decode(data[a].split(',')[1]), dtype=np.uint8),
    #         flags=cv2.IMREAD_COLOR)
    #     cv2.imwrite(str(request.form.get('number')) + '.png', frame)
    #     return jsonify({"result": "Done", "status": 200})

@app.route('/del',methods=["POST"])
def delete():
    print(request.form.get("id"))
    if delete_embedding(request.form.get("id")):
        return Response(train_embedding(recognizer, le, lelock, dataLock, "/Empty"),content_type='text/event-stream')
    else:
        return jsonify({"status":200})

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
@app.route('/send_notification',methods=["POST","GET"])
def send_notification():
    try:
        data_raw=request.get_json()
        if not request.get_json()["to"] or not request.get_json()["from"] or not request.get_json()["msg"]:
            return jsonify({"result": "null"})
        else:
            print(request.get_json())
            data=request.get_json()
            # result=getallData(request.args.get("id"))
            # return{"result":result}
            resp=saveMsg(data)
            return jsonify({"result":resp})
    except:
        logging.exception("An exception occured=====>>")

@app.route('/get_notification',methods=["POST","GET"])
def get_notification():
    try:
        data=request.args.get("id")
        print(data)
        res=getMsgs(data)
        return jsonify({"result":res})
    except:
        logging.exception("An exception occured=====>>")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
