
from sqlalchemy import *
from database_config import Base




class device_master(Base):
    __tablename__ = 'device_masters'
    id = Column(Integer, primary_key=True,autoincrement=True)
    deviceid = Column(String(50), unique=True)
    ecn = Column(String(50), unique=True)
    name=Column(String(50))
    datetime = Column(String(50))

    # email = Column(String(120), unique=True)

    def __init__(self, ecn = None,datetime=None,deviceid=None,name=None):
        self.ecn = ecn
        self.datetime = datetime
        self.deviceid=deviceid
        self.name=name
        # self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


class attendance_master(Base):
    __tablename__ = 'attendance_captured'
    id = Column(Integer, primary_key=True,autoincrement=True)
    ecn = Column(String(50))
    deviceid = Column(String(50))
    location = Column(String(50))
    date = Column(String(50))
    time = Column(String(50))
    action = Column(String(50))
    comments = Column(String(200))


    # email = Column(String(120), unique=True)

    def __init__(self, ecn = None,date=None,time=None,deviceid=None,location=None,action=None,comments=None):
        self.ecn = ecn
        self.date = date
        self.deviceid=deviceid
        self.time=time
        self.location= location
        self.action = action
        self.comments = comments
        # self.email = email

    def __repr__(self):
        return '<User %r>' % (self.date)


class notification_master(Base):
    __tablename__ = 'notification_master'
    id = Column(Integer, primary_key=True,autoincrement=True)
    from_ecn = Column(String(50))
    to_ecn = Column(String(50))

    date = Column(String(50))
    time = Column(String(50))

    msg = Column(String(200))


    # email = Column(String(120), unique=True)

    def __init__(self, from_ecn = None,to_ecn=None,date=None,time=None,msg=None):
        self.from_ecn = from_ecn
        self.to_ecn = to_ecn
        self.date=date
        self.time=time
        self.time= time
        self.msg = msg
        # self.comments = comments
        # self.email = email

    def __repr__(self):
        return '<User %r>' % (self.date)