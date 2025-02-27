#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import uuid
from typing import List, Literal, Optional, Union

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel


class InvalidUUIDError(ValueError):
    pass


class MissingRequiredFieldError(ValueError):
    pass


class InvalidConnectionTypeError(ValueError):
    pass


class InvalidSimilarityMethodError(ValueError):
    pass


class SourceTargetConnection(BaseModel):
    id: str
    name: str
    workspace: Optional[str] = "default"
    host: Optional[str] = None
    port: Optional[Union[int, str]] = None
    driver: str
    table: Optional[str] = None
    database: Optional[str] = None
    filepath: Optional[str] = None
    catalog: Optional[str] = None
    schema_name: Optional[str] = None
    warehouse: Optional[str] = None
    role: Optional[str] = None
    account: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    http_path: Optional[str] = None
    access_token: Optional[str] = None
    odbc_driver: Optional[str] = None
    server: Optional[str] = None


class SimilarityConfig(BaseModel):
    pre_processing: List[str]
    similarity_method: str
    threshold: float


class Comparison(BaseModel):
    comparison_name: str
    source: SourceTargetConnection
    target: SourceTargetConnection
    source_columns: List[str]
    target_columns: List[str]
    primary_keys_source: List[str]
    primary_keys_target: List[str]
    source_filter: Optional[str] = None
    target_filter: Optional[str] = None
    source_query: Optional[str] = None
    target_query: Optional[str] = None
    temporary_schema_source: Optional[str] = None
    temporary_schema_target: Optional[str] = None
    similarity: Optional[SimilarityConfig] = None


class EnvYamlLoader(yaml.SafeLoader):
    """YAML Loader with `!ENV` constructor."""

    def __init__(self, stream):
        super(EnvYamlLoader, self).__init__(stream)
        self.add_constructor("!ENV", self.env_constructor)

    @classmethod
    def env_constructor(cls, loader, node):
        value = loader.construct_scalar(node)
        env_var = value.strip("${} ")
        return os.environ.get(env_var, "")


class DataDiffConfig:
    DRIVER_MAP = {
        "file": "duckdb",
        "duckdb": "duckdb",
        "postgres": "postgres",
        "postgresql": "postgres",
        "snowflake": "snowflake",
        "trino": "trino",
        "databricks": "databricks",
        "oracle": "oracle",
        "mssql": "mssql",
        "mysql": "mysql",
        "sybase": "sybase",
    }

    def __init__(
        self,
        yaml_file_path: Optional[str] = None,
        yaml_string: Optional[str] = None,
        config_json: Optional[dict] = None,
    ):
        load_dotenv()
        if yaml_file_path:
            self.data = self.read_yaml_file(yaml_file_path)
        elif yaml_string:
            self.data = self.read_yaml_string(yaml_string)
        elif config_json:
            self.data = config_json
        else:
            raise ValueError("No configuration provided")

    @staticmethod
    def read_yaml_file(file_path: str) -> dict:
        with open(file_path, "r") as file:
            return yaml.load(file, Loader=EnvYamlLoader)

    @staticmethod
    def read_yaml_string(yaml_string: str) -> dict:
        return yaml.load(yaml_string, Loader=EnvYamlLoader)

    @staticmethod
    def is_valid_uuid(val: str) -> bool:
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def validate_uuid(self, uuid_str: str, field_name: str) -> None:
        if not self.is_valid_uuid(uuid_str):
            raise InvalidUUIDError(f"{field_name} is not a valid UUID")

    @staticmethod
    def validate_required_field(value: Union[str, None], field_name: str, source_name: str) -> None:
        if value is None:
            raise MissingRequiredFieldError(f"{field_name} is required for datasource {source_name}")

    @staticmethod
    def validate_file_connection(connection: dict) -> None:
        if connection.get("type") == "file" and connection.get("filepath") is None:
            raise MissingRequiredFieldError("file path is required for file connection")

    @staticmethod
    def validate_databricks_connection(connection: dict) -> None:
        if connection.get("type") == "databricks":
            if connection.get("connection", {}).get("http_path") is None:
                raise MissingRequiredFieldError("http_path is required for databricks connection")
            if connection.get("connection", {}).get("access_token") is None:
                raise MissingRequiredFieldError("access_token is required for databricks connection")

    @staticmethod
    def validate_host_or_server(connection: dict) -> None:
        if connection.get("type") == "sybase":
            if not connection.get("connection", {}).get("host") and not connection.get("connection", {}).get("server"):
                raise MissingRequiredFieldError("host or server is required for connection")

    @staticmethod
    def validate_comparison_by_query(
        comparison_data: dict, field_name: Literal["source", "target"], temporary_schema: str | None, database_type: str
    ) -> None:
        if comparison_data.get(field_name, {}).get("query") is not None:
            if comparison_data.get(field_name, {}).get("table") is not None:
                raise ValueError(f"table and query cannot be used together in {field_name} connection")
            if comparison_data.get(field_name, {}).get("filter") is not None:
                raise ValueError(f"filter and query cannot be used together in {field_name} connection")
            if database_type in ["file", "oracle"]:
                return
            if temporary_schema is None:
                raise ValueError("temporary_schema is required for query based comparison")

    @staticmethod
    def validate_similarity_threshold(threshold: float) -> None:
        if threshold is None:
            raise MissingRequiredFieldError("threshold is required for similarity")
        if not 0 <= threshold <= 1:
            raise ValueError("Similarity threshold must be between 0 and 1")
        return threshold

    def get_driver(self, connection: dict) -> str:
        connection_type = connection.get("type")
        if connection_type not in self.DRIVER_MAP:
            raise InvalidConnectionTypeError(f"Invalid connection type: {connection_type}")
        return self.DRIVER_MAP[connection_type]

    def get_similarity_method(self, similarity_method: str) -> str:
        if similarity_method is None:
            raise MissingRequiredFieldError("similarity_method is required for similarity")
        similarity_methods = ["jaccard", "cosine", "levenshtein"]
        if similarity_method not in similarity_methods:
            raise InvalidSimilarityMethodError(f"Invalid similarity method: {similarity_method}")
        return similarity_method

    def get_pre_processing_methods(self, pre_processing: List[str]) -> List[str]:
        if pre_processing is None:
            raise MissingRequiredFieldError("pre_processing is required for similarity")
        pre_processing_methods = ["lower_case", "remove_punctuation", "remove_stop_words", "remove_extra_whitespaces"]
        for method in pre_processing:
            if method not in pre_processing_methods:
                raise ValueError(f"Invalid pre_processing method: {method}")
        return pre_processing

    def create_connection_config(
        self,
        connection: dict,
        comparison_data: dict,
        is_source: bool,
        temporary_schema: str | None,
    ) -> dict:
        self.validate_uuid(connection.get("id"), "Datasource id")
        self.validate_required_field(connection.get("name"), "connection name", source_name=connection.get("name"))
        self.validate_required_field(connection.get("type"), "connection type", source_name=connection.get("name"))
        self.validate_file_connection(connection)
        self.validate_databricks_connection(connection)
        self.validate_host_or_server(connection)
        self.validate_comparison_by_query(
            comparison_data, "source" if is_source else "target", temporary_schema, connection.get("type")
        )

        driver = self.get_driver(connection)

        return {
            "id": connection.get("id"),
            "name": connection.get("name"),
            "workspace": connection.get("workspace", "default"),
            "host": connection.get("connection", {}).get("host", ""),
            "port": connection.get("connection", {}).get("port", None),
            "account": connection.get("connection", {}).get("account"),
            "warehouse": connection.get("connection", {}).get("warehouse"),
            "role": connection.get("connection", {}).get("role"),
            "driver": driver,
            "table": comparison_data.get("source" if is_source else "target", {}).get("table"),
            "database": connection.get("connection", {}).get("database"),
            "catalog": connection.get("connection", {}).get("catalog"),
            "schema_name": connection.get("connection", {}).get("schema"),
            "username": connection.get("connection", {}).get("username"),
            "password": connection.get("connection", {}).get("password"),
            "http_path": connection.get("connection", {}).get("http_path"),
            "access_token": connection.get("connection", {}).get("access_token"),
            "filepath": connection.get("filepath"),
            "odbc_driver": connection.get("connection", {}).get("odbc_driver"),
            "server": connection.get("connection", {}).get("server"),
        }

    def get_data_diff_configs(self) -> List[Comparison]:
        data_sources = {
            ds["name"]: {
                "name": ds.get("name"),
                "id": ds.get("id"),
                "type": ds.get("type"),
                "workspace": ds.get("workspace", "default"),
                "connection": ds.get("connection", {}),
                "filepath": ds.get("file_path"),
                "temporary_schema": ds.get("temporary_schema"),
            }
            for ds in self.data["data_sources"]
        }
        new_structure = []

        for comparison_name, comparison_data in self.data["comparisons"].items():
            source_connection = data_sources[comparison_data["source"]["data_source"]]
            target_connection = data_sources[comparison_data["target"]["data_source"]]

            temporary_schema_source = source_connection.get("temporary_schema")
            temporary_schema_target = target_connection.get("temporary_schema")

            source_to_target = {
                item["source_column"]: item["target_column"] for item in comparison_data.get("columns_mappings", {})
            }

            source_columns = comparison_data.get("columns", [])
            target_columns = [source_to_target.get(col, col) for col in source_columns]

            assert len(source_columns) == len(
                target_columns
            ), "source_columns and target_columns must have the same length"

            primary_keys_source = comparison_data.get("key_columns", [])
            if not primary_keys_source:
                raise MissingRequiredFieldError("key_columns are required for comparison")
            primary_keys_target = [source_to_target.get(pk, pk) for pk in primary_keys_source]

            similarity_data = comparison_data.get("similarity")
            similarity = (
                SimilarityConfig(
                    pre_processing=self.get_pre_processing_methods(similarity_data.get("pre_processing", None)),
                    similarity_method=self.get_similarity_method(similarity_data.get("similarity_method", None)),
                    threshold=self.validate_similarity_threshold(similarity_data.get("threshold", None)),
                )
                if similarity_data
                else None
            )

            new_comparison = {
                "comparison_name": comparison_name,
                "source": self.create_connection_config(
                    source_connection, comparison_data, True, temporary_schema_source
                ),
                "target": self.create_connection_config(
                    target_connection, comparison_data, False, temporary_schema_target
                ),
                "source_columns": source_columns,
                "target_columns": target_columns,
                "primary_keys_source": primary_keys_source,
                "primary_keys_target": primary_keys_target,
                "source_filter": comparison_data.get("source", {}).get("filter", None),
                "target_filter": comparison_data.get("target", {}).get("filter", None),
                "source_query": comparison_data.get("source", {}).get("query", None),
                "target_query": comparison_data.get("target", {}).get("query", None),
                "temporary_schema_source": temporary_schema_source,
                "temporary_schema_target": temporary_schema_target,
                "similarity": similarity,
            }
            new_structure.append(Comparison(**new_comparison))

        return new_structure


def data_diff_config_loader(
    config_path: Optional[str] = None,
    config_yaml: Optional[str] = None,
    config_json: Optional[dict] = None,
) -> List[Comparison]:
    config = DataDiffConfig(
        yaml_file_path=config_path,
        yaml_string=config_yaml,
        config_json=config_json,
    )
    return config.get_data_diff_configs()
