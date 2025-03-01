import re
from typing import Any

from pysll.exceptions import (
    ConstellationObjectDoesNotExistException,
    TraversalTooDeepError,
)
from pysll.models import ConstellationFieldParser


def parse_results_from_traversals(objects_info, obj, traversals, field_parser, *, depth: int):
    """Parse out the response for the requested traversals."""

    if depth >= 100:
        raise TraversalTooDeepError

    object_info = objects_info.get(obj.id, {})
    results = []
    for traversal in traversals:
        if "name" not in traversal:
            continue
        field_name = traversal["name"]
        field_value = object_info.get(field_name)
        if "rows" in traversal and field_value is not None:
            if not isinstance(field_value, list):
                raise TypeError(f"Field {field_name} is not an array")

            start_idx = traversal["rows"]["start"] - 1
            end_idx = traversal["rows"]["end"] - 1

            try:
                if start_idx == end_idx:
                    field_value = field_value[start_idx]
                else:
                    field_value = field_value[start_idx : end_idx + 1]
            except IndexError:
                raise IndexError(f"Row index out of range for field {field_name}")

        if "columns" in traversal and field_value is not None:
            if not isinstance(field_value, list):
                raise TypeError(f"Field {field_name} is not an array")

            unwrap = False
            # Handle case where field_value is a single row after row indexing
            if "rows" in traversal and not isinstance(field_value[0], list):
                unwrap = True
                field_value = [field_value]

            start_idx = traversal["columns"]["start"] - 1
            end_idx = traversal["columns"]["end"] - 1

            try:
                if start_idx == end_idx:
                    field_value = [row[start_idx] for row in field_value]
                else:
                    field_value = [row[start_idx : end_idx + 1] for row in field_value]

                # Unwrap single row result
                if unwrap:
                    field_value = field_value[0]

            except IndexError:
                raise IndexError(f"Column index out of range for field {field_name}")

        if field_name is None or field_name == "All":
            all_dict = {}
            for field_name, field_value in object_info.items():
                all_dict[field_name] = field_parser.parse_field_value(
                    object_info.get("type"), field_name, field_value, traversal
                )
            return [all_dict]

        if "repeat" in traversal:
            if isinstance(field_value, list):
                subresults = []
                for field_obj in field_value:
                    subsubresults = []
                    # If we have more traversing to do to get the final field value,
                    # take the current level of recursion, find the final value, and append it
                    if "next" in traversal:
                        subtraversals = traversal["next"]
                        subsubresults.append(
                            parse_results_from_traversals(
                                objects_info,
                                field_parser.to_link(field_obj),
                                subtraversals,
                                field_parser,
                                depth=depth + 1,
                            )[0]
                        )
                    else:
                        subsubresults.append(
                            field_parser.parse_field_value(
                                object_info.get("type"),
                                field_name,
                                field_obj,
                                traversal,
                            )
                        )
                    subsubresults.append(
                        parse_results_from_traversals(
                            objects_info,
                            field_parser.to_link(field_obj),
                            traversals,
                            field_parser,
                            depth=depth + 1,
                        )[0]
                    )
                    subresults.append(subsubresults)
                results.append(subresults)
            elif field_value is not None:
                subresults = []
                if "next" in traversal:
                    subtraversals = traversal["next"]
                    subresults.append(
                        parse_results_from_traversals(
                            objects_info,
                            field_parser.to_link(field_value),
                            subtraversals,
                            field_parser,
                            depth=depth + 1,
                        )[0]
                    )
                else:
                    subresults.append(
                        field_parser.parse_field_value(
                            object_info.get("type"),
                            field_name,
                            field_value,
                            traversal,
                        )
                    )
                subsubresults = parse_results_from_traversals(
                    objects_info,
                    field_parser.to_link(field_value),
                    traversals,
                    field_parser,
                    depth=depth + 1,
                )[0]

                if subsubresults is not None:
                    subresults.extend(subsubresults)

                results.append(subresults)
            else:
                results.append(None)
        elif "next" in traversal:
            sub_traversals = traversal["next"]
            if isinstance(field_value, list):
                results.append(
                    [
                        parse_results_from_traversals(
                            objects_info,
                            field_parser.to_link(field_obj),
                            sub_traversals,
                            field_parser,
                            depth=depth + 1,
                        )[0]
                        for field_obj in field_value
                    ]
                )
            else:
                results.append(
                    parse_results_from_traversals(
                        objects_info,
                        field_parser.to_link(field_value),
                        sub_traversals,
                        field_parser,
                        depth=depth + 1,
                    )[0]
                )
        else:
            results.append(
                field_parser.parse_field_value(
                    object_info.get("type"),
                    field_name,
                    field_value,
                    traversal,
                )
            )

    return results


def parse_results_from_response(response_objects, objects, traversals, field_parser: ConstellationFieldParser):
    """Parse out the response for the requested fields and traversals."""
    results = []
    for obj in objects:
        obj_results = []
        for traversal in traversals:
            obj_results.append(
                parse_results_from_traversals(response_objects, obj, [traversal], field_parser, depth=0)[0]
            )
        results.append(obj_results)
    return results


def parse_field_values_from_response(response):
    """Parse out the field values contained in the response."""
    response_objects = {}
    field_summaries = {}
    response_fields = response.get("fields", {})
    response_field_summaries = response.get("summaries", {})
    ecl_type = response.get("resolved_object", {}).get("type")
    object_id = response.get("resolved_object", {}).get("id")

    if ecl_type is None or object_id is None:
        raise ConstellationObjectDoesNotExistException(response.get("object", {}).get("id"))

    response_objects[object_id] = {"type": ecl_type, "id": object_id}
    response_objects[object_id].update(response_fields)
    if ecl_type not in field_summaries:
        field_summaries[ecl_type] = {}
    field_summaries[ecl_type].update(response_field_summaries)
    for traversed_object in response.get("traversed_objects", []):
        (
            traversed_response_objects,
            traversed_field_summaries,
        ) = parse_field_values_from_response(traversed_object)
        response_objects.update(traversed_response_objects)

        # Merge field summaries instead of overwriting
        for type_key, summaries in traversed_field_summaries.items():
            if type_key not in field_summaries:
                field_summaries[type_key] = {}
            field_summaries[type_key].update(summaries)

    return response_objects, field_summaries


def build_traversal_from_tokens(tokens: list[str]):
    current_traversal = part_dict(tokens[0])

    if len(tokens) == 1:
        return current_traversal

    current_traversal.update({"next": [build_traversal_from_tokens(tokens[1:])]})
    return current_traversal


def build_traversal(field_string: str):
    tokens = split_on_brackets(field_string.replace(" ", ""))

    if len(tokens) == 0:
        return None

    return build_traversal_from_tokens(tokens)


def replace_repeated_pattern(input_string: str) -> str:
    pattern = r"Repeated\[(.*?)\]"
    return re.sub(pattern, r"{{\1}}", input_string)


def replace_array_pattern(input_string: str) -> str:
    # Match patterns like [[All,1]] or [[1]]
    pattern = r"\[\[(((All|\d+),)*\d+)\]\]"
    return re.sub(pattern, r"(\1)", input_string)


def split_on_brackets(input_string: str) -> list[str]:
    # First replace array access patterns
    transformed = replace_array_pattern(input_string)

    # Then replace Repeated[...] patterns
    transformed = replace_repeated_pattern(transformed)

    # Split on either '{{' or '['
    parts = [part for part in re.split(r"\[", transformed) if part]
    return [part.replace("]", "") for part in parts]


def part_dict(field_string: str) -> dict:
    single_index_pattern = r"(\w+)\((\d+)\)"
    multi_index_pattern = r"(\w+)\(All,\s*(\d+)\)"
    multi_specific_index_pattern = r"(\w+)\((\d+),\s*(\d+)\)"
    repeated_pattern = r"{{(.*)}}"

    repeated = False
    match = re.match(repeated_pattern, field_string)
    if match:
        repeated = True
        field_string = match.group(1)

    result: dict[str, Any] = {
        "name": field_string,
    }

    match = re.match(single_index_pattern, field_string)
    if match:
        result = {
            "name": match.group(1),
            "rows": {"start": int(match.group(2)), "end": int(match.group(2))},
        }

    match = re.match(multi_index_pattern, field_string)
    if match:
        result = {
            "name": match.group(1),
            "columns": {"start": int(match.group(2)), "end": int(match.group(2))},
        }

    match = re.match(multi_specific_index_pattern, field_string)
    if match:
        result = {
            "name": match.group(1),
            "rows": {"start": int(match.group(2)), "end": int(match.group(2))},
            "columns": {"start": int(match.group(3)), "end": int(match.group(3))},
        }

    if repeated:
        result["repeat"] = {"max": -1, "where": "", "inclusive_search": False}

    return result
