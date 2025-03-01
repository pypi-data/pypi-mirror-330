from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from omop_cdm_graphql.database import metadata

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=metadata)


class Person(Base):
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True, index=True)
    gender_concept_id = Column(Integer)
    birth_datetime = Column(DateTime)
    observations = relationship("Observation", back_populates="person")
    conditions = relationship("ConditionOccurrence", back_populates="person")


class Observation(Base):
    __tablename__ = "observation"
    observation_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    observation_concept_id = Column(Integer)
    observation_date = Column(DateTime)
    person = relationship("Person", back_populates="observations")


class ConditionOccurrence(Base):
    __tablename__ = "condition_occurrence"
    condition_occurrence_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    condition_concept_id = Column(Integer)
    condition_start_date = Column(DateTime)
    person = relationship("Person", back_populates="conditions")
