from database_config import db_session, engine
from sqlalchemy.orm import sessionmaker
from models import *

Session = sessionmaker(bind=engine)
session = Session()

# class Register_Repository:
#     def register(user):
#         db_session.add(user)
#         db_session.commit()
#         return True



# class User_Repository:
#     def create_user(user):
#         db_session.add(user)
#         db_session.commit()

class device_master_Repository:
    def device_master(data):
        print(data.ecn)
        result=session.query(device_master).filter(device_master.ecn==data.ecn).first()
        if not result:
            db_session.add(data)
            db_session.commit()
            return data.deviceid
        else:
            print(result.deviceid)
            print("Already Exist")
            return result.deviceid

    def authDevice(deviceid):
        result = session.query(device_master).filter(device_master.deviceid == deviceid).first()

        if not result:
            print("Sending False")
            return False
        else:
            print(result.ecn)
            print("Sending True")
            return True

    def get_name(id):
        from_name = session.query(device_master).filter(device_master.ecn == id).first()
        return from_name.name

class attendance_master_Repository:
    def attendance_master(att_data):
        print("Inside att master repository")
        res=attendance_master_Repository.checkIfExist(att_data.ecn,att_data.date,att_data.action)
        # print("ecn=====>",att_data.ecn)
        if(res):
            result = session.query(device_master).filter(device_master.ecn == att_data.ecn).first()
            print("action=====>", att_data.action)
            db_session.add(att_data)
            db_session.commit()
            print("Inside repositiry")
            return result.name
        else:
            result = session.query(device_master).filter(device_master.ecn == att_data.ecn).first()
            return result.name
        # return data1.

    def checkIfExist(ecn,date,action):
        result = session.query(attendance_master).filter(attendance_master.ecn == ecn,attendance_master.date==date,attendance_master.action=="intime").first()
        if not result or action=="outtime":
            print("Not Present")
            return True
        else:
            print("Attendance Already Marked=====>>",result.ecn, result.date,result.time)
            return False

    def checkIfExistConfig(deviceID,date):
        print("DATE Auth=====>",date,deviceID)
        result = session.query(attendance_master).filter(attendance_master.deviceid == deviceID,attendance_master.date==date,attendance_master.action=="intime").first()
        if not result:
            #if else..
            print("Not Present")
            return True
        else:
            print("Attendance Already Marked=====>>",result.ecn, result.date,result.time)
            return False

    def getallData(id):
        result = session.query(attendance_master).filter(attendance_master.ecn == id)
        return result


class notification_master_Repository:
    def saveMsg(data):
        db_session.add(data)
        db_session.commit()

    def getMsgs(id):
        result = session.query(notification_master).filter(notification_master.to_ecn == id)
        to_name = session.query(device_master).filter(device_master.ecn == id).first()

        return [result,to_name.name]

