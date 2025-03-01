from sqlalchemy.orm import Session
from datetime import datetime

from omop_cdm_graphql.models import Base, Person, Observation, ConditionOccurrence
from omop_cdm_graphql.database import engine, get_db


Base.metadata.create_all(engine)


# Function to populate the database with more records
def populate_db():
    db: Session = next(get_db())

    # Additional Persons
    persons = [
        Person(
            person_id=1, gender_concept_id=8507, birth_datetime=datetime(1990, 1, 1)
        ),
        Person(
            person_id=2, gender_concept_id=8532, birth_datetime=datetime(1985, 5, 15)
        ),
        Person(
            person_id=3, gender_concept_id=8507, birth_datetime=datetime(1978, 3, 22)
        ),  # Male
        Person(
            person_id=4, gender_concept_id=8532, birth_datetime=datetime(1995, 7, 10)
        ),  # Female
        Person(
            person_id=5, gender_concept_id=8507, birth_datetime=datetime(1982, 11, 30)
        ),  # Male
        Person(
            person_id=6, gender_concept_id=8532, birth_datetime=datetime(2000, 4, 15)
        ),  # Female
    ]

    # Additional Observations
    observations = [
        Observation(
            observation_id=1,
            person_id=1,
            observation_concept_id=123,
            observation_date=datetime(2023, 1, 1),
        ),
        Observation(
            observation_id=2,
            person_id=2,
            observation_concept_id=124,
            observation_date=datetime(2023, 3, 15),
        ),
        Observation(
            observation_id=3,
            person_id=3,
            observation_concept_id=125,
            observation_date=datetime(2022, 12, 10),
        ),
        Observation(
            observation_id=4,
            person_id=4,
            observation_concept_id=126,
            observation_date=datetime(2023, 5, 20),
        ),
        Observation(
            observation_id=5,
            person_id=5,
            observation_concept_id=127,
            observation_date=datetime(2023, 1, 25),
        ),
        Observation(
            observation_id=6,
            person_id=6,
            observation_concept_id=128,
            observation_date=datetime(2023, 6, 1),
        ),
        Observation(
            observation_id=7,
            person_id=1,
            observation_concept_id=129,
            observation_date=datetime(2023, 7, 10),
        ),  # Second obs for person 1
    ]

    # Additional Condition Occurrences
    conditions = [
        ConditionOccurrence(
            condition_occurrence_id=1,
            person_id=1,
            condition_concept_id=456,
            condition_start_date=datetime(2023, 2, 1),
        ),
        ConditionOccurrence(
            condition_occurrence_id=2,
            person_id=2,
            condition_concept_id=457,
            condition_start_date=datetime(2023, 4, 1),
        ),
        ConditionOccurrence(
            condition_occurrence_id=3,
            person_id=3,
            condition_concept_id=458,
            condition_start_date=datetime(2022, 11, 15),
        ),
        ConditionOccurrence(
            condition_occurrence_id=4,
            person_id=4,
            condition_concept_id=459,
            condition_start_date=datetime(2023, 6, 5),
        ),
        ConditionOccurrence(
            condition_occurrence_id=5,
            person_id=5,
            condition_concept_id=460,
            condition_start_date=datetime(2023, 2, 10),
        ),
        ConditionOccurrence(
            condition_occurrence_id=6,
            person_id=6,
            condition_concept_id=461,
            condition_start_date=datetime(2023, 7, 15),
        ),
        ConditionOccurrence(
            condition_occurrence_id=7,
            person_id=1,
            condition_concept_id=462,
            condition_start_date=datetime(2023, 8, 20),
        ),  # Second condition for person 1
    ]
    # Add to the session and commit
    db.add_all(persons + observations + conditions)
    db.commit()
    print("Database populated with records!")


def main() -> None:
    # Ensure tables exist
    Base.metadata.create_all(engine)
    populate_db()


# Run the population script
if __name__ == "__main__":
    main()
