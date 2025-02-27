"""Tasks to publish data to an InvenioRDMCredentials instance."""

import os
import glob
from typing import Dict, Any, List

from prefect import task, get_run_logger
from prefect.blocks.system import Secret
from prefect.tasks import exponential_backoff
from prefect.concurrency.asyncio import rate_limit

from prefect_invenio_rdm.credentials import InvenioRDMCredentials

from prefect_invenio_rdm.models.records import DraftConfig
from prefect_invenio_rdm.constants import (
    INVENIO_RDM_ACCESS_TOKEN,
    INVENIO_RDM_BASE_URL,
    INVENIO_RDM_API_TAG,
    ACCESS_TOKEN_BLOCK,
)


@task
async def get_access_token() -> Secret:
    """
    Retrieves an access token and stores it in a Prefect `Secret` block.

    Raises:
        ValueError: If the access token environment variable is not found.

    Returns:
        Secret: The access token secret.
    """

    access_token = os.getenv(INVENIO_RDM_ACCESS_TOKEN)

    if not access_token:
        raise ValueError(
            f"Environment variable '{INVENIO_RDM_ACCESS_TOKEN}' is not set."
        )

    # Create or update the Secret block
    secret = Secret(value=access_token)
    await secret.save(name=ACCESS_TOKEN_BLOCK, overwrite=True)

    return secret


@task
async def get_base_url() -> str:
    """
    Retrieves the InvenioRDM instance base URL.

    Raises:
        ValueError: If the base URL environment variable is not found.

    Returns:
        str: An InvenioRDM instance base URL.
    """

    base_url = os.getenv(INVENIO_RDM_BASE_URL)

    if not base_url:
        raise ValueError(f"Environment variable '{INVENIO_RDM_BASE_URL}' is not set.")

    return base_url


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def create_draft_record(
    credentials: InvenioRDMCredentials,
    config: DraftConfig,
) -> Dict[str, Any]:
    """
    Creates a draft record.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        config (DraftConfig): Draft record configurations.

    Raises:
        HTTPStatusError: If the request is unsuccessful.

    Returns:
        Dict[str, Any]: The API response as JSON.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    logger = get_run_logger()

    json = config.to_dict()
    logger.debug(json)

    async with credentials.get_client() as client:
        response = await client.post("records", json=json)
        response.raise_for_status()

    return response.json()


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def publish_draft_record(
    credentials: InvenioRDMCredentials,
    record_id: int,
) -> Dict[str, Any]:
    """
    Publish a draft record.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        record_id (int): Identifier of the record,

    Raises:
        HTTPStatusError: If the request fails.

    Returns:
        Dict[str, Any]: The API response as JSON.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    get_run_logger().info("Publishing draft record, ID: %d", record_id)

    async with credentials.get_client() as client:
        response = await client.post(f"records/{record_id}/draft/actions/publish")
        response.raise_for_status()

    return response.json()


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def delete_draft_record(
    credentials: InvenioRDMCredentials,
    record_id: int,
) -> None:
    """
    Deletes a draft record.

    Note:
        Deleting a draft for an unpublished record will remove the draft
            and associated files from the system.
        Deleting a draft for a published record will remove the draft but
            not the published record.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        record_id (int): Identifier of the record,

    Raises:
        HTTPStatusError: If the request fails.

    Returns:
        None.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    get_run_logger().info("Deleting draft record, ID: %d", record_id)

    async with credentials.get_client() as client:
        response = await client.delete(f"records/{record_id}/draft")
        response.raise_for_status()


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def start_draft_file_uploads(
    credentials: InvenioRDMCredentials,
    record_id: int,
    file_keys: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Start draft file upload.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        record_id (int): Identifier of the record,
        file_keys (List[[Dict[str, Any]]]): A list of file keys describing
            the file uploads to be initialized.

    Raises:
        HTTPStatusError: If the request fails.

    Returns:
        Dict[str, Any]: The API response as JSON.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    if not file_keys:
        raise ValueError("No file keys provided")

    get_run_logger().info(
        "Starting draft uploads for the following files: %s", file_keys
    )

    async with credentials.get_client() as client:
        response = await client.post(f"records/{record_id}/draft/files", json=file_keys)
        response.raise_for_status()

    return response.json()


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def upload_draft_file(
    credentials: InvenioRDMCredentials,
    record_id: int,
    file_name: str,
    file: str,
) -> Dict[str, Any]:
    """
    Upload a draft file's content.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        record_id (int): Identifier of the record,
        file_name (str): Name of the file.
        file (str): The file path.

    Raises:
        HTTPStatusError: If the request fails.
        IOError: If the file is not found or unable to be read.

    Returns:
        Dict[str, Any]: The API response as JSON.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    if not file_name:
        raise ValueError("Invalid file name")

    if not file:
        raise ValueError("Invalid file")

    if not os.path.exists(file):
        raise ValueError(f"File does not exist: {file}")

    get_run_logger().info(
        "Uploading file '%s', size: %dMB",
        file,
        os.path.getsize(file) / (1024 * 1024),
    )

    # Must use a synchronous client when uploading files
    with credentials.get_sync_client() as client:
        with open(file, "rb") as fp:
            response = client.put(
                f"records/{record_id}/draft/files/{file_name}/content",
                data=fp,
            )
            response.raise_for_status()

    return response.json()


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def commit_draft_file_upload(
    credentials: InvenioRDMCredentials,
    record_id: int,
    file_name: str,
) -> Dict[str, Any]:
    """
    Complete a draft file upload.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        record_id (int): Identifier of the record,
        file_name (str): Name of the file.

    Raises:
        HTTPStatusError: If the request fails.

    Returns:
        Dict[str, Any]: The API response as JSON.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    if not file_name:
        raise ValueError("Invalid file name")

    get_run_logger().info(
        "Commiting uploaded file '%s' for draft record %s", file_name, record_id
    )

    async with credentials.get_client() as client:
        response = await client.post(
            f"records/{record_id}/draft/files/{file_name}/commit"
        )
        response.raise_for_status()

    return response.json()


@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_jitter_factor=0.5,
    tags=[INVENIO_RDM_API_TAG],
)
async def add_community(
    credentials: InvenioRDMCredentials,
    record_id: int,
    community_id: str,
) -> Dict[str, Any]:
    """
    Associates the record with a community in which it will appear.

    Args:
        credentials (InvenioRDMCredentials): Credentials used to authenticate
            with an InvenioRDM instance.
        record_id (int): Identifier of the record,
        community_id (str): The ID of the community.

    Raises:
        HTTPStatusError: If the request fails.

    Returns:
        Dict[str, Any]: The API response as JSON.
    """
    await rate_limit("rate-limit:invenio-rdm-api")

    if not record_id:
        raise ValueError("Invalid record ID")

    if not community_id:
        raise ValueError("Invalid community ID")

    async with credentials.get_client() as client:
        response = await client.put(
            f"/records/{record_id}/draft/review",
            json={
                "receiver": {"community": community_id},
                "type": "community-submission",
            },
        )
        response.raise_for_status()

    return response.json()


@task
async def validate_upload_files(files: List[str]) -> None:
    """
    Validates that all files exist locally.

    Args:
        files (List[str]): A list of local files.

    Returns:
        bool: `True` if all the files exists, otherwise `False`.
    """
    if not files:
        raise ValueError("The list of file paths cannot be empty")

    get_run_logger().debug("Files:%s", files)

    if not [os.path.exists(file) for file in files].count(True) == len(files):
        raise ValueError("Cannot find one or more files in the list of paths provided")


@task
async def get_dir_files(
    directory: str, pattern: str, recursive: bool = False
) -> List[str]:
    """
    Retrieves all matching files for each local directory.

    Args:
        directory (str): A directory.
        pattern (str): The glob pattern to match file names against.
        recursive (bool): If `True`, will match any files in the directory and subdirectories.
            Defaults to `False`.

    Returns:
        List[str]: A list of files that match the pattern in the given directory.
    """
    logger = get_run_logger()

    logger.debug("Directory:%s", directory)
    logger.debug("File pattern: %s, recursive: %s", pattern, recursive)

    if not os.path.exists(directory):
        raise ValueError(f"The directory '{directory}' does not exist.")

    search_pattern = os.path.join(directory, pattern)
    matching_files = glob.glob(search_pattern, recursive=recursive)

    # Filter out directories, keeping only files
    files = [file for file in matching_files if os.path.isfile(file)]

    logger.info("Matching files from directory: %s", files)

    return files
