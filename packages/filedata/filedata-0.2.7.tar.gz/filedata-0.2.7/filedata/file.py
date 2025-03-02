import gzip
import io
import mimetypes
from typing import Optional

import requests
from pydantic.main import BaseModel
from requests_toolbelt import MultipartEncoder

from filedata.config import Config
from filedata.retry import retry_api

_session = requests.Session()


@retry_api
def get_file_meta(source: bytes, timeout: int = 20) -> dict:
    resp = _session.put(
        f'http://{Config.TIKA_HOST}/meta',
        data=source,
        headers={'Accept': 'application/json'},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


class FileInspection(BaseModel):
    file_bytes: bytes = None
    file_ext: str = None
    content_type: str = None
    content_encoding: str = None


def inspect_file(file_bytes: bytes, timeout: int = 20) -> FileInspection:
    meta = get_file_meta(file_bytes, timeout=timeout)

    content_type = meta.get('Content-Type')
    if content_type:
        content_type = content_type.split(';')[0]

    if content_type == 'application/gzip':
        file_bytes = gzip.decompress(file_bytes)
        meta = get_file_meta(file_bytes, timeout=timeout)
        content_type = meta.get('Content-Type')
        if content_type:
            content_type = content_type.split(';')[0]

    content_encoding = meta.get('Content-Encoding')
    if content_type is not None:
        file_ext: Optional[str] = mimetypes.guess_extension(content_type)
        if file_ext:
            file_ext = file_ext[1:]
    else:
        file_ext = None

    return FileInspection(
        file_bytes=file_bytes,
        file_ext=file_ext,
        content_type=content_type,
        content_encoding=content_encoding,
    )


@retry_api
def download_file_from_link(link: str, timeout: int = 20) -> requests.Response:
    resp = _session.get(
        link,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp


@retry_api
def extract_content_from_file(source: bytes, timeout: int = 20) -> Optional[str]:
    resp = _session.put(
        f'http://{Config.TIKA_HOST}/tika',
        data=source,
        timeout=timeout,
        headers={'Accept': 'text/plain'}
    )
    resp.raise_for_status()
    return resp.content.decode('utf-8')


content_file_ext = {
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'pdf': 'application/pdf',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}


@retry_api
def convert_to_pdf(source: bytes, filename: str = None, timeout: int = 20) -> Optional[bytes]:
    data = None
    if filename:
        ext = filename.rsplit('.', maxsplit=1)[-1]
        if ext in content_file_ext:
            data = (f'data.{ext}', io.BytesIO(source), content_file_ext[ext])
    if data is None:
        _meta = inspect_file(source, timeout=timeout)
        if _meta.content_type:
            data = ('data', io.BytesIO(source), _meta.content_type)
    if data is None:
        return

    payload = MultipartEncoder({'data': data})
    resp = _session.post(
        f'http://{Config.PDF_CONVERTER_HOST}/lool/convert-to/pdf',
        data=payload,
        headers={'Content-Type': payload.content_type},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.content
