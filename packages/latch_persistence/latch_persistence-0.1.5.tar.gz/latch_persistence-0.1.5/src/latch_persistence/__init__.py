import base64
import hashlib
import math
import mimetypes
import os as _os
import time
import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
from threading import Thread, Semaphore
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter, Retry


@dataclass
class LatchConfig(object):
    """
    Latch specific configuration values
    """

    endpoint: str = "https://nucleus.latch.bio"
    upload_chunk_size_bytes: int = 10000000

    @classmethod
    def auto(cls, config_file=None) -> "LatchConfig":
        return LatchConfig()


"""
Thread Utils For Downloading Directories
"""


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.tasks: Queue = Queue(-1)
        self.threads: List[Worker] = []
        self.cache_accum = bytearray([0] * 32)
        for _ in range(num_threads):
            self.threads.append(Worker(self.tasks))

    def start(self):
        for t in self.threads:
            t.start()

    def join(self):
        for t in self.threads:
            t.join()

            for i in range(len(self.cache_accum)):
                self.cache_accum[i] ^= t.cache_accum[i]

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """Add a list of tasks to the queue"""
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        try:
            self.tasks.join()
        finally:
            self.join()


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, tasks: Queue):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.cache_accum = bytearray([0] * 32)

    def run(self):
        while True:
            try:
                func, args, kargs = self.tasks.get_nowait()
            except Empty:
                break

            try:
                attempts = 0
                while True:
                    try:
                        res = func(*args, **kargs)

                        if res is not None and res["cache"] is not None:
                            hash = hashlib.sha256(res["cache"].encode("utf-8")).digest()
                            for i in range(len(self.cache_accum)):
                                self.cache_accum[i] ^= hash[i]

                        break
                    except Exception as e:
                        attempts += 1
                        if attempts >= 5:
                            raise e
                        time.sleep(0.1 * 2**attempts)
            except Exception:
                traceback.print_exc()
            finally:
                self.tasks.task_done()


download_part_size = 1024 * 1024 * 100
write_chunk_size = 1024 * 1024
num_concurrent_downloads = 8


def urlretrieve(url: str, start: int, end: int, fd: int):
    attempts = 0
    while True:
        try:
            headers = {"Range": f"bytes={start}-{end}"}
            r = _session.get(url, headers=headers, stream=True, timeout=90)

            bytes_written = 0
            for chunk in r.iter_content(write_chunk_size):
                bytes_written += _os.pwrite(fd, chunk, start + bytes_written)

            break
        except requests.exceptions.ConnectionError as e:
            attempts += 1
            if attempts >= 3:
                raise e

        time.sleep(0.1 * 2**attempts)


byte_range_prefix = "bytes 0-0/"


def get(args):
    url = args[0]
    path = args[1]

    r = _session.get(url, headers={"Range": "bytes=0-0"}, timeout=90)
    if r.status_code == 416:
        Path(path).write_text("")
        return

    if r.status_code != 206:
        raise RuntimeError(
            f"failed to get file size for `{url}`: status_code={r.status_code} error={r.content}"
        )

    content_range = r.headers.get("Content-Range")
    if content_range is None or not content_range.startswith(byte_range_prefix):
        raise RuntimeError(f"invalid Content-Range header for `{url}`: {content_range}")

    file_size = int(content_range[len(byte_range_prefix) :])
    num_parts = math.ceil(file_size / download_part_size)

    with open(path, "wb") as output_file:
        futures: list[Future] = []

        with ThreadPoolExecutor(max_workers=num_concurrent_downloads) as executor:
            for i in range(num_parts):
                start = i * download_part_size
                end = min(start + download_part_size - 1, file_size - 1)
                futures.append(
                    executor.submit(urlretrieve, url, start, end, output_file.fileno())
                )

        for future in futures:
            future.result()


def get_auth_header() -> str:
    internal_execution_id = _os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if internal_execution_id is not None:
        return f"Latch-Execution-Token {internal_execution_id}"

    token_path = Path.home() / ".latch" / "token"
    if token_path.exists():
        return f"Latch-SDK-Token {token_path.read_text().strip()}"

    raise ValueError("no authentication method found")


def _enforce_trailing_slash(path: str):
    if path[-1] != "/":
        path += "/"
    return path


_session = requests.Session()

_adapter = HTTPAdapter(
    max_retries=Retry(
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        allowed_methods=["GET", "PUT", "POST"],
    ),
    pool_maxsize=100,
    pool_connections=10,
)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)


MAXIMUM_UPLOAD_SIZE = 5 * 2**40  # 5 TiB
MAXIMUM_UPLOAD_PARTS = 10000
MAX_CONCURRENT_CHUNKS = 100
MAX_CONCURRENT_UPLOADS = 100
MAX_CONCURRENT_CALLS = 10

_nucleus_semaphore = Semaphore(MAX_CONCURRENT_CALLS)


class LatchPersistence:
    PROTOCOL = "latch://"

    def __init__(self, default_prefix: Optional[str] = None, data_config=None):
        self._name = "latch"
        self._default_prefix = default_prefix
        default_latch_config = data_config.latch if data_config else LatchConfig.auto()

        latch_endpoint = _os.environ.get("LATCH_AUTHENTICATION_ENDPOINT")
        if latch_endpoint is None:
            latch_endpoint = default_latch_config.endpoint
        if latch_endpoint is None:
            raise ValueError("LATCH_AUTHENTICATION_ENDPOINT must be set")

        self._latch_endpoint = latch_endpoint

        self._default_chunk_size = default_latch_config.upload_chunk_size_bytes
        if self._default_chunk_size is None:
            raise ValueError("S3_UPLOAD_CHUNK_SIZE_BYTES must be set")

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_prefix(self) -> Optional[str]:
        return self._default_prefix

    @staticmethod
    def _split_s3_path_to_key(path: str) -> str:
        """
        :param str path:
        :rtype: str
        """
        url = urlparse(path)
        return url.path

    def exists(self, remote_path: str) -> bool:
        """
        :param str remote_path: remote latch:// path
        :rtype bool: whether the s3 file exists or not
        """
        if not remote_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {remote_path}")

        attempts = 0
        while True:
            try:
                r = _session.post(
                    urljoin(self._latch_endpoint, "/api/object-exists-at-url"),
                    json={
                        "object_url": remote_path,
                        "execution_name": _os.environ.get(
                            "FLYTE_INTERNAL_EXECUTION_ID"
                        ),
                    },
                    timeout=90,
                )
                break
            except requests.exceptions.ConnectionError as e:
                attempts += 1
                if attempts >= 3:
                    raise e
                time.sleep(0.1 * 2**attempts)

        if r.status_code != 200:
            raise ValueError(
                "failed to check if object exists at url `{}`".format(remote_path)
            )

        return r.json()["exists"]

    def download_directory(self, remote_path: str, local_path: str) -> bool:
        """
        :param str remote_path: remote latch:// path
        :param str local_path: directory to copy to
        """

        auth_headers = {"Authorization": get_auth_header()}
        r = _session.post(
            urljoin(self._latch_endpoint, "/ldata/get-signed-urls-recursive"),
            json={
                "path": remote_path,
            },
            headers=auth_headers,
            timeout=90,
        )

        res_data = r.json()
        if r.status_code != 200:
            raise ValueError(f"failed to get presigned urls for `{remote_path}`")

        # todo(aidan, max): write property typed wrappers to validate responses
        key_to_url_map: Dict[str, str] = res_data["data"]["urls"]

        task_tuples = []
        for key, url in key_to_url_map.items():
            local_file_path = Path(local_path).joinpath(key)
            local_file_path.parent.mkdir(parents=True, exist_ok=True)

            task_tuples.append((url, local_file_path))

        pool = ThreadPool(20)
        pool.map(get, task_tuples)
        pool.start()
        pool.wait_completion()
        return True

    def download(self, remote_path: str, local_path: str) -> bool:
        """
        :param str remote_path: remote latch:// path
        :param str local_path: directory to copy to
        """

        auth_headers = {"Authorization": get_auth_header()}
        r = _session.post(
            urljoin(self._latch_endpoint, "/ldata/get-signed-url"),
            json={
                "path": remote_path,
            },
            headers=auth_headers,
            timeout=90,
        )

        res_data = r.json()
        if r.status_code != 200:
            raise ValueError(f"failed to get presigned url for `{remote_path}`")

        url = res_data["data"]["url"]
        get((url, local_path))
        return _os.path.exists(local_path)

    @staticmethod
    def _upload_chunk(file_path: str, chunk_size: int, offset: int, url: str, part_num: int):
        with open(file_path, "rb") as f:
            chunk = _os.pread(f.fileno(), chunk_size, offset)
            r = _session.put(url, data=chunk, timeout=90)
            if r.status_code != 200:
                raise RuntimeError(f"Failed to upload chunk: {r.status_code} {r.text}")
            return {"ETag": r.headers["ETag"], "PartNumber": part_num}

    @staticmethod
    def _upload_chunks(file_path: str, presigned_urls: List[str], chunk_size: int, executor: Optional[ThreadPoolExecutor] = None):
        managed_executor = executor is None
        if managed_executor:
            executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_CHUNKS)

        try:
            futures: List[Future] = []
            for idx, url in enumerate(presigned_urls):
                offset = idx * chunk_size
                futures.append(
                    executor.submit(
                        LatchPersistence._upload_chunk,
                        file_path,
                        chunk_size,
                        offset,
                        url,
                        idx + 1
                    )
                )

            parts = []
            for future in futures:
                parts.append(future.result())
        finally:
            if managed_executor:
                executor.shutdown()

        return sorted(parts, key=lambda x: x["PartNumber"])

    @staticmethod
    def _upload(file_path: str, to_path: str, default_chunk_size: int, endpoint: str, executor: Optional[ThreadPoolExecutor] = None):
        file_size = _os.path.getsize(file_path)
        if file_size > MAXIMUM_UPLOAD_SIZE:
            raise ValueError(
                f"File {file_path} is {file_size} bytes which exceeds the maximum upload size (5TiB)"
            )

        nrof_parts = min(
            MAXIMUM_UPLOAD_PARTS,
            math.ceil(file_size / default_chunk_size),
        )
        chunk_size = max(
            default_chunk_size,
            math.ceil(file_size / MAXIMUM_UPLOAD_PARTS),
        )

        nrof_parts = math.ceil(float(file_size) / chunk_size)
        content_type = mimetypes.guess_type(file_path)[0]
        if content_type is None:
            content_type = "application/octet-stream"

        auth_headers = {"Authorization": get_auth_header()}

        with _nucleus_semaphore:
            r = _session.post(
                urljoin(endpoint, "/ldata/start-upload"),
                json={
                    "path": to_path,
                    "part_count": nrof_parts,
                    "content_type": content_type,
                },
                headers=auth_headers,
                timeout=90,
            )

        res_data = r.json()
        if r.status_code != 200:
            raise ValueError(
                f"failed to get presigned upload urls for `{to_path}`: {res_data['error']}"
            )

        data = res_data["data"]

        if nrof_parts == 0:
            return {"cache": data["version_id"]}

        presigned_urls = data["urls"]
        upload_id = data["upload_id"]

        parts = LatchPersistence._upload_chunks(file_path, presigned_urls, chunk_size, executor)

        with _nucleus_semaphore:
            r = _session.post(
                urljoin(endpoint, "/ldata/end-upload"),
                json={
                    "upload_id": upload_id,
                    "parts": parts,
                    "path": to_path,
                },
                headers=auth_headers,
                timeout=90,
            )

        res_data = r.json()
        if r.status_code != 200:
            raise RuntimeError(
                f"failed to complete upload for `{to_path}`: {res_data['error']}"
            )

        data = res_data["data"]
        return {"cache": data["version_id"]}

    def upload(self, file_path: str, to_path: str):
        """
        :param str file_path:
        :param str to_path:
        """
        return LatchPersistence._upload(
            file_path, to_path, self._default_chunk_size, self._latch_endpoint
        )

    def upload_directory(self, local_path: str, remote_path: str):
        """
        :param str local_path:
        :param str remote_path:
        """
        if remote_path == "latch://":
            remote_path = "latch:///"

        # ensure formatting
        local_path = _enforce_trailing_slash(local_path)
        remote_path = _enforce_trailing_slash(remote_path)

        files_to_upload = [
            _os.path.join(dp, f)
            for dp, __, filenames in _os.walk(local_path)
            for f in filenames
        ]

        cache_accum = bytearray([0] * 32)

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_UPLOADS) as outer_executor:
            futures: List[Future] = []

            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_CHUNKS) as inner_executor:
                for file_path in files_to_upload:
                    relative_name = file_path.replace(local_path, "", 1)
                    if relative_name.startswith("/"):
                        relative_name = relative_name[1:]

                    futures.append(
                        outer_executor.submit(
                            self._upload,
                            file_path,
                            remote_path + relative_name,
                            self._default_chunk_size,
                            self._latch_endpoint,
                            inner_executor
                        )
                    )

                for future in futures:
                    result = future.result()
                    if result is not None and result["cache"] is not None:
                        hash = hashlib.sha256(result["cache"].encode("utf-8")).digest()
                        for i in range(len(cache_accum)):
                            cache_accum[i] ^= hash[i]

        cache = base64.standard_b64encode(bytes(cache_accum)).decode("ascii")
        return {"cache": cache}

    def construct_path(self, add_protocol: bool, add_prefix: bool, *args: str) -> str:
        paths = list(args)  # make type check happy
        if add_prefix and self.default_prefix is not None:
            paths.insert(0, self.default_prefix)
        path = "/".join(paths)
        if add_protocol:
            return f"{self.PROTOCOL}{path}"
        return path

    def get(self, from_path: str, to_path: str, recursive: bool = False):
        if not from_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {from_path}")

        if recursive:
            return self.download_directory(from_path, to_path)

        return self.download(from_path, to_path)

    def put(self, from_path: str, to_path: str, recursive: bool = False):
        if not to_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {to_path}")

        if recursive:
            return self.upload_directory(from_path, to_path)

        return self.upload(from_path, to_path)
