import datetime
import hashlib
import threading
from functools import reduce
from typing import Any


def constellation_date_string(dt):
    """Return a datetime formatted in the format constellation
    wants as a string like: 2021-02-17T15:16:36Z

    Note - the datetime object must be in utc time."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def constellation_date_from_string(date_string):
    """Return a datetime object from the string format that constellation
    uses like: 2021-02-09T04:12:02.618767Z

    Note - the datetime object will be in utc time."""
    # Handle both second and subsecond precision on datetimes
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        pass

    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


def parts_to_xml(parts):
    part_nodes = "\n".join(
        f"""
        <Part>
            <ETag>{part["ETag"]}</ETag>
            <PartNumber>{part["PartNumber"]}</PartNumber>
        </Part>
        """
        for part in parts
    )

    xml = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <CompleteMultipartUpload xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        {part_nodes}
        "</CompleteMultipartUpload>"
    """

    return xml.encode("ascii")


def md5_hash_file(file_path):
    with open(file_path, "rb") as file:
        chunk_size = 1_000_000  # 1MB, a bit arbitrary
        md5 = hashlib.md5()
        chunk = file.read(chunk_size)
        while chunk:
            md5.update(chunk)
            chunk = file.read(chunk_size)
        return md5


def create_one_way_link(linked_type: str, linked_id: str):
    """Given the type and id in an object, create a two-way link to that
    object."""
    return {
        "$Type": "__JsonLink__",
        "object": {"id": linked_id, "type": linked_type},
    }


def create_two_way_link(linked_type: str, linked_id: str, linked_field: str):
    """Given the type, id and field in an object, create a two-way link to that
    object."""
    return {
        "$Type": "__JsonLink__",
        "object": {"id": linked_id, "type": linked_type},
        "field": {"name": linked_field},
    }


def extend(*dicts: dict) -> dict:
    """Returns a dictionary that combines all dictionaries passed as arguments
    without mutating any of them.

    >>> extend({"foo": "bar"}, {"food": "taco"})
    {"foo": "bar", "food": "taco"}
    >>> extend({"food": "cake"}, {"food": "taco", "answer": 42})
    {"food": "taco", "answer": 42}
    """

    def fold(acc: dict, curr: dict) -> dict:
        acc.update(curr)
        return acc

    return reduce(fold, dicts, {})


def truthy(v: str | None) -> bool:
    """
    >>> set(map(truthy, ["1", "true", "True", "TRUE", "tRuE", "on", "ON"]))
    {True}
    >>> set(map(truthy, [None, "", " ", "0", "0.0", "false", "False", "FALSE", "fAlSe", "off", "OFF"]))
    {False}
    """
    v = (v or "").strip()
    if v.lower() in {"true", "on"}:
        return True
    if v.lower() in {"false", "off"}:
        return False
    try:
        return bool(float(v))
    except ValueError:
        return bool(v)


def tmap(fn, *collections, **kw_collections) -> list[Any]:
    """Concurrent map.

    Map each item in each of the collections/keyword collections with
    the provided function in a separate thread.
    `tmap` can drastically improve performance when compared to
    `map` but should only be used for IO-bound functions that have
    no side effects.
    >>> tmap(download, urls)
    [<url1_data>, <url2_data>, <url3_data>]
    >>> datasets = tmap(read_csv, files)

    To thread a function over multiple inputs, you can provide multiple
    collections as positional arguments.
    >>> tmap(download, urls, fields)
    [<url1_field1_data>, <url2_field2_data>, ...]
    Note that each of the above functional evaluations are of the form
    `download(urls[i], fields[i])` where `i` is the index. Note that
    each collection must be the same length.

    If e.g. `download` has keyword arguments, then you may input other
    collections as keyword arguments.
    >>> tmap(download, urls, field=fields)
    [<url1_field1_data>, <url2_field2_data>, ...]
    which evaluates as `download(urls[i], field=fields[i])` for each
    element in the collections provided.
    """

    # check that each of the collections are the same size
    # set n to be either the first collection length or the first kwarg collection length
    if len(collections) > 0:
        n = len(collections[0])
    else:
        n = len(tuple(kw_collections.values())[0])
    for c in collections:
        if len(c) != n:
            raise ValueError("The collections passed to tmap must have the same length.")
    for key in kw_collections.keys():
        if len(kw_collections[key]) != n:
            raise ValueError("The collections passed to tmap must have the same length.")
    payload = [None] * n

    def process(i):
        args = (c[i] for c in collections)
        kwargs = {key: c[i] for key, c in kw_collections.items()}
        payload[i] = fn(*args, **kwargs)

    threads = [threading.Thread(target=process, args=(i,)) for i in range(n)]

    each("start", threads)
    each("join", threads)

    return payload


def each(accept, iterable, *args, **kwargs):
    """Applies the accept function to each of the elements in the iterable
    collection."""
    if isinstance(accept, str):
        methods = [getattr(item, accept) for item in iterable]
        _ = [method(*args, **kwargs) for method in methods]
        return

    unpack = kwargs.get("_unpack", False)
    for item in iterable:
        _args = (item,) if not unpack else item
        accept(*_args)
