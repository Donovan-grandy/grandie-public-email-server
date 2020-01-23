from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    grade = Column(String)
    county = Column(String)
    state = Column(String)
    zipcode = Column(Integer)
    classcode = Column(String)
    city = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Teacher(name={self.firstname + self.lastname}, email={self.email}, classcode={self.classcode})>"


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    studentfirstname = Column(String)
    studentlastname = Column(String)
    day_time_1_day = Column(String)
    day_time_2_day = Column(String)
    day_time_3_day =Column(String)
    day_time_1_time = Column(String)
    day_time_2_time = Column(String)
    day_time_3_time =Column(String)
    grade = Column(String)
    county = Column(String)
    state = Column(String)
    zipcode = Column(Integer)
    classcode = Column(String)
    city = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Parent(name={self.studentfirstname + self.studentlastname}, email={self.email}, classcode={self.classcode})>"




class InitiatorContact(Base):
    __tablename__ = 'initiatorContacts'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    initiator_type = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Parent(name={self.studentfirstname + self.studentlastname}, email={self.email}, classcode={self.classcode})>"