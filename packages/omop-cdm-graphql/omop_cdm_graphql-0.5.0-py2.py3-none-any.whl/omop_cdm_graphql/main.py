import os
import pathlib
import uvicorn
import yaml

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from omop_cdm_graphql.schema import schema
from omop_cdm_graphql.file_utils import check_infile_status
from omop_cdm_graphql import constants


current_working_directory = os.getcwd()
config_file = os.path.join(current_working_directory, "config.yaml")

check_infile_status(config_file)

print(f"Will load contents of config file '{config_file}'")
config = yaml.safe_load(pathlib.Path(config_file).read_text())

host = config.get("host", None)
port = config.get("port", None)

if not host:
    host = constants.DEFAULT_HOST
    print(f"Host not specified in configuration file '{config_file}' - setting default '{host}'")
if not port:
    port = constants.DEFAULT_PORT
    print(f"Port not specified in configuration file '{config_file}' - setting default '{port}'")


app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


def main() -> None:
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
