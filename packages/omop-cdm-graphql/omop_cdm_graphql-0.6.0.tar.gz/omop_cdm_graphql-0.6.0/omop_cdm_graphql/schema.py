import strawberry

from datetime import datetime
from functools import lru_cache
from sqlalchemy.orm import Session
from typing import List, Optional

from omop_cdm_graphql.database import get_db
from omop_cdm_graphql.models import (
    Person as PersonModel,
    Observation as ObservationModel,
    ConditionOccurrence as ConditionModel,
)


@strawberry.type
class Observation:
    observation_id: int
    observation_concept_id: int
    observation_date: str


@strawberry.type
class ConditionOccurrence:
    condition_occurrence_id: int
    condition_concept_id: int
    condition_start_date: str


@strawberry.type
class Person:
    person_id: int
    gender_concept_id: int
    birth_datetime: str
    observations: List[Observation]
    conditions: List[ConditionOccurrence]

@strawberry.type
class Query:
    @strawberry.field
    @lru_cache(maxsize=128)
    def person(self, person_id: int) -> Optional[Person]:
        db: Session = next(get_db())
        db_person = db.query(PersonModel).filter(PersonModel.person_id == person_id).first()
        if not db_person:
            return None
        return Person(
            person_id=db_person.person_id,
            gender_concept_id=db_person.gender_concept_id,
            birth_datetime=db_person.birth_datetime.isoformat(),
            observations=[
                Observation(
                    observation_id=o.observation_id,
                    observation_concept_id=o.observation_concept_id,
                    observation_date=o.observation_date.isoformat()
                ) for o in db_person.observations
            ],
            conditions=[
                ConditionOccurrence(
                    condition_occurrence_id=c.condition_occurrence_id,
                    condition_concept_id=c.condition_concept_id,
                    condition_start_date=c.condition_start_date.isoformat()
                ) for c in db_person.conditions
            ]
        )

    @strawberry.field
    @lru_cache(maxsize=128)
    def all_persons(self) -> List[Person]:
        db: Session = next(get_db())
        db_persons = db.query(PersonModel).all()
        return [
            Person(
                person_id=p.person_id,
                gender_concept_id=p.gender_concept_id,
                birth_datetime=p.birth_datetime.isoformat(),
                observations=[
                    Observation(
                        observation_id=o.observation_id,
                        observation_concept_id=o.observation_concept_id,
                        observation_date=o.observation_date.isoformat()
                    ) for o in p.observations
                ],
                conditions=[
                    ConditionOccurrence(
                        condition_occurrence_id=c.condition_occurrence_id,
                        condition_concept_id=c.condition_concept_id,
                        condition_start_date=c.condition_start_date.isoformat()
                    ) for c in p.conditions
                ]
            ) for p in db_persons
        ]

    @strawberry.field
    @lru_cache(maxsize=128)
    def persons_by_gender(self, gender_concept_id: int) -> List[Person]:
        db: Session = next(get_db())
        db_persons = db.query(PersonModel).filter(PersonModel.gender_concept_id == gender_concept_id).all()
        return [
            Person(
                person_id=p.person_id,
                gender_concept_id=p.gender_concept_id,
                birth_datetime=p.birth_datetime.isoformat(),
                observations=[
                    Observation(
                        observation_id=o.observation_id,
                        observation_concept_id=o.observation_concept_id,
                        observation_date=o.observation_date.isoformat()
                    ) for o in p.observations
                ],
                conditions=[
                    ConditionOccurrence(
                        condition_occurrence_id=c.condition_occurrence_id,
                        condition_concept_id=c.condition_concept_id,
                        condition_start_date=c.condition_start_date.isoformat()
                    ) for c in p.conditions
                ]
            ) for p in db_persons
        ]

    @strawberry.field
    @lru_cache(maxsize=128)
    def recent_observations(self, after_date: str) -> List[Observation]:
        db: Session = next(get_db())
        date_filter = datetime.fromisoformat(after_date)
        db_observations = db.query(ObservationModel).filter(ObservationModel.observation_date > date_filter).all()
        return [
            Observation(
                observation_id=o.observation_id,
                observation_concept_id=o.observation_concept_id,
                observation_date=o.observation_date.isoformat()
            ) for o in db_observations
        ]

    @strawberry.field
    @lru_cache(maxsize=128)
    def persons_with_condition(self, condition_concept_id: int) -> List[Person]:
        db: Session = next(get_db())
        # db_persons = db.query(PersonModel).join(ConditionOccurrence).filter(ConditionOccurrence.condition_concept_id == condition_concept_id).all()
        db_persons = db.query(Person).join(Person.conditions).filter(ConditionOccurrence.condition_concept_id == condition_concept_id).all()
        return [
            Person(
                person_id=p.person_id,
                gender_concept_id=p.gender_concept_id,
                birth_datetime=p.birth_datetime.isoformat(),
                observations=[
                    Observation(
                        observation_id=o.observation_id,
                        observation_concept_id=o.observation_concept_id,
                        observation_date=o.observation_date.isoformat()
                    ) for o in p.observations
                ],
                conditions=[
                    ConditionOccurrence(
                        condition_occurrence_id=c.condition_occurrence_id,
                        condition_concept_id=c.condition_concept_id,
                        condition_start_date=c.condition_start_date.isoformat()
                    ) for c in p.conditions
                ]
            ) for p in db_persons
        ]

schema = strawberry.Schema(query=Query)
