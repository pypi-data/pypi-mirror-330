from __future__ import annotations

import base64
import functools
import json
import os
import pathlib
import tempfile
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from http import HTTPStatus
from itertools import count
from typing import Any, Generator, Optional

import backoff
import requests
import rollbar
import xmltodict

from .exceptions import (
    ConstellationException,
    ConstellationInvalidMethodException,
    ConstellationInvalidResponseException,
    ConstellationMissingFieldException,
    ConstellationNotLoggedInException,
    ConstellationObjectDoesNotExistException,
    ConstellationUnauthorizedRequestError,
)
from .models import (
    BlobRef,
    CloudFileArgs,
    ConstellationFieldParser,
    Function,
    ListableKind,
    ListableType,
    Model,
    Object,
    ResultPayload,
    deserialize_item,
)
from .parsers import (
    build_traversal,
    parse_field_values_from_response,
    parse_results_from_response,
)
from .utils import create_two_way_link, extend, md5_hash_file, parts_to_xml, tmap

UPLOAD_PART_SIZE = 10_000_000  # 10 MB
MULTIPART_CLOUDFILE_THRESHOLD = 100_000_000  # 100 MB
NOTEBOOK_ID_HEADER = "X-ECL-NotebookId"


class Constellation:
    def __init__(self, auth_token: str | None = None, host: str | None = None):
        self._host = host or "https://constellation.emeraldcloudlab.com"
        self._auth_token = auth_token

        self._temp_directory = None

        # set the sleep time for getting API results here
        self._sleep_time = 0.3
        self._max_sleep_time = 600

        self._headers = {}

    # Retry decorator for requests failures (like timeout or connection error)
    _retry_requests_decorator = backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_tries=5,
    )

    # Configuration related functions
    def host(self):
        """Return the url of the instance constellation that the client is
        connecting to."""
        return self._host

    def download_directory(self):
        """Returns where cloud file downloads are stored."""
        if self._temp_directory is None:
            self._temp_directory = tempfile.TemporaryDirectory()

        return self._temp_directory.name

    @staticmethod
    def from_env(*, prefix: str | None = None, host: str | None = None) -> Constellation:
        """Credentials are loaded from the environment. If
        CONSTELLATION_AUTH_TOKEN is present, is it pushed into the client.
        Otherwise, CONSTELLATION_USERNAME, CONSTELLATION_PASSWORD are used to
        issue a call to the login method.

        Any prefix that is passed is applied to the environment
        variables. For example, prefix="PYTEST" means look up
        PYTEST_CONSTELLATION_AUTH_TOKEN and so on.
        """
        key = lambda k: "_".join([prefix or "", k])

        client = Constellation(host=host)
        try:
            auth_token = os.environ[key("CONSTELLATION_AUTH_TOKEN")]
        except KeyError:
            username, password = (os.environ[key(k)] for k in ["CONSTELLATION_USERNAME", "CONSTELLATION_PASSWORD"])
            client.login(username, password)
        else:
            client._auth_token = auth_token

        return client

    # Identity requests
    @_retry_requests_decorator
    def login(self, username: str | None = None, password: str | None = None):
        """Return the auth token token for the supplied username and
        password."""

        username = username or os.environ["CONSTELLATION_USERNAME"]
        password = password or os.environ["CONSTELLATION_PASSWORD"]

        auth_token = self._send_and_validate_request(
            "/ise/signintoken",
            {"username": username, "password": password},
            "AuthToken",
            requires_auth_token=False,
        )
        self.set_auth_token(auth_token)
        return self.me()

    def is_logged_in(self) -> bool:
        return bool(self._auth_token)

    def set_auth_token(self, auth_token: str):
        """Set the auth token used by the constellation client."""
        self._auth_token = auth_token

    @_retry_requests_decorator
    def me(self):
        """Return the response from the /ise/me endpoint."""
        return self._send_and_validate_request("/ise/me", None, None, method="GET")

    # Searching objects
    def search(self, ecl_type, query, max_results: int | None = None):
        """Perform a simple search on a given type."""
        payload = {
            "queries": [
                {
                    "clauses": [
                        {
                            "Types": [ecl_type],
                            "Query": query,
                        }
                    ],
                    "SubTypes": True,
                    "SoftLimit": max_results,
                    "date": None,
                    "ignore_time": False,
                }
            ],
        }

        return self._send_and_validate_request(
            "/obj/search",
            payload,
            field_to_retrieve="Results",
        )

    # Downloading objects
    def download(
        self,
        objects,
        fields: str | list[str] | set[str] = "All",
        auto_download_cloud_files=False,
        byte_size: Optional[int] = None,
    ) -> Any:
        """Download the supplied fields off the supplied object or objects.

        Note that fields can traverse across links using []'s.  For
        example:

        download(self.me()["ID"], "FinancingTeams[Name]")

        will download the status field off the protocol link of the
        supplied object.
        """
        result = None
        collapse_fields = False
        collapse_objects = False

        if isinstance(fields, str):
            field_list = [fields]
            collapse_fields = True
        elif isinstance(fields, list):
            field_list = fields
        elif isinstance(fields, set):
            field_list = list(fields)

        if not isinstance(objects, list):
            objects = [objects]
            collapse_objects = True

        result = self._download_objects(objects, field_list, auto_download_cloud_files, byte_size=byte_size)

        # Unwind the normalization of fields and object ids into lists
        if collapse_fields and collapse_objects:
            return result[0][0]

        if collapse_fields:
            return [x[0] for x in result]

        if isinstance(fields, set):
            result = [{key: value for key, value in zip(field_list, row, strict=True)} for row in result]

        if collapse_objects:
            return result[0]

        return result

    def _download_objects(
        self,
        objects,
        fields: list[str],
        auto_download_cloud_files,
        byte_size: Optional[int] = None,
    ):
        """Download multiple objects in a single request."""

        # Build the request
        traversals = [build_traversal(traversal) for traversal in fields]
        obj_requests = [
            {
                "object": {"id": obj.id},
                "limit": 0,
                "subfield_info": True,
                "traversals": traversals,
            }
            for obj in objects
        ]

        # Send the request to constellation
        responses = self._send_and_validate_request(
            "/obj/download",
            {"requests": obj_requests},
            "responses",
        )
        if len(responses) != len(objects):
            raise ConstellationInvalidResponseException(
                f"Expected exactly {len(objects)} response from /obj/download", responses
            )

        # Parse the json results into objects
        response_objects = {}
        field_parser = ConstellationFieldParser()
        for response in responses:
            (
                sub_response_objects,
                sub_response_field_summaries,
            ) = parse_field_values_from_response(response)
            response_objects.update(sub_response_objects)
            for ecl_type, field_summaries in sub_response_field_summaries.items():
                field_parser.add_summaries_for_type(field_summaries, ecl_type)

        # Map the objects into a formatted result based on the fields string
        parsed_results = parse_results_from_response(response_objects, objects, traversals, field_parser)

        # now we want to download all the blob refs all in one go, and parse them locally
        paths = self.download_blob_ref(field_parser._blob_refs_encountered)
        parsed_blobs = [field_parser.parse_local_file(p) for p in paths]
        # create a blob ref store from the connecting the blob ref file hashes to their parsed values
        blob_store = {blob.file_hash: value for blob, value in zip(field_parser._blob_refs_encountered, parsed_blobs)}

        # exchange the blobs in the results with their parsed values
        self._replace_blob_values(parsed_results, blob_store)

        # If requested, go ahead and download all the cloud files encountered
        if auto_download_cloud_files:
            self.download_cloud_file(field_parser.cloud_files_encountered(), byte_size=byte_size)

        # return the results
        return parsed_results

    def resolve_type(self, obj: ListableKind) -> ListableKind:
        """Queries Constellation for the object(s) type(s) and injects them
        into the input object(s).

        >>> obj = Object("id:qdkmxzGkAK0a")
        >>> obj
        Object["id:qdkmxzGkAK0a"]
        >>> client.resolve_type(obj)
        >>> obj
        Object[Sample, "id:qdkmxzGkAK0a"]
        """
        match obj:
            case Object() | Model():
                objects = [obj]
            case _:
                objects = list(obj)

        responses = self._send_and_validate_request(
            "/obj/download",
            {
                "requests": [
                    {
                        "object": {"id": obj.id},
                        "fields": ["ID"],
                    }
                    for obj in objects
                ]
            },
            "responses",
        )
        for object, response in zip(objects, responses):
            try:
                resolved_object = response["resolved_object"]
            except KeyError:
                raise ConstellationObjectDoesNotExistException(object.id)
            object.type = resolved_object["type"]

        return obj

    def _replace_blob_values(self, parsed_results: list, store: dict) -> None:
        """Replace the BlobRef values in the parsed results list with their
        associated python types that have been parsed from their downloaded
        file.

        Note that this function replaces the values in-line so the
        original parsed results list is mutated in the process.
        """
        for i in range(len(parsed_results)):
            pr = parsed_results[i]
            if isinstance(pr, list):
                self._replace_blob_values(pr, store)
            elif isinstance(pr, BlobRef):
                parsed_results[i] = store[pr.file_hash]
        return None

    # Downloading cloud files
    def download_cloud_file(self, cloud_files: list[Object] | Object, byte_size: Optional[int] = None):
        """Download the supplied cloud file to client.download_directory()"""
        # process singleton inputs into lists
        singleton_flag = False
        if not isinstance(cloud_files, list):
            cloud_files = [cloud_files]
            singleton_flag = True

        # download the s3 information in one go
        cf_info_list = self.download(cloud_files, ["FileName", "FileType", "CloudFile"])

        # unpack the results
        file_names = [
            cfi[0] if cfi[0] else f"EmeraldCloudFile_{cf.id.replace(':', '_')}"
            for cfi, cf in zip(cf_info_list, cloud_files)
        ]
        extensions = [cfi[1].replace('"', "") for cfi in cf_info_list]
        file_infos = [cfi[2] for cfi in cf_info_list]
        target_paths = [self._get_temp_file_path(fn, ext) for fn, ext in zip(file_names, extensions)]

        # prepare a function to thread over by enclosing the bytesize option into the main helper function
        # yielding a lambda that takes in 2 arguments, a file_info and a path
        def parallel_func(file_info: dict, path: str):
            return self._download_cloud_file(
                file_info["CloudFileId"], file_info["Bucket"], file_info["Key"], path, byte_size=byte_size
            )

        # parallel map over the s3 downloads
        target_paths = tmap(parallel_func, file_infos, target_paths)

        # update the cloud file objects with the path information
        for cf, tp in zip(cloud_files, target_paths):
            cf.local_path = tp

        # if a singleton file was requested, unpack the list into a singleton object
        if singleton_flag:
            target_paths = target_paths[0]
        return target_paths

    def _get_temp_file_path(self, filename, extension):
        """Get a temp file path as close to filename as possible."""
        index = 0
        target_path = os.path.join(self.download_directory(), f"{filename}.{extension}")
        while os.path.exists(target_path):
            target_path = os.path.join(self.download_directory(), f"{filename}_{index}.{extension}")
            index += 1

        return target_path

    def blobsign_download(self, cloud_file_id, cloud_file_bucket, cloud_file_key):
        """Return the url to download the supplied cloud file."""
        return self._send_and_validate_request(
            "/blobsign/download",
            {
                "CloudFileId": cloud_file_id,
                "Bucket": cloud_file_bucket,
                "Key": cloud_file_key,
            },
            "Url",
        )

    def _download_cloud_file(
        self, cloud_file_id, cloud_file_bucket, cloud_file_key, target_path, byte_size: Optional[int] = None
    ):
        """Download a cloud file based off the supplied identifiers.

        Default byte_size is None, in which case file will download in a
        single request. Note, byte ranges are inclusive, so getting
        0-1024, and then 1024-2048 would downlaod the 1024th byte twice.
        """

        url = self.blobsign_download(cloud_file_id, cloud_file_bucket, cloud_file_key)
        if not url:
            raise ConstellationMissingFieldException("When downloading cloud file", "url")

        # Now download the file from s3
        target_file = open(target_path, "wb")
        if byte_size is None:
            download_response = requests.get(url)
            target_file.write(download_response.content)
        else:
            assert byte_size > 0, "Expected `byte_size` value to be positive"
            chunks = lambda w: ((lower, lower + w - 1) for lower in count(0, step=w))  # noqa: E731
            for lower, upper in chunks(byte_size):
                download_response = requests.get(url, headers={"Range": f"bytes={lower}-{upper}"})
                if download_response.status_code != HTTPStatus.PARTIAL_CONTENT:
                    break
                target_file.write(download_response.content)

        return target_path

    def download_blob_ref(
        self, blob_refs: list[BlobRef] | BlobRef, target_path="", byte_size: Optional[int] = None
    ) -> list[str] | str:
        """Download a blob ref to the supplied target path."""
        singleton_flag = not isinstance(blob_refs, list)
        if singleton_flag:
            blob_refs = [blob_refs]
        target_paths = [target_path or self._get_temp_file_path(br.file_hash, "tmp") for br in blob_refs]

        cloud_file_buckets = [br.bucket for br in blob_refs]
        cloud_file_keys = [br.key() for br in blob_refs]
        # check the buckets
        if any(not bucket for bucket in cloud_file_buckets):
            raise ConstellationMissingFieldException("When downloading cloud file", "bucket")
        if any(not key for key in cloud_file_keys):
            raise ConstellationMissingFieldException("When downloading cloud file", "hash")

        parallel_fn = functools.partial(self._download_cloud_file, cloud_file_id="", byte_size=byte_size)
        target_paths = tmap(
            parallel_fn, cloud_file_bucket=cloud_file_buckets, cloud_file_key=cloud_file_keys, target_path=target_paths
        )
        # update the blob ref paths
        for br, tp in zip(blob_refs, target_paths):
            br.local_path = tp

        # unpack the singleton if necessary
        if singleton_flag:
            target_paths = target_paths[0]
        return target_paths

    def upload(self, object_type, object_id, new_field_values, allow_public_objects: bool = False):
        """Performs a very simple upload of a list of fields on a single
        object.

        Pass `None` for object_id to create a new object. By default, new objects will be linked to
        the requesting user's default notebook (or their financing team's default notebook). In order
        to allow for public objects to be created, the `allow_public_objects` flag need to be explicitly
        set to `True`.
        """
        request_body = {
            "object": {"id": object_id, "type": object_type},
            "fields": new_field_values,
        }
        if object_id is None:
            # If you have no object id because you're creating a new object,
            # you need to format it slightly differently
            request_body = {"type": object_type, "fields": new_field_values}
        responses = self._send_and_validate_request(
            "/obj/upload",
            {"requests": [request_body]},
            "responses",
            method="PUT",
            additional_headers={"X-ECL-AllowPublicObjects": "true"} if allow_public_objects else None,
        )

        if len(responses) != 1:
            raise ConstellationInvalidResponseException("Expected exactly 1 response from /obj/upload", responses)

        return responses[0]

    # Uploading cloud files
    def upload_cloud_file(self, file_path, notebook_id: str | None = None):
        """Uploads the given file to constellation."""
        md5 = md5_hash_file(file_path)
        extension = pathlib.Path(file_path).suffix
        if extension:
            extension = extension[1:]  # Remove the dot
        with open(file_path, "rb") as file:
            cloud_file_args = CloudFileArgs(
                file=file,
                name=pathlib.Path(file_path).stem,
                extension=extension,
                path=file_path,
                size=os.path.getsize(file_path),
                key=f"{md5.hexdigest()}.{extension}",
                content_md5=base64.b64encode(md5.digest()).decode(),
                content_disposition=f'attachment; filename="{file_path}"',  # noqa
            )

            method = (
                self._single_sign_and_upload_file_to_s3
                if cloud_file_args.size < MULTIPART_CLOUDFILE_THRESHOLD
                else self._multi_part_sign_and_upload_file_to_s3
            )

            return method(cloud_file_args, notebook_id)

    @_retry_requests_decorator
    def _single_sign_and_upload_file_to_s3(self, cloud_file_args, notebook_id: str | None = None):
        blobsign_response = self._blobsign("upload", cloud_file_args)
        headers = {
            "Content-Md5": cloud_file_args.content_md5,
            "Content-Disposition": cloud_file_args.content_disposition,
        }
        cloud_file_args.file.seek(0)
        s3_response = requests.put(
            url=blobsign_response["Url"],
            data=cloud_file_args.file,
            headers=headers,
        )
        if s3_response.status_code != HTTPStatus.OK:
            raise ConstellationException(
                f"Unexpected non-200 response from constellation endpoint {s3_response}: {s3_response.text}",
                s3_response.status_code,
            )
        return self._upload_cloud_file_to_constellation(blobsign_response["Key"], cloud_file_args, notebook_id)

    @_retry_requests_decorator
    def _upload_cloud_file_to_constellation(self, s3_key, cloud_file_args, notebook_id: str | None = None):
        cloud_field_values = {
            "$Type": "__JsonEmeraldCloudFile__",
            "Bucket": "emeraldsci-ecl-blobstore-stage",
            "CloudFileId": "None",
            "Key": s3_key,
        }
        fields = extend(
            {
                "FileName": cloud_file_args.name,
                "FileSize": f'Quantity[{cloud_file_args.size}, "bytes"]',
                "FileType": f'"{cloud_file_args.extension}"',
                "CloudFile": cloud_field_values,
            },
            (
                {
                    "Notebook": create_two_way_link(
                        linked_field="Objects", linked_id=notebook_id, linked_type="Object.LaboratoryNotebook"
                    )
                }
                if notebook_id is not None
                else {}
            ),
        )

        return self.upload("Object.EmeraldCloudFile", None, fields)

    def _blobsign(self, sign_type, cloud_file_args: CloudFileArgs, part=0, upload_id=""):
        """Return the url to upload the supplied cloud file."""
        sign_response = self._send_and_validate_request(
            "/blobsign/" + sign_type,
            {
                "Key": cloud_file_args.key,
                "ContentMD5": cloud_file_args.content_md5,
                "ContentDisposition": cloud_file_args.content_disposition,
                "Part": part,
                "UploadID": upload_id,
            },
            additional_headers={"ContentDisposition": cloud_file_args.content_disposition},
        )
        return sign_response

    def _multi_part_sign_and_upload_file_to_s3(self, cloud_file_args, notebook_id: str | None = None):
        upload_id, sharded_key = self._send_create_multi_part_upload_request(cloud_file_args)
        try:
            parts = self._upload_all_parts(upload_id, cloud_file_args)
            self._send_complete_multi_part_upload_request(upload_id, parts, cloud_file_args)
        except Exception as cloudFileUploadException:
            self._send_abort_multi_part_upload_request(upload_id, cloud_file_args)
            raise ConstellationException(
                "Unexpected exception while uploading cloud file", HTTPStatus.INTERNAL_SERVER_ERROR
            ) from cloudFileUploadException
        return self._upload_cloud_file_to_constellation(sharded_key, cloud_file_args, notebook_id)

    @_retry_requests_decorator
    def _send_create_multi_part_upload_request(self, cloud_file_args):
        blobsign_response = self._blobsign("init_multi_upload", cloud_file_args)
        s3_response = requests.post(
            url=blobsign_response["Url"],
        )
        if s3_response.status_code != HTTPStatus.OK:
            raise ConstellationException(
                f"Unexpected non-200 response from s3 endpoint {s3_response}: {s3_response.text}, "
                "failed to init multi-part upload",
                s3_response.status_code,
            )
        parsed_response = xmltodict.parse(s3_response.content)
        return (
            parsed_response["InitiateMultipartUploadResult"]["UploadId"],
            parsed_response["InitiateMultipartUploadResult"]["Key"],
        )

    @_retry_requests_decorator
    def _send_complete_multi_part_upload_request(self, upload_id, parts, cloud_file_args):
        blobsign_response = self._blobsign("complete_multi_upload", cloud_file_args, upload_id=upload_id)
        s3_response = requests.post(url=blobsign_response["Url"], data=parts_to_xml(parts))
        if s3_response.status_code != HTTPStatus.OK:
            raise ConstellationException(
                f"Unexpected non-200 response from s3 endpoint {s3_response}: {s3_response.text}, "
                "failed to complete multi-part upload",
                s3_response.status_code,
            )

    @_retry_requests_decorator
    def _send_abort_multi_part_upload_request(self, upload_id, cloud_file_args):
        blobsign_response = self._blobsign("abort_multi_upload", cloud_file_args)
        s3_response = requests.delete(url=blobsign_response["Url"])
        if s3_response.status_code != HTTPStatus.OK:
            rollbar.report_message(
                "Failed to abort multi part upload. "
                f"UploadID: {upload_id}, Key: {blobsign_response['Key']}, "
                f"S3 response: {s3_response} {s3_response.text}",
                "error",
            )
            raise ConstellationException(
                f"Unexpected non-200 response from s3 {s3_response}: {s3_response.text}, "
                "failed to abort multi part upload",
                s3_response.text,
            )

    def _upload_all_parts(self, upload_id, cloud_file_args):
        current_part_number = 1
        parts = []
        chunk = cloud_file_args.file.read(UPLOAD_PART_SIZE)
        while chunk != b"":
            part = self._upload_part(upload_id, current_part_number, chunk, cloud_file_args)
            parts.append(part)
            current_part_number += 1
            chunk = cloud_file_args.file.read(UPLOAD_PART_SIZE)
        return parts

    @_retry_requests_decorator
    def _upload_part(self, upload_id, part_number, data_chunk, cloud_file_args):
        blobsign_response = self._blobsign("upload_part", cloud_file_args, part=part_number, upload_id=upload_id)
        s3_response = requests.put(
            url=blobsign_response["Url"],
            data=data_chunk,
        )
        if s3_response.status_code != HTTPStatus.OK:
            raise ConstellationException(
                f"Unexpected non-200 response from s3 endpoint {s3_response}: {s3_response.text}, "
                "failed to upload part",
                s3_response.status_code,
            )
        return {"ETag": s3_response.headers["ETag"], "PartNumber": part_number}

    # Getting history of changes to an object
    def object_log(
        self,
        object_ids=None,
        types=None,
        start_date=None,
        end_date=None,
        max_results=1000,
    ):
        """Find changes on the supplied types after the supplied start_date."""
        payload = {
            "limit": max_results,
            "order": "dsc",
        }
        if object_ids is not None:
            payload["object"] = [{"id": x} for x in object_ids]
        if types is not None:
            payload["Types"] = types
        if start_date is not None:
            payload["startDate"] = start_date
        if end_date is not None:
            payload["endDate"] = end_date
        return self._send_and_validate_request(
            "/obj/objectlog",
            payload,
        )

    # Getting type information
    def get_type(self, type_name):
        """Retrieve all of the fields and their formats for a given type."""
        return self._send_and_validate_request(
            "/obj/type/{}".format(type_name),
            {},
            method="GET",
        )

    # Internal helper functions
    def _auth_header_from_token(self, auth_token):
        """Build a authorization header when an auth token is supplied."""
        return {"Authorization": "Bearer " + str(auth_token)}

    def _send_and_validate_request(
        self,
        path,
        data,
        field_to_retrieve=None,
        method="POST",
        requires_auth_token=True,
        additional_headers=None,
    ):
        """Send a request and validate a request to the given path."""
        if requires_auth_token and not self._auth_token:
            raise ConstellationNotLoggedInException()

        url = self._host + path
        if additional_headers is None:
            additional_headers = {}
        headers = extend(
            self._headers,
            {"Content-type": "application/json"},
            additional_headers,
        )
        if self._auth_token:
            headers.update(self._auth_header_from_token(self._auth_token))
        if method == "POST":
            response = requests.post(
                url=url,
                data=json.dumps(data),
                headers=headers,
            )
        elif method == "PUT":
            response = requests.put(
                url=url,
                data=json.dumps(data),
                headers=headers,
            )
        elif method == "GET":
            response = requests.get(url=url, headers=headers)
        else:
            raise ConstellationInvalidMethodException(method, path)

        # since Constellation will double as an authorization service, be more specific about invalid tokens.
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise ConstellationUnauthorizedRequestError

        if response.status_code != HTTPStatus.OK:
            raise ConstellationException(
                f"Unexpected non-200 response from constellation endpoint {url}: {response.text}",
                response.status_code,
            )

        if field_to_retrieve:
            field_value = response.json().get(field_to_retrieve)
            if not field_value:
                raise ConstellationInvalidResponseException(
                    f"Could not retrieve field {field_to_retrieve} from request to {path}",
                    response.text,
                )
            return field_value

        return response.json()

    def run(self, func: Function) -> SLLResult:
        """Primary method for interacting with the SLL API. This method submits
        an experiment/analysis/simulation on AWS, and quickly returns if the
        request was successful. The data from the result is not immediately
        stored, and is instead lazily queried when you need it.

        :param func: The object representing the analysis/simulation/experiment function.
        :type func: Function
        :returns: A result object that contains the data from the function evaluation in the `result`, `error`,
        and `messages` fields.
        :rtype: SLLResult
        """
        # create the payload from the function object, making sure to jsonify function
        # this is b/c the function json string is to be passed through the go endpoint, and into MM kernels
        payload = {"function": json.dumps(asdict(func.payload()))}
        # construct the request
        url = f"{self.host()}/obj/sll/run_function"

        assert self._auth_token
        headers = {"Authorization": f"Bearer {self._auth_token}", "Content-Type": "application/json"}
        resp = requests.post(url=url, data=payload, headers=headers)
        resp = self._run_api_function(url=url, payload=payload, headers=headers)

        # handle non-200 responses in a heavy-handed way for now
        if resp.status_code != 200:
            try:
                message = resp.json().get("message")
            except Exception:
                raise ValueError("Something went wrong on the API backend.")
            raise ValueError(f"Error occurred while submitting command to API. Message: {message}")
        command = resp.json()["command"]
        return SLLResult(command=Object(command["id"]), client=self)

    def get_results(self, command: Object) -> ResultPayload:
        # run the get request
        url = f"{self.host()}/obj/sll/function_results?command={command.id}"
        headers = {"Authorization": f"Bearer {self._auth_token}", "Content-Type": "application/json"}
        resp = self._get_api_results(url=url, headers=headers)

        # handle errors
        self._handle_get_results_errors(resp)

        # safe to try to unpack results
        res = resp.json().get("result")

        # if result is None, then we'll have to do a wait-and-poll again flow
        total_sleep_time = 0
        # 2 ** counter generator: e.g. first val is 1, second is 2, third is 4, etc.
        backoff_generator = backoff.expo()
        while res is None:
            if total_sleep_time > self._max_sleep_time:
                raise ValueError(
                    f"Result not found after waiting for more than {self._max_sleep_time / 60.0} minutes. "
                    "Try again later."
                )
            # apply jitter to prevent any concurrent race conditions
            sleep = self._exp_backoff_time(backoff_generator)
            time.sleep(sleep)
            resp = requests.get(url=url, headers=headers)
            res = resp.json().get("result")
            total_sleep_time += sleep
        return ResultPayload(**json.loads(res))

    def _exp_backoff_time(self, backoff_iter: Generator) -> float:
        # NOTE: this initialization needs to happen with backoff 2.x.x otherwise the
        # generator returns None on next calls
        backoff_iter.send(None)
        # apply jitter to prevent any concurrent race conditions
        return self._sleep_time * backoff.full_jitter(next(backoff_iter))

    def _handle_get_results_errors(self, resp: requests.Response):
        # handle non-200 responses in a heavy-handed way for now
        if resp.status_code != 200:
            try:
                message = resp.json().get("message")
            except Exception:
                raise ValueError("Something went wrong on the API backend.")
            raise ValueError(f"Error occurred while submitting command to API. Message: {message}")

    @_retry_requests_decorator
    def _run_api_function(self, url: str, payload: dict, headers: dict) -> requests.Response:
        return requests.post(url=url, data=json.dumps(payload), headers=headers)

    @_retry_requests_decorator
    def _get_api_results(self, url: str, headers: dict) -> requests.Response:
        return requests.get(url=url, headers=headers)

    @contextmanager
    def notebook(self, notebook_id: str):
        original_notebook_id: str | None = self._headers.get(NOTEBOOK_ID_HEADER)
        self._headers[NOTEBOOK_ID_HEADER] = notebook_id
        try:
            yield self
        finally:
            if original_notebook_id:
                self._headers[NOTEBOOK_ID_HEADER] = original_notebook_id
            else:
                _ = self._headers.pop(NOTEBOOK_ID_HEADER)


def needs_response(fn):
    @functools.wraps(fn)
    def wrapper(self: SLLResult, *args, **kwargs):
        if self._response is None:
            payload = self._client.get_results(self._command)
            self._response = SLLResult.Response(payload=payload, result=deserialize_item(payload.result))
        return fn(self, *args, **kwargs)

    return wrapper


class SLLResult:
    @dataclass
    class Response:
        payload: ResultPayload
        result: ListableType

    def __init__(self, command: Object, client: Constellation):
        self._command = command
        self._client = client

        self._response: SLLResult.Response | None = None

    def __repr__(self) -> str:
        default = "<Unevaluated>"
        result = self._response.result if self._response else default
        error = self._response.payload.error if self._response else default
        messages = self._response.payload.messages if self._response else default
        return f"SLLResult(result={result}, error={error}, messages={messages})"

    @property
    @needs_response
    def result(self) -> ListableType | None:
        assert self._response
        return self._response.result

    @property
    @needs_response
    def error(self) -> bool | None:
        assert self._response
        return self._response.payload.error

    @property
    @needs_response
    def messages(self) -> list[str] | None:
        assert self._response
        return self._response.payload.messages
