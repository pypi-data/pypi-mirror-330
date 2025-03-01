import pytest
from strawberry.test import GraphQLTestClient
from omop_cdm_graphql.schema import schema

@pytest.fixture
def client():
    return GraphQLTestClient(schema)

def test_person_query(client):
    query = """
    query {
      person(personId: 1) {
        personId
        genderConceptId
        birthDatetime
        observations {
          observationId
          observationConceptId
          observationDate
        }
        conditions {
          conditionOccurrenceId
          conditionConceptId
          conditionStartDate
        }
      }
    }
    """
    response = client.query(query)
    assert response.errors is None
    assert response.data["person"]["personId"] == 1

def test_all_persons_query(client):
    query = """
    query {
      allPersons {
        personId
        genderConceptId
        birthDatetime
      }
    }
    """
    response = client.query(query)
    assert response.errors is None
    assert len(response.data["allPersons"]) > 0

def test_persons_by_gender_query(client):
    query = """
    query {
      personsByGender(genderConceptId: 8507) {
        personId
        birthDatetime
      }
    }
    """
    response = client.query(query)
    assert response.errors is None
    assert len(response.data["personsByGender"]) > 0

def test_recent_observations_query(client):
    query = """
    query {
      recentObservations(afterDate: "2023-01-01") {
        observationId
        observationConceptId
        observationDate
      }
    }
    """
    response = client.query(query)
    assert response.errors is None
    assert len(response.data["recentObservations"]) > 0

def test_persons_with_condition_query(client):
    query = """
    query {
      personsWithCondition(conditionConceptId: 456) {
        personId
        genderConceptId
        conditions {
          conditionOccurrenceId
          conditionStartDate
        }
        observations {
          observationId
        }
      }
    }
    """
    response = client.query(query)
    assert response.errors is None
    assert len(response.data["personsWithCondition"]) > 0
