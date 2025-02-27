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

from collections import defaultdict
from typing import Union

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def create_legend():
    legend = Table(show_header=False, box=None)
    legend.add_column(style="bold")
    legend.add_column()
    legend.add_row("Red", "Mismatch", style="red")
    legend.add_row("Cyan", "Match", style="cyan")
    legend.add_row("Yellow", "Duplicate", style="yellow")
    return Panel(legend, title="Info", border_style="cyan bold", width=80)


def create_schema_table(response, console, is_source=True):
    key = "source_dataset" if is_source else "target_dataset"
    columns = response[key]["columns"]
    title = f"Schema: {response[key]['database']}.{response[key]['schema']}.{response[key]['table_name']}"
    mapped_columns = response["columns_mappings"]
    other_columns = response["target_dataset"]["columns"] if is_source else response["source_dataset"]["columns"]

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("#")
    table.add_column("Column Name", style="cyan")
    table.add_column("Data Type", style="magenta")
    table.add_column("Reason", style="red")

    for index, col in enumerate(columns, start=1):
        name = col["column_name"]
        data_type = col["data_type"]
        max_length = col.get("character_maximum_length", None)

        mapped_col = next(
            (
                m["target_column"] if is_source else m["source_column"]
                for m in mapped_columns
                if m["source_column" if is_source else "target_column"] == name
            ),
            None,
        )

        other_col = next((c for c in other_columns if c["column_name"] == (mapped_col or name)), None)

        mismatch_reason = ""
        if other_col:
            if data_type != other_col["data_type"]:
                mismatch_reason = "Data type mismatch"
            elif max_length != other_col.get("character_maximum_length", None):
                mismatch_reason = "Max length mismatch"
        else:
            mismatch_reason = "Exclusive to source" if is_source else "Exclusive to target"

        data_type_with_max_len = f"{data_type} {('('+ str(max_length) + ')') if max_length is not None else ''}"
        if mismatch_reason:
            table.add_row(
                str(index),
                Text(name, style="red"),
                Text(data_type_with_max_len, style="red"),
                mismatch_reason,
            )
        else:
            table.add_row(str(index), name, data_type_with_max_len, Text("-", style="green", justify="left"))
        col["mismatch_reason"] = mismatch_reason
    console.print(table)


def create_table_schema_row_count(response, row_diff_table, console):
    source_dataset = response["source_dataset"]
    target_dataset = response["target_dataset"]

    console.print(create_legend())
    table_row_counts = Table(title="Row Counts", show_header=True, header_style="bold magenta")
    table_row_counts.add_column("")
    table_row_counts.add_column(
        f"{source_dataset['database'] }.{source_dataset['schema']}.{source_dataset['table_name']}",
        style="cyan",
    )
    table_row_counts.add_column(
        f"{target_dataset['database']}.{target_dataset['schema']}.{target_dataset['table_name']}",
        style="yellow",
    )
    table_row_counts.add_row(
        "Row Count",
        str(source_dataset["row_count"]),
        str(target_dataset["row_count"]),
    )
    console.print(table_row_counts)

    create_schema_table(response, console, is_source=True)
    create_schema_table(response, console, is_source=False)

    if row_diff_table is not None:
        console.print(row_diff_table)


def differ_rows(diff_iter, response, limit: int):
    data = []
    table_row_diff = Table(title="Row Difference", show_header=True, header_style="bold magenta")
    for diff in diff_iter:
        sign, rows = diff
        obj = {"meta": {}}
        obj["meta"]["origin"] = "source" if sign == "-" else "target"
        obj["meta"]["sign"] = sign
        for idx, col_ in enumerate(rows):
            obj[response["columns_mappings"][idx]["source_column"]] = col_

        data.append(obj)
    response["diff_rows"] = data
    pk_key_col = response["source_dataset"]["primary_keys"][0]
    if len(data) > 0:
        create_table_diff_rows(table_row_diff, data, pk_key_col, response["columns_mappings"], limit)
    return table_row_diff


def create_table_diff_rows(table, data, primary_keys: Union[str, list[str]], columns_mappings, limit):
    column_mapping_dict = {mapping["source_column"]: mapping["target_column"] for mapping in columns_mappings}

    # Add serial number column
    table.add_column("#")
    table.add_column("Origin")

    for mapping in columns_mappings:
        source_col = mapping["source_column"]
        target_col = mapping["target_column"]
        if source_col == target_col:
            table.add_column(source_col, style="cyan")
        else:
            table.add_column(f"{target_col}/{source_col}", style="cyan")

    if isinstance(primary_keys, str):
        primary_keys = [primary_keys]

    def get_composite_key(row):
        return tuple(row[key] for key in primary_keys)

    records = defaultdict(lambda: defaultdict(list))
    for row in data:
        composite_key = get_composite_key(row)
        origin = row["meta"]["origin"]
        records[composite_key][origin].append(row)

    previous_composite_key = None
    serial_number = 0
    unique_keys_processed = set()
    for row in data:
        composite_key = get_composite_key(row)
        if composite_key not in unique_keys_processed:
            if len(unique_keys_processed) >= limit:
                break
            serial_number += 1
        meta_values = row["meta"]
        row_values = {key: row[key] for key in column_mapping_dict.keys()}

        mismatched_columns = set()
        for origin_records in records[composite_key].values():
            for record in origin_records:
                if record != row and row["meta"]["origin"] == "target":
                    for col in column_mapping_dict.keys():
                        if record[col] != row_values[col]:
                            mismatched_columns.add(col)

        origin = meta_values["origin"]
        duplicate_in_same_origin = len(records[composite_key][origin]) > 1

        formatted_cells = [Text(str(serial_number))]
        for col in meta_values:
            if col != "sign":
                formatted_cells.append(
                    Text(
                        str(meta_values[col]),
                        style=f"{'chartreuse2' if meta_values['origin'] == 'source' else 'cyan3'}",
                    )
                )

        for col in column_mapping_dict.keys():
            cell_value = row_values[col]
            if col in mismatched_columns:
                formatted_cells.append(Text(str(cell_value), style="red bold"))
            else:
                formatted_cells.append(Text(str(cell_value)))

        if duplicate_in_same_origin:
            formatted_cells = [
                (
                    Text(str(cell), style="default")
                    if idx == 0
                    else (
                        Text(
                            str(cell),
                            style=f"{'chartreuse2' if str(cell) == 'source' else 'cyan3'}",
                        )
                        if idx == 1
                        else Text(str(cell), style="yellow bold")
                    )
                )
                for idx, cell in enumerate(formatted_cells)
            ]

        if previous_composite_key is not None and previous_composite_key != composite_key:
            table.add_section()

        table.add_row(*formatted_cells)
        previous_composite_key = composite_key
        unique_keys_processed.add(composite_key)
