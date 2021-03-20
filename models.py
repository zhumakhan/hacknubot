from sqlalchemy import Column, Integer
# from sqlalchemy.orm import relationship

from database import Base

class Dataset1(Base):
	__tablename__ = 'dataset1'
	id = Column(Integer, primary_key=True, index=True)
	age = Column(Integer,nullable=False)
	traveltime = Column(Integer,nullable=False)
	studytime = Column(Integer,nullable=False)
	failures = Column(Integer,nullable=False)
	activities = Column(Integer,nullable=False)
	higher = Column(Integer,nullable=False)
	internet = Column(Integer,nullable=False)
	romantic = Column(Integer,nullable=False)
	health = Column(Integer,nullable=False)
	absences = Column(Integer,nullable=False)
	G3 = Column(Integer,nullable=False)