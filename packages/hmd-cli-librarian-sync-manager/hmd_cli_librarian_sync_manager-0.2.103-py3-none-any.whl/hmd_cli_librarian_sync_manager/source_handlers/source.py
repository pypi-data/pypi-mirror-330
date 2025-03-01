import logging
import os
from json import dumps
from pathlib import Path
from tempfile import gettempdir
from typing import Dict
import jwt
import time
from cement import CaughtSignal
from hmd_lang_librarian_sync.hmd_lang_librarian_sync_client import (
    File,
    HmdLangLibrarianSyncClient,
)
from hmd_lib_librarian_client.hmd_lib_librarian_client import HmdLibrarianClient
from hmd_lib_auth.hmd_lib_auth import (
    okta_service_account_token,
    okta_service_account_token_by_secret_name,
)
from hmd_lang_librarian_sync.file import File
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)
OKTA_SECRET_NAME = "okta-agent-service"


def check_token_exp(auth_token: str):
    payload = jwt.decode(auth_token, options={"verify_signature": False})
    logger.info("Checking auth token expiration..")
    if payload["exp"] - time.time() <= 0:
        logger.info(f"Refreshing auth token..")
        if os.environ.get("HMD_ENTITY_NID"):
            auth_token = okta_service_account_token_by_secret_name(OKTA_SECRET_NAME)
        else:
            auth_token = okta_service_account_token(
                os.environ["HMD_AGENT_CLIENT_ID"],
                os.environ["HMD_AGENT_CLIENT_SECRET"],
                okta_host_url=os.environ["HMD_SERVICES_ISSUER"],
            )
    else:
        auth_token = None
    return auth_token


class Source:
    def __init__(
        self,
        config: Dict,
        librarian_sync_client: HmdLangLibrarianSyncClient,
        librarian_client: HmdLibrarianClient,
        hmd_home: Path,
        hmd_repo_home: Path,
        timestamp_reverse: bool,
    ):
        self.attempts = 0
        self._librarian_sync_client = librarian_sync_client
        self._hmd_home = hmd_home
        self._hmd_repo_home = hmd_repo_home
        self._librarian_client = librarian_client
        self.name: str = config["name"]
        self.type = config.get("type", "default")
        if self.type == "manifest":
            self.manifest_file_name = config.get(
                "manifest_file_name", "hmd-librarian-manifest.json"
            )
        self.delete_when_successful: bool = config.get("delete_when_successful", False)
        self.path: Path = Path(os.path.expandvars(config["path"])).expanduser()
        self.is_enabled: bool = config.get("enabled", True)
        direction: str = config.get("direction", "push")
        self.is_push = direction == "push"
        self.is_pull = direction == "pull"
        self.stop_requested = False
        self.max_part_size = config.get("max_part_size", None)
        self.number_of_threads = config.get("number_of_threads", None)
        self.librarian = self._librarian_client.base_client.base_url
        self.archive_root = None
        self.attempt_max = int(config.get("attempt_max", "3"))
        self.timestamp_reverse: bool = timestamp_reverse
        if "archive_root" in config:
            self.archive_root: Path = Path(
                os.path.expandvars(config["archive_root"])
            ).expanduser()
        self.enable_checksum = config.get("enable_checksum", False)

    def put_file_callback(self, data):
        logger.info(
            f"{self.name}: Parts: {data['parts_complete']}/{data['total_parts']}; {data['parts_percent']:2.2%}"
        )
        logger.info(
            f"{self.name}: Bytes: {data['bytes_complete']}/{data['total_bytes']}; {data['bytes_percent']:2.2%}"
        )
        logger.info(f"{self.name}: {data['parts'][:5]}")

    def update_modified(self, file: File):
        logger.info(f"{self.name}: BEGIN Update modified for {file.content_path}")
        file.librarians_synced[self.librarian] = file.modified
        file.schedule_upload = 1
        file = self._librarian_sync_client.upsert_file_hmd_lang_librarian_sync(file)
        logger.info(f"{self.name}: END   Update modified for {file.content_path}")

    def update_upload_failed(self, file: File):
        logger.info(f"{self.name}: BEGIN Update failed for {file.content_path}")
        file.schedule_upload = 2
        file = self._librarian_sync_client.upsert_file_hmd_lang_librarian_sync(file)
        logger.info(f"{self.name}: END   Update failed for {file.content_path}")

    def handle_file_delete(self, file: File):
        if self.delete_when_successful:
            Path(file.path).unlink()

    def archive_file(self, file: File):
        # TODO implement archive

        logger.info(f"{self.name}: BEGIN Archive file {file.content_path}")
        file_path = Path(file.path)
        if self.archive_root and file_path.exists():
            pass
            # logger.info(f"{self.name}: {ile.source_name}")
            # sources = list(
            #     filter(lambda s: s["name"] == file.source_name, self._config["sources"])
            # )
            # if len(sources) == 1:
            #     source = sources[0]
            #     logger.info(source)
            #     if source:
            #         source_path = Path(os.path.expandvars(source["path"]))
            #         source_trailer = file_path.relative_to(source_path)
            #         archive_path = self.archive_root / source_trailer
            #         logger.info(f"Moving file from {file_path} to {archive_path}")
            #         archive_path.parent.mkdir(parents=True, exist_ok=True)
            #         file_path.replace(archive_path)
        else:
            logger.info(f"{self.name}: Archiving is currently disabled")
        logger.info(f"{self.name}: END   Archive file {file.content_path}")

    def put_file(self, file: File):
        logger.info(f"{self.name}: BEGIN Put file {file.content_path}")
        while not self.attempt_max_reached():
            self.attempts += 1
            try:
                kwargs = {
                    "content_path": file.content_path,
                    "file_name": file.path,
                    "content_item_type": file.content_item_type,
                    "status_callback": self.put_file_callback,
                }
                if self.max_part_size:
                    kwargs["max_part_size"] = self.max_part_size
                if self.number_of_threads:
                    kwargs["number_of_threads"] = self.number_of_threads
                if file.checksum is not None:
                    kwargs["checksum"] = file.checksum

                file_upload = self._librarian_client.put_file(**kwargs)
                if (
                    os.environ.get("HMD_ENTITY_NID")
                    and os.path.basename(kwargs["file_name"]) == self.manifest_file_name
                ):
                    entity = self._librarian_client.search_librarian(
                        {
                            "attribute": "hmd_lang_librarian.content_item.content_item_path",
                            "operator": "=",
                            "value": file_upload["content_item_path"],
                        }
                    )
                    manifest_upload = {
                        "name": "hmd_lang_librarian.content_item",
                        "id": entity[0]["identifier"],
                    }
                    path = f"{gettempdir()}/entity.txt"
                    with open(path, "w") as output_param:
                        output_param.write(dumps(manifest_upload))
                self.update_modified(file)
                self.archive_file(file)
                if self.type != "manifest":
                    self.handle_file_delete(file)
                break
            except CaughtSignal as cs:
                logger.error(
                    f"{self.name}: stop requested while putting file", exc_info=cs
                )
                raise cs
            except AssertionError as ae:
                message = f"{self.name}: error putting file: {he.response.json()}"
                logger.error(message, exc_info=ae)
                self.update_upload_failed(file)
                break
            except HTTPError as he:
                message = f"{self.name}: error putting file: {he.response.json()}"
                logger.error(message, exc_info=he)
                self.update_upload_failed(file)
            except BaseException as e:
                if self._librarian_client.base_client.auth_token:
                    auth_token = check_token_exp(
                        self._librarian_client.base_client.auth_token
                    )
                    if auth_token:
                        self._librarian_client = HmdLibrarianClient(
                            base_url=self.librarian, auth_token=auth_token
                        )
                        logger.info(f"Auth token refreshed for {self.librarian}")
                    else:
                        logger.error(f"{self.name}: error putting file", exc_info=e)
                        self.update_upload_failed(file)
                else:
                    logger.error(f"{self.name}: error putting file", exc_info=e)
                    self.update_upload_failed(file)
            finally:
                logger.info(f"{self.name}: END   Put file {file.content_path}")

    def update_librarians_synced(self, file: File):
        if file.librarians_synced is None:
            file.librarians_synced = dict()
        if self.librarian not in file.librarians_synced.keys():
            file.librarians_synced[self.librarian] = ""
            self._librarian_sync_client.upsert_file_hmd_lang_librarian_sync(file)

        return file

    def _is_present_and_not_synced(self, file: File):
        file_path = Path(file.path)
        if not file_path.exists():
            logger.info(
                f"{self.name}: SKIP  File not found in filesystem, skipping {file.path}"
            )
            return False
        elif file_path.stat().st_size == 0:
            logger.info(f"{self.name}: SKIP  File is empty, skipping {file.path}")
            return False
        if file.schedule_upload is not None:
            return (
                file.modified != file.librarians_synced[self.librarian]
                and file.schedule_upload < 1
            )
        else:
            return file.modified != file.librarians_synced[self.librarian]

    def get_queued_files(self):
        logger.info(f"{self.name}: Getting queued files")
        query = {
            "and": [
                {"attribute": "source_name", "operator": "=", "value": self.name},
                {"attribute": "schedule_upload", "operator": "<", "value": 1},
            ]
        }
        files = self._librarian_sync_client.search_file_hmd_lang_librarian_sync(query)
        files = map(self.update_librarians_synced, files)
        files = list(filter(self._is_present_and_not_synced, files))
        # Sort based on modified time, default is older files first
        files = sorted(
            files,
            key=lambda f: f.modified,
            reverse=self.timestamp_reverse,
        )
        # Sort based on priority
        files = sorted(files, key=lambda f: f.upload_priority, reverse=True)
        return files

    def sync(self, file: File):
        try:
            self.attempts = 0
            logger.info(f"{self.name}: BEGIN sync")
            if self.stop_requested:
                logger.info(f"{self.name}: Stop requested, skipping sync")

            else:
                if self.is_push:
                    if self.stop_requested:
                        logger.info(
                            f"{self.name}: Stop requested, skpping remaining queued files"
                        )
                        return
                    logger.info(f"BEGIN put_file: {file.path}")
                    logger.info(f"{self.name}: put file progress: {file.path}")
                    self.put_file(file)
                    logger.info(f"END put_file: {file.path}")
                else:
                    logger.info(f"{self.name}: Pulling")
                    self.pull_files()
        finally:
            logger.info(f"{self.name}: END   sync")

    def pull_files(self):
        raise NotImplementedError()

    def is_complete(self):
        if self.is_push:
            return 0 == len(self.get_queued_files())
        raise Exception("Invalid configuration, can't pull standard source")

    def attempt_max_reached(self):
        return self.attempts > self.attempt_max

    def stop(self):
        logger.info(f"{self.name}: Requesting stop")
        self.stop_requested = True
