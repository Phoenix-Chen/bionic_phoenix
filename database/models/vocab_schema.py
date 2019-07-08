from sqlalchemy import Column, Integer, String, ForeignKey, Table, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Vocabulary(Base):
    __tablename__ = 'vocabulary'

    id = Column(Integer, Sequence('vocabulary_id_seq'), primary_key=True, autoincrement=True)
    word = Column(String, unique=True)
    correct = Column(Integer, default=0)
