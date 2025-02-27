"""Flows to publish data to an InvenioRDM instance."""

import os
from typing import List, Dict, Any, Optional

import httpx
from prefect import flow, unmapped
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.blocks.system import Secret

from prefect_invenio_rdm.credentials import InvenioRDMCredentials
from prefect_invenio_rdm.models.records import DraftConfig
from prefect_invenio_rdm.models.api import (
    APIResult,
    APIError,
    ErrorType,
)
from prefect_invenio_rdm.tasks import (
    get_access_token,
    get_base_url,
    get_dir_files,
    validate_upload_files,
    create_draft_record,
    delete_draft_record,
    start_draft_file_uploads,
    upload_draft_file,
    commit_draft_file_upload,
    publish_draft_record,
    add_community,
)


@flow(flow_run_name="get-credentials", task_runner=ThreadPoolTaskRunner)
async def get_credentials() -> InvenioRDMCredentials:
    """
    Retrieve credentials used to authenticate with an InvenioRDM instance.

    Returns:
        InvenioRDMCredentials: The credentials.
    """
    access_token: Secret = await get_access_token()
    base_url = await get_base_url()

    return InvenioRDMCredentials(base_url=base_url, token=access_token.get())


@flow(
    name="create-records-dir",
    task_runner=ThreadPoolTaskRunner(),
)
async def create_record_dir(
    directory: str,
    config: DraftConfig,
    file_pattern: str = "*",
    recursive: bool = False,
    auto_publish: bool = False,
    delete_on_failure: bool = False,
    credentials: Optional[InvenioRDMCredentials] = None,
) -> List[APIResult]:
    """
    Creates and publishes a record from a directory.

    Args:
        directory (str): A local directory.
        config (DraftConfig): Draft record configurations.
        file_pattern (str): A regex pattern to match specific files in each directory.
            Defaults to include all files.
        recursive (bool): If `True`, the pattern segment “**” will match any number of
            path segments. Defaults to `False`.
        auto_publish (bool): If `True`, the draft record will be automatically published if
            all files were uploaded successfully. Defaults to `False`.
        delete_on_failure (bool): If `True`, deletes the record if there is an error
            when uploading files or publishing. Defaults to `False`.
        credentials (InvenioRDMCredentials): Credentials used to authenticate with an
            InvenioRDM instance. If not provided will default to using env var credentials.
    Returns:
        APIResult: The result of a successfully created or published record.
    """

    if not directory:
        raise ValueError("No directory provided")

    if not file_pattern:
        raise ValueError("Invalid file pattern")

    if not credentials:
        credentials = await get_credentials()

    dir_files = await get_dir_files(
        directory=directory, pattern=file_pattern, recursive=recursive
    )

    return await create_record_files(
        credentials=credentials,
        files=dir_files,
        config=config,
        delete_on_failure=delete_on_failure,
        auto_publish=auto_publish,
    )


@flow(
    name="create-record-from-files",
    task_runner=ThreadPoolTaskRunner(),
)
async def create_record_files(
    files: List[str],
    config: DraftConfig,
    delete_on_failure: bool = False,
    auto_publish: bool = False,
    credentials: Optional[InvenioRDMCredentials] = None,
) -> APIResult:
    """
    Create a record from local files.

    Args:
        files (List[str]): A list of files to upload.
        config (DraftConfig): Draft record configurations.
        auto_publish (bool): If `True`, the deposition will be automatically published
            if created and all files were uploaded successfully. Defaults to `False`.
        delete_on_failure (bool): If `True`, deletes the record if there is an error
            when uploading files or publishing. Defaults to `False`.
        credentials (InvenioRDMCredentials): Credentials used to authenticate with an
            InvenioRDM instance.
    Returns:
        APIResult: The API result including the create or publish response
            if successful.
    """

    if not files:
        raise ValueError("No files provided")

    await validate_upload_files(files=files)

    if not credentials:
        credentials = await get_credentials()

    result: APIResult = await create_record(
        credentials=credentials, config=config, files=files, auto_publish=auto_publish
    )

    # delete deposition on error
    if delete_on_failure and not result.successful and result.api_response:
        record_id = result.api_response["id"]
        await delete_draft_record(credentials=credentials, record_id=record_id)

    return result


@flow(name="create-record", task_runner=ThreadPoolTaskRunner())
async def create_record(
    credentials: InvenioRDMCredentials,
    config: DraftConfig,
    files: List[str],
    auto_publish: bool = False,
) -> APIResult:
    """
    Create a record from local files.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate with an
            InvenioRDM instance.
        files (List[str]): A list of files to upload.
        config (DraftConfig): Draft record configurations.
        auto_publish (bool): If `True`, the deposition will be automatically published
            if created and all files were uploaded successfully. Defaults to `False`.

    Returns:
        APIResult: The API result including the create or publish response
            if successful.
    """
    # create a draft record
    try:
        draft_response: Dict[str, Any] = await create_draft_record(
            credentials=credentials, config=config
        )
    except httpx.HTTPError as error:
        return APIResult(
            successful=False,
            error=APIError(type=ErrorType.CREATE, error_message=str(error)),
        )

    record_id: int = draft_response["id"]

    if config.community_id:
        try:
            await add_community(
                credentials=credentials,
                record_id=record_id,
                community_id=config.community_id,
            )
        except httpx.HTTPError as error:
            return APIResult(
                successful=False,
                api_response=draft_response,
                error=APIError(type=ErrorType.UPDATE, error_message=str(error)),
            )

    # upload draft files
    try:
        await upload_draft_files(
            credentials=credentials, record_id=record_id, files=files
        )
    except httpx.HTTPError as error:
        return APIResult(
            successful=False,
            api_response=draft_response,
            error=APIError(type=ErrorType.FILE_UPLOAD, error_message=str(error)),
        )

    # publish draft record
    if auto_publish:
        try:
            publish_response = await publish_draft_record(
                credentials=credentials,
                record_id=record_id,
            )
            return APIResult(successful=True, api_response=publish_response)
        except httpx.HTTPError as error:
            return APIResult(
                successful=False,
                api_response=draft_response,
                error=APIError(type=ErrorType.PUBLISH, error_message=str(error)),
            )

    return APIResult(successful=True, api_response=draft_response)


@flow(
    flow_run_name="upload-draft-{record_id}-files", task_runner=ThreadPoolTaskRunner()
)
async def upload_draft_files(
    credentials: InvenioRDMCredentials,
    record_id: int,
    files: List[str],
) -> None:
    """
    Uploads a list of files to a draft record.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate with an
            InvenioRDM instance.
        record_id (int): Identifier of the record.
        files (List[str]): A list of files.

    Returns:
        None
    """

    # start file upload process
    file_names = [os.path.basename(file) for file in files]

    await start_draft_file_uploads(
        credentials=credentials,
        record_id=record_id,
        file_keys=[{"key": file_name} for file_name in file_names],
    )

    # upload files
    upload_draft_file.map(
        credentials=unmapped(credentials),
        record_id=unmapped(record_id),
        file_name=file_names,
        file=files,
    ).result(raise_on_failure=True)

    # commit uploaded files
    commit_draft_file_upload.map(
        credentials=unmapped(credentials),
        record_id=unmapped(record_id),
        file_name=file_names,
    ).result(raise_on_failure=True)
