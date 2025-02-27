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

import glob
import os
from contextlib import suppress
from datetime import datetime, timezone
from typing import Dict, List, Optional

from rich.console import Console

from data_diff import TableSegment, connect, connect_to_table, diff_tables
from data_diff.databases import Database
from dcs_sdk.sdk.config.config_loader import Comparison, SourceTargetConnection
from dcs_sdk.sdk.utils.serializer import serialize_table_schema
from dcs_sdk.sdk.utils.table import create_table_schema_row_count, differ_rows
from dcs_sdk.sdk.utils.themes import theme_1
from dcs_sdk.sdk.utils.utils import (
    analyze_diff_rows,
    calculate_column_differences,
    duck_db_load_csv_to_table,
    find_identical_columns,
    generate_table_name,
    obfuscate_sensitive_data,
)


class DBTableDiffer:
    def __init__(self, config: Comparison):
        self.config = config
        self.console = Console(record=True)
        self.created_at = datetime.now(tz=timezone.utc)
        self.algorithm = "hashdiff"
        self.table1 = None
        self.table2 = None
        self.diff_iter = None
        self.response = {}
        self.source_file_path = self.config.source.filepath
        self.target_file_path = self.config.target.filepath
        self.limit = 100
        self.source_db: Database = None
        self.target_db: Database = None
        self.similarity = self.config.similarity
        if self.similarity:
            from dcs_sdk.sdk.utils.similarity_score.cosine_similarity_provider import (
                CosineSimilarityProvider,
            )
            from dcs_sdk.sdk.utils.similarity_score.jaccard_provider import (
                JaccardSimilarityProvider,
            )
            from dcs_sdk.sdk.utils.similarity_score.levenshtein_distance_provider import (
                LevenshteinDistanceProvider,
            )

            self.similarity_providers = {
                "jaccard": JaccardSimilarityProvider,
                "levenshtein": LevenshteinDistanceProvider,
                "cosine": CosineSimilarityProvider,
            }

    def create_dataset_dict(
        self,
        config: SourceTargetConnection,
        table: TableSegment,
        db_name: str,
        file_path: str,
        database_type: str,
    ) -> Dict:
        schema_list = [serialize_table_schema(v) for v in table.get_schema().values()]
        schema_list.sort(key=lambda x: x["column_name"].upper())

        return {
            "id": config.id,
            "name": config.name,
            "workspace": config.workspace,
            "database_type": database_type,
            "table_name": table.table_path[0],
            "schema": table.database.default_schema,
            "database": db_name,
            "primary_keys": list(table.key_columns),
            "file_path": file_path,
            "files": [] if file_path is None else [generate_table_name(csv, False) for csv in glob.glob(file_path)],
            "row_count": table.count(),
            "columns": schema_list,
            "exclusive_pk_cnt": 0,
            "duplicate_pk_cnt": 0,
            "null_pk_cnt": 0,
        }

    def connect_to_db_table(
        self,
        config: SourceTargetConnection,
        is_source: bool,
    ) -> TableSegment:
        if is_source:
            primary_keys = self.config.primary_keys_source
            columns = self.config.source_columns
            where = self.config.source_filter
        else:
            primary_keys = self.config.primary_keys_target
            columns = self.config.target_columns
            where = self.config.target_filter

        return connect_to_table(
            {
                "driver": config.driver,
                "host": config.host,
                "port": config.port,
                "http_path": config.http_path,
                "access_token": config.access_token,
                "user": config.username,
                "password": config.password,
                "database": config.database,
                "schema": config.schema_name,
                "filepath": config.filepath,
                "warehouse": config.warehouse,
                "role": config.role,
                "catalog": config.catalog,
                "account": config.account,
                "odbc_driver": config.odbc_driver,
                "server": config.server,
            },
            config.table,
            tuple(primary_keys),
            extra_columns=tuple(columns),
            where=where,
        )

    def connect_to_db(self, config: SourceTargetConnection, is_source: bool):
        if is_source:
            self.source_db: Database = connect(
                {
                    "driver": config.driver,
                    "host": config.host,
                    "port": config.port,
                    "http_path": config.http_path,
                    "access_token": config.access_token,
                    "user": config.username,
                    "password": config.password,
                    "database": config.database,
                    "warehouse": config.warehouse,
                    "schema": config.schema_name,
                    "role": config.role,
                    "catalog": config.catalog,
                    "account": config.account,
                    "odbc_driver": config.odbc_driver,
                    "server": config.server,
                }
            )
        else:
            self.target_db: Database = connect(
                {
                    "driver": config.driver,
                    "host": config.host,
                    "port": config.port,
                    "http_path": config.http_path,
                    "access_token": config.access_token,
                    "user": config.username,
                    "password": config.password,
                    "database": config.database,
                    "warehouse": config.warehouse,
                    "schema": config.schema_name,
                    "role": config.role,
                    "catalog": config.catalog,
                    "account": config.account,
                    "odbc_driver": config.odbc_driver,
                    "server": config.server,
                }
            )

    def process_duckdb(self, is_source: bool):
        if is_source:
            filepath = self.config.source.filepath
        else:
            filepath = self.config.target.filepath
        if filepath is None:
            raise ValueError("File path is required for file")
        if filepath.endswith(".csv"):
            if not duck_db_load_csv_to_table(self.config, filepath, is_source):
                raise ValueError(f"Error in loading CSV, for the {'source' if is_source else 'target'}")

    def get_stats(
        self,
        source_row_count: int,
        target_row_count: int,
        schema_1_list: List,
        schema_2_list: List,
    ) -> Dict:
        try:
            stats = self.diff_iter.get_stats_dict()
            stats.update(
                {
                    "table_a_row_count": source_row_count,
                    "table_b_row_count": target_row_count,
                    "diff_pks": (stats["exclusive_A"] + stats["exclusive_B"]) / target_row_count,
                    "identical_columns": find_identical_columns(schema_1_list, schema_2_list),
                }
            )
        except:
            stats = {
                "table_a_row_count": source_row_count,
                "table_b_row_count": target_row_count,
                "identical_columns": find_identical_columns(schema_1_list, schema_2_list),
            }
        return stats

    def _prepare_source_table(self) -> Optional[str]:
        view_name = None
        if self.config.source_query is not None:
            self._process_database_as_schema(
                driver=self.config.source.driver,
                is_source=True,
            )
            self.connect_to_db(
                self.config.source,
                is_source=True,
            )
            view_name = self.source_db.create_view_from_query(
                query=self.config.source_query,
                schema=self.config.temporary_schema_source,
            )
            self.config.source.schema_name = self.config.temporary_schema_source
            self.config.source.table = view_name
        return view_name

    def _prepare_target_table(self) -> Optional[str]:
        view_name = None
        if self.config.target_query is not None:
            self._process_database_as_schema(
                driver=self.config.target.driver,
                is_source=False,
            )
            self.connect_to_db(
                self.config.target,
                is_source=False,
            )
            view_name = self.target_db.create_view_from_query(
                query=self.config.target_query,
                schema=self.config.temporary_schema_target,
            )
            self.config.target.schema_name = self.config.temporary_schema_target
            self.config.target.table = view_name

        return view_name

    def _process_database_as_schema(self, driver: str, is_source: bool):
        if driver in ["mysql"]:
            if is_source:
                self.config.source.database = self.config.temporary_schema_source
            else:
                self.config.target.database = self.config.temporary_schema_target

    def _process_duckdb_connections(self):
        if self.config.source.driver == "duckdb":
            self.process_duckdb(is_source=True)
        if self.config.target.driver == "duckdb":
            self.process_duckdb(is_source=False)

    def diff_tables(
        self,
        is_cli: bool = False,
        show_stats: bool = False,
        save_html: bool = False,
        html_path: str = "dcs_report.html",
    ) -> Dict:

        self._process_duckdb_connections()
        view_name_source = self._prepare_source_table()
        view_name_target = self._prepare_target_table()

        self.table1 = self.connect_to_db_table(self.config.source, is_source=True)
        self.table2 = self.connect_to_db_table(self.config.target, is_source=False)

        db1_name = self.config.source.database or self.config.source.catalog or "source"
        db2_name = self.config.target.database or self.config.target.catalog or "target"

        columns_order_wise_src = self.config.primary_keys_source + self.config.source_columns
        columns_order_wise_target = self.config.primary_keys_target + self.config.target_columns

        self.diff_iter = diff_tables(self.table1, self.table2, algorithm=self.algorithm)

        source_dataset = self.create_dataset_dict(
            self.config.source,
            self.table1,
            db1_name,
            self.source_file_path,
            "file" if self.config.source.driver == "duckdb" else self.config.source.driver,
        )
        target_dataset = self.create_dataset_dict(
            self.config.target,
            self.table2,
            db2_name,
            self.target_file_path,
            "file" if self.config.target.driver == "duckdb" else self.config.target.driver,
        )

        columns_mappings = [
            {"source_column": src, "target_column": trg}
            for src, trg in zip(columns_order_wise_src, columns_order_wise_target)
        ]

        stats = self.get_stats(
            source_dataset["row_count"],
            target_dataset["row_count"],
            source_dataset["columns"],
            target_dataset["columns"],
        )

        columns_with_unmatched_data_type, columns_not_compared = calculate_column_differences(
            source_dataset["columns"], target_dataset["columns"], columns_mappings
        )
        stats.update(
            {
                "columns_with_unmatched_data_type": columns_with_unmatched_data_type,
                "columns_not_compared": columns_not_compared,
            }
        )
        try:
            source_dataset["exclusive_pk_cnt"] = stats["exclusive_A"]
            target_dataset["exclusive_pk_cnt"] = stats["exclusive_B"]
        except:
            ...
        finished_at = datetime.now(tz=timezone.utc)

        self.response = {
            "source_dataset": source_dataset,
            "target_dataset": target_dataset,
            "stats": stats,
            "columns_mappings": columns_mappings,
            "meta": {
                "created_at": self.created_at.isoformat(),
                "seconds": finished_at.timestamp() - self.created_at.timestamp(),
                "finished_at": finished_at.isoformat(),
                "status": "done",
            },
        }

        table = differ_rows(self.diff_iter, self.response, self.limit)

        if is_cli:
            create_table_schema_row_count(self.response, table, self.console)
            if save_html:
                self.console.save_html(html_path, theme=theme_1, clear=True)

        self.cleanup_duckdb()
        self.config.source.filepath = self.source_file_path
        self.config.target.filepath = self.target_file_path
        if self.config.source.driver == "duckdb":
            self.config.source.driver = "file"
        if self.config.target.driver == "duckdb":
            self.config.target.driver = "file"
        rows = analyze_diff_rows(self.response["diff_rows"], [self.response["source_dataset"]["primary_keys"][0]])
        src_duplicates_pks = len(rows.get("duplicate_pk_values_source", []))
        trg_duplicates_pks = len(rows.get("duplicate_pk_values_target", []))
        self.response["source_dataset"]["duplicate_pk_cnt"] = src_duplicates_pks
        self.response["target_dataset"]["duplicate_pk_cnt"] = trg_duplicates_pks

        if show_stats:
            self.print_stats()

        self.process_diff_rows(rows)
        self.drop_view_and_close_connection(view_name_source, view_name_target)
        return self.response

    def drop_view_and_close_connection(self, view_name_source, view_name_target):

        def safe_close(db_connection):
            if db_connection:
                with suppress(Exception):
                    db_connection.close()

        safe_close(self.table1.database)
        safe_close(self.table2.database)

        if self.source_db:
            self.source_db.drop_view_from_db(
                view_name=view_name_source,
                schema=self.config.temporary_schema_source,
            )
        if self.target_db:
            self.target_db.drop_view_from_db(
                view_name=view_name_target,
                schema=self.config.temporary_schema_target,
            )

        safe_close(self.source_db)
        safe_close(self.target_db)

    def cleanup_duckdb(self):
        for db_config in (self.config.source, self.config.target):
            if db_config.driver == "duckdb":
                try:
                    (self.table1 if db_config == self.config.source else self.table2).database.close()
                    os.remove(db_config.filepath)
                except:
                    pass

    def process_diff_rows(self, rows):
        src_duplicates_pks = self.response["source_dataset"]["duplicate_pk_cnt"]
        trg_duplicates_pks = self.response["target_dataset"]["duplicate_pk_cnt"]
        self.response["source_dataset"]["duplicate_pk_cnt"] = src_duplicates_pks
        self.response["target_dataset"]["duplicate_pk_cnt"] = trg_duplicates_pks
        self.response["source_dataset"]["pk_cnt"] = (
            self.response["source_dataset"]["row_count"]
            - src_duplicates_pks
            - len(rows.get("null_pk_values_source", []))
        )
        self.response["target_dataset"]["pk_cnt"] = (
            self.response["target_dataset"]["row_count"]
            - trg_duplicates_pks
            - len(rows.get("null_pk_values_target", []))
        )
        self.response.pop("diff_rows", None)
        self.response.update(rows)
        self.response["stats"].update(
            {
                "diff_rows": (len(self.response["records_with_differences"]) // 2)
                / self.response["source_dataset"]["row_count"],
                "total_diff_rows_count": len(self.response["records_with_differences"]) // 2,
                "total_duplicate_rows_count": (src_duplicates_pks + trg_duplicates_pks),
            }
        )
        self.response["exclusive_pk_values_target"] = self.slice_rows(
            self.response["exclusive_pk_values_target"], 0, self.limit
        )
        self.response["exclusive_pk_values_source"] = self.slice_rows(
            self.response["exclusive_pk_values_source"], 0, self.limit
        )
        self.response["null_pk_values_target"] = self.slice_rows(self.response["null_pk_values_target"], 0, self.limit)
        self.response["null_pk_values_source"] = self.slice_rows(self.response["null_pk_values_source"], 0, self.limit)
        self.response["duplicate_pk_values_target"] = self.slice_rows(
            self.response["duplicate_pk_values_target"], 0, self.limit
        )
        self.response["duplicate_pk_values_source"] = self.slice_rows(
            self.response["duplicate_pk_values_source"], 0, self.limit
        )
        self.response["records_with_differences"] = self.slice_rows(
            self.response["records_with_differences"], 0, self.limit * 2
        )

        if self.similarity:
            provider_class = self.similarity_providers.get(self.similarity.similarity_method.lower())
            if provider_class:
                provider = provider_class()
                fields = self.config.source_columns
                self.response["records_with_differences"] = provider.add_text_similarity(
                    data=self.response["records_with_differences"],
                    key=self.response["source_dataset"]["primary_keys"][0],
                    fields=fields,
                    similarity=self.similarity,
                )
            else:
                raise ValueError(f"Unknown similarity method: {self.similarity.similarity_method}")

        self.response.get("stats", {}).pop("stats", None)
        self.response.get("stats", {}).pop("rows_A", None)
        self.response.get("stats", {}).pop("rows_B", None)

    def print_stats(self):
        try:
            stats_str, stats = self.diff_iter.get_stats_string()
            stats.update(
                {
                    "diff_pks": (stats["exclusive_A"] + stats["exclusive_B"])
                    / self.response["target_dataset"]["row_count"],
                }
            )
            self.response["stats"].update(stats)
            self.response["source_dataset"]["exclusive_pk_cnt"] = stats.get("exclusive_A", 0)
            self.response["target_dataset"]["exclusive_pk_cnt"] = stats.get("exclusive_B", 0)
            src_duplicates_pks = self.response["source_dataset"]["duplicate_pk_cnt"]
            trg_duplicates_pks = self.response["target_dataset"]["duplicate_pk_cnt"]
            stats_str += f"{src_duplicates_pks} duplicate {'row' if src_duplicates_pks <= 1 else 'rows'} in source\n"
            stats_str += f"{trg_duplicates_pks} duplicate {'row' if trg_duplicates_pks <= 1 else 'rows'} in target\n"
            print(stats_str)
        except:
            ...

    def slice_rows(self, rows, start, end):
        return rows[start:end]


def diff_db_tables(
    config: Comparison,
    is_cli: bool = False,
    show_stats: bool = False,
    save_html: bool = False,
    html_path: str = "dcs_report.html",
) -> Dict:
    differ = DBTableDiffer(config)
    response = differ.diff_tables(is_cli, show_stats, save_html, html_path)
    response["comparison_name"] = config.comparison_name
    configuration = config.model_dump()
    del configuration["source"]["id"]
    del configuration["target"]["id"]
    configuration["source"]["schema_name"] = response["source_dataset"]["schema"]
    configuration["target"]["schema_name"] = response["target_dataset"]["schema"]
    response["configuration"] = configuration
    if is_cli:
        response["configuration"]["source"] = obfuscate_sensitive_data(response["configuration"]["source"])
        response["configuration"]["target"] = obfuscate_sensitive_data(response["configuration"]["target"])
    return response
