import os
import pathlib
import sys
import yaml

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from omop_cdm_graphql.file_utils import check_infile_status
from omop_cdm_graphql import constants

current_working_directory = os.getcwd()
config_file = os.path.join(current_working_directory, "config.yaml")
check_infile_status(config_file)

print(f"Will load contents of config file '{config_file}'")
config = yaml.safe_load(pathlib.Path(config_file).read_text())


database_file = config.get("database_file", None)
if not database_file:
    database_file = constants.DEFAULT_DATABASE_FILE
    print(
        f"Database file not specified in configuration file '{config_file}' - setting default '{database_file}'"
    )

DATABASE_URL = f"sqlite:///{database_file}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables (run once)
metadata.create_all(engine)
