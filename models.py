from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Dataset1(Base):
	__tablename__ = 'dataset1'
	id = Column(Integer, primary_key=True, index=True)
	studytime = Column(Integer,nullable=False)
	activities = Column(Integer,nullable=False)
	freetime = Column(Integer,nullable=False)
	internet = Column(Integer,nullable=False)
	health = Column(Integer,nullable=False)
	absences = Column(Integer,nullable=False)
	G3 = Column(String(5),nullable=False)