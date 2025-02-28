from enum import Enum

import requests
from requests.adapters import Retry
from requests.adapters import HTTPAdapter
from tomlkit import item

from ._constants import ConnectorKeys


TAB_STRING: str = " " * 4


class RequestMode:
    POST: str = "post"
    PUT: str = "put"
    GET: str = "get"


def create_requests_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def parse_enum_to_value(data):
    if isinstance(data, list) or isinstance(data, tuple):
        return parse_list_enum_to_value(data)
    if isinstance(data, dict):
        return parse_dict_enum_to_value(data)
    return data.value if isinstance(data, Enum) else data


def parse_list_enum_to_value(data: list):
    return [parse_enum_to_value(v) for v in data]


def parse_dict_enum_to_value(data: dict):
    return {parse_enum_to_value(k): parse_enum_to_value(v) for k, v in data.items()}


def request(
    url: str,
    params={},
    data={},
    json={},
    headers={},
    files={},
    mode: str = RequestMode.POST,
    verify: bool = False,
):
    session = create_requests_session()
    r: requests.Response = getattr(session, mode)(
        url,
        params=parse_enum_to_value(params),
        json=parse_enum_to_value(json),
        data=parse_enum_to_value(data),
        headers=parse_enum_to_value(headers),
        files=parse_enum_to_value(files),
        verify=verify,
        timeout=1800
    )

    if r.status_code >= 400:
        raise Exception(
            f"Call request to {url} failed with status code {r.status_code}, response {r.text}"
        )
    try:
        response = r.json()
    except:
        response = r.text
    r.close()
    return response


def parse_to_str(data, tab_level: int = 0) -> str:
    if isinstance(data, list):
        return list_to_str(data, tab_level)
    if isinstance(data, tuple):
        return tuple_to_str(data, tab_level)
    if isinstance(data, dict):
        return dict_to_str(data, tab_level)
    return f"{data}"


def list_to_str(data: list, tab_level: int = 0) -> str:
    if len(data) == 0:
        return "[""]"
    return "[\n" + "".join([
        TAB_STRING * (tab_level + 1) +
        f"{parse_to_str(value, tab_level + 1)}\n" for value in data
    ]) + TAB_STRING * tab_level + "]"


def tuple_to_str(data: list, tab_level: int = 0) -> str:
    if len(data) == 0:
        return "("")"
    return "(\n" + "".join([
        TAB_STRING * (tab_level + 1) +
        f"{parse_to_str(value, tab_level + 1)}\n" for value in data
    ]) + TAB_STRING * tab_level + ")"


def dict_to_str(data: dict, tab_level: int = 0) -> str:
    if len(data) == 0:
        return "{""}"
    return "{\n" + "".join([
        f"{TAB_STRING * (tab_level + 1)}{key}: "
        f"{parse_to_str(value, tab_level + 1)}\n"
        for key, value in data.items()
    ]) + TAB_STRING * tab_level + "}"


def format_print(data):
    print(parse_to_str(data))


def get_chunk_size(chunk_size: int, file_size: int) -> int:
    if chunk_size > 0:
        if chunk_size > ConnectorKeys.UPLOAD_CHUNK_LARGE_SIZE.value:
            chunk_size = ConnectorKeys.UPLOAD_CHUNK_LARGE_SIZE.value
        return chunk_size

    if file_size < 15*1024*1024:
        return ConnectorKeys.UPLOAD_CHUNK_SMALL_SIZE.value
    elif file_size < 100*1024*1024:
        return ConnectorKeys.UPLOAD_CHUNK_MEDIUM_SIZE.value
    elif file_size < 1024*1024*1024:
        return ConnectorKeys.UPLOAD_CHUNK_NORMAL_SIZE.value

    return ConnectorKeys.UPLOAD_CHUNK_LARGE_SIZE.value
