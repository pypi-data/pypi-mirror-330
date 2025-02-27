"""Tests for the flows.py module"""

# pylint: disable=redefined-outer-name, too-many-locals, too-many-arguments
from typing import Generator, List, Dict, Any, Optional
from unittest.mock import Mock, MagicMock, AsyncMock, call

import pytest
import httpx

from prefect import unmapped
from prefect.blocks.system import Secret
from prefect.testing.utilities import prefect_test_harness
from prefect.logging import disable_run_logger

from prefect_invenio_rdm import flows
from prefect_invenio_rdm.credentials import InvenioRDMCredentials
from prefect_invenio_rdm.models.api import APIResult, APIError, ErrorType
from prefect_invenio_rdm.models.records import DraftConfig, Access


@pytest.fixture(scope="session", autouse=True)
def prefect_db() -> Generator[None, Any, None]:
    """
    Sets up test harness for temporary DB during test runs.
    """
    with prefect_test_harness():
        yield


@pytest.fixture(scope="session", autouse=True)
def disabled_loggers() -> Generator[None, Any, None]:
    """
    Disable Prefect loggers during test runs.
    """
    with disable_run_logger():
        yield


@pytest.fixture
def credentials() -> InvenioRDMCredentials:
    """
    Creates a mock instance of InvenioRDMCredentials.
    """
    return InvenioRDMCredentials(
        base_url="https://example.org/api/",
        token="testing_token",
    )


@pytest.fixture
def access_token_secret() -> Secret:
    """
    Creates a mock instance of a Prefect Secret
    """
    return Secret(value="test access token")


@pytest.fixture
def dir_files() -> List[str]:
    """
    Creates a mock list of directory files.
    """
    return ["files/file.txt", "files/image.png"]


@pytest.fixture
def config() -> DraftConfig:
    """
    Creates a mock of a draft record config.
    """
    return DraftConfig(
        record_access=Access.PUBLIC,
        files_access=Access.PUBLIC,
        files_enabled=True,
        metadata={"title": "test title"},
        custom_fields={"custom_field": "custom field value"},
        community_id="test community id",
    )


@pytest.fixture
def create_response() -> Dict[str, Any]:
    """
    Creates a mock API response for a create record request.
    """
    return {"id": 1, "creators": []}


@pytest.fixture
def publish_response() -> Dict[str, Any]:
    """
    Creates a mock API response for a publish record request.
    """
    return {"id": 1, "creators": [], "is_published": True}


def mock_call(
    mocker: Any,
    method: str,
    return_value: Optional[Any] = None,
    side_effect: Optional[Any] = None,
) -> Mock:
    """
    Mocks a Prefect Task or Flow.
    """
    mock = AsyncMock()
    mocker.patch(f"prefect_invenio_rdm.flows.{method}", mock)

    mock.return_value = return_value

    if side_effect:
        mock.side_effect = side_effect

    return mock


async def test_get_credentials_successful(
    mocker: any, access_token_secret: Secret, credentials: InvenioRDMCredentials
) -> None:
    """
    Tests that get_credentials() successfully returns a
    instance of InvenioRDMCredentials.
    """

    mock_get_access_token = mock_call(
        mocker=mocker, method="get_access_token", return_value=access_token_secret
    )
    mock_get_base_url = mock_call(
        mocker=mocker, method="get_base_url", return_value="test base url"
    )

    mock_credentials = Mock(return_value=credentials)
    mocker.patch("prefect_invenio_rdm.flows.InvenioRDMCredentials", mock_credentials)

    credentials: InvenioRDMCredentials = await flows.get_credentials()

    mock_get_access_token.assert_called_once()
    mock_get_base_url.assert_called_once()
    mock_credentials.assert_called_once_with(
        base_url="test base url", token=access_token_secret.get()
    )
    assert credentials == credentials


async def test_create_record_dir_validates_args(config: DraftConfig) -> None:
    """
    Tests that create_record_dir() successfully validates all provided.
    arguments.
    """

    with pytest.raises(ValueError, match="No directory provided"):
        await flows.create_record_dir(directory="", config=config)

    with pytest.raises(ValueError, match="Invalid file pattern"):
        await flows.create_record_dir(
            directory="files/", config=config, file_pattern=""
        )


async def test_create_record_dir_successful(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    create_response: Dict[str, Any],
    credentials: InvenioRDMCredentials,
) -> None:
    """
    Tests that create_record_dir() successfully creates a record from
    a directory and uploads all matching files.
    """

    mock_get_credentials = mock_call(
        mocker=mocker, method="get_credentials", return_value=credentials
    )
    mock_get_dir_files = mock_call(
        mocker=mocker, method="get_dir_files", return_value=dir_files
    )
    expected_result = APIResult(successful=True, api_response=create_response)
    mock_create_record_files = mock_call(
        mocker=mocker, method="create_record_files", return_value=expected_result
    )

    result = await flows.create_record_dir(
        directory="files/",
        config=config,
        file_pattern="*",
        recursive=True,
        delete_on_failure=False,
        auto_publish=True,
    )

    mock_get_dir_files.assert_called_once_with(
        directory="files/", pattern="*", recursive=True
    )

    mock_get_credentials.assert_called_once()

    assert mock_create_record_files.call_args_list == [
        call(
            credentials=credentials,
            files=dir_files,
            config=config,
            delete_on_failure=False,
            auto_publish=True,
        ),
    ]

    assert result == expected_result


async def test_create_record_files_validates_args(
    mocker: any, config: DraftConfig
) -> None:
    """
    Tests that create_record_files() successfully validates all provided
    arguments.
    """

    mock_validate_upload_files = mock_call(
        mocker=mocker, method="validate_upload_files", side_effect=ValueError("error!")
    )

    with pytest.raises(ValueError, match="No files provided"):
        await flows.create_record_files(files=[], config=config)

    with pytest.raises(ValueError):
        await flows.create_record_files(files=["files/file.txt"], config=config)

        mock_validate_upload_files.assert_called_once_with(files=["files/file.txt"])


async def test_create_record_files_delete_on_failure(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
) -> None:
    """
    Tests that create_record_files() deletes the created record
    when there are errors and the delete on failure option is enabled.
    """

    mock_validate_upload_files = mock_call(
        mocker=mocker, method="validate_upload_files", return_value=None
    )
    mock_get_credentials = mock_call(
        mocker=mocker, method="get_credentials", return_value=credentials
    )

    create_result = APIResult(
        successful=False,
        api_response={"id": "test record id"},
        errors=[APIError(type=ErrorType.CREATE, error_message="create error")],
    )
    mock_create_record = mock_call(
        mocker=mocker,
        method="create_record",
        return_value=create_result,
    )
    mock_delete_draft_record = mock_call(
        mocker=mocker,
        method="delete_draft_record",
        return_value=None,
    )

    result = await flows.create_record_files(
        files=dir_files, config=config, auto_publish=True, delete_on_failure=True
    )

    mock_validate_upload_files.assert_called_once_with(files=dir_files)
    mock_get_credentials.assert_called_once()
    mock_create_record.assert_called_once_with(
        credentials=credentials, config=config, files=dir_files, auto_publish=True
    )
    mock_delete_draft_record.assert_called_once_with(
        credentials=credentials, record_id="test record id"
    )

    assert result == create_result


async def test_create_record_create_error(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
) -> None:
    """
    Tests that create_record() returns the expected result when
    creating a record fails.
    """
    mock_create_draft_record = mock_call(
        mocker=mocker,
        method="create_draft_record",
        side_effect=httpx.HTTPError("create error!"),
    )
    mock_add_community = mock_call(
        mocker=mocker,
        method="add_community",
        return_value=None,
    )
    mock_upload_draft_files = mock_call(
        mocker=mocker,
        method="upload_draft_files",
        return_value=None,
    )
    mock_publish_draft_record = mock_call(
        mocker=mocker, method="publish_draft_record", return_value=None
    )

    result = await flows.create_record(
        credentials=credentials, files=dir_files, config=config, auto_publish=True
    )

    mock_create_draft_record.assert_called_once_with(
        credentials=credentials, config=config
    )

    mock_add_community.assert_not_called()
    mock_upload_draft_files.assert_not_called()
    mock_publish_draft_record.assert_not_called()

    assert result == APIResult(
        successful=False,
        error=APIError(type=ErrorType.CREATE, error_message="create error!"),
    )


async def test_create_record_add_community_error(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
    create_response: Dict[str, Any],
) -> None:
    """
    Tests that create_record() returns the expected result when
    adding a community fails.
    """
    mock_create_draft_record = mock_call(
        mocker=mocker, method="create_draft_record", return_value=create_response
    )
    mock_add_community = mock_call(
        mocker=mocker,
        method="add_community",
        side_effect=httpx.HTTPError("add community error!"),
    )
    mock_upload_draft_files = mock_call(
        mocker=mocker,
        method="upload_draft_files",
        return_value=None,
    )
    mock_publish_draft_record = mock_call(
        mocker=mocker, method="publish_draft_record", return_value=None
    )

    result = await flows.create_record(
        credentials=credentials, files=dir_files, config=config, auto_publish=True
    )

    mock_create_draft_record.assert_called_once_with(
        credentials=credentials, config=config
    )
    mock_add_community.assert_called_once_with(
        credentials=credentials, record_id=1, community_id="test community id"
    )
    mock_upload_draft_files.assert_not_called()
    mock_publish_draft_record.assert_not_called()

    assert result == APIResult(
        successful=False,
        api_response=create_response,
        error=APIError(type=ErrorType.UPDATE, error_message="add community error!"),
    )


async def test_create_record_upload_files_error(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
    create_response: Dict[str, Any],
) -> None:
    """
    Tests that create_record() returns the expected result when
    uploading files fail.
    """
    mock_create_draft_record = mock_call(
        mocker=mocker, method="create_draft_record", return_value=create_response
    )
    mock_add_community = mock_call(
        mocker=mocker, method="add_community", return_value=None
    )
    mock_upload_draft_files = mock_call(
        mocker=mocker,
        method="upload_draft_files",
        side_effect=httpx.HTTPError("upload files error!"),
    )
    mock_publish_draft_record = mock_call(
        mocker=mocker, method="publish_draft_record", return_value=None
    )

    result = await flows.create_record(
        credentials=credentials, files=dir_files, config=config, auto_publish=True
    )

    mock_create_draft_record.assert_called_once_with(
        credentials=credentials, config=config
    )
    mock_add_community.assert_called_once_with(
        credentials=credentials, record_id=1, community_id="test community id"
    )
    mock_upload_draft_files.assert_called_once_with(
        credentials=credentials, record_id=1, files=dir_files
    )
    mock_publish_draft_record.assert_not_called()

    assert result == APIResult(
        successful=False,
        api_response=create_response,
        error=APIError(type=ErrorType.FILE_UPLOAD, error_message="upload files error!"),
    )


async def test_create_record_publish_error(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
    create_response: Dict[str, Any],
) -> None:
    """
    Tests that create_record() returns the expected result when
    publishing a record fails.
    """
    mock_create_draft_record = mock_call(
        mocker=mocker, method="create_draft_record", return_value=create_response
    )
    mock_add_community = mock_call(
        mocker=mocker, method="add_community", return_value=None
    )
    mock_upload_draft_files = mock_call(
        mocker=mocker, method="upload_draft_files", return_value=None
    )
    mock_publish_draft_record = mock_call(
        mocker=mocker,
        method="publish_draft_record",
        side_effect=httpx.HTTPError("publish error!"),
    )

    result = await flows.create_record(
        credentials=credentials, files=dir_files, config=config, auto_publish=True
    )

    mock_create_draft_record.assert_called_once_with(
        credentials=credentials, config=config
    )
    mock_add_community.assert_called_once_with(
        credentials=credentials, record_id=1, community_id="test community id"
    )
    mock_upload_draft_files.assert_called_once_with(
        credentials=credentials, record_id=1, files=dir_files
    )
    mock_publish_draft_record.assert_called_once_with(
        credentials=credentials, record_id=1
    )

    assert result == APIResult(
        successful=False,
        api_response=create_response,
        error=APIError(type=ErrorType.PUBLISH, error_message="publish error!"),
    )


async def test_create_record_publish_successful(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
    create_response: Dict[str, Any],
    publish_response: Dict[str, Any],
) -> None:
    """
    Tests that create_record() succesfully publishes a record when
    the auto publish option is enabled.
    """
    mock_create_draft_record = mock_call(
        mocker=mocker, method="create_draft_record", return_value=create_response
    )
    mock_add_community = mock_call(
        mocker=mocker, method="add_community", return_value=None
    )
    mock_upload_draft_files = mock_call(
        mocker=mocker, method="upload_draft_files", return_value=None
    )
    mock_publish_draft_record = mock_call(
        mocker=mocker, method="publish_draft_record", return_value=publish_response
    )

    result = await flows.create_record(
        credentials=credentials, files=dir_files, config=config, auto_publish=True
    )

    mock_create_draft_record.assert_called_once_with(
        credentials=credentials, config=config
    )
    mock_add_community.assert_called_once_with(
        credentials=credentials, record_id=1, community_id="test community id"
    )
    mock_upload_draft_files.assert_called_once_with(
        credentials=credentials, record_id=1, files=dir_files
    )
    mock_publish_draft_record.assert_called_once_with(
        credentials=credentials, record_id=1
    )

    assert result == APIResult(successful=True, api_response=publish_response)


async def test_create_record_successful(
    mocker: Any,
    dir_files: List[str],
    config: DraftConfig,
    credentials: InvenioRDMCredentials,
    create_response: Dict[str, Any],
) -> None:
    """
    Tests that create_record() succesfully creates a record.
    """
    mock_create_draft_record = mock_call(
        mocker=mocker, method="create_draft_record", return_value=create_response
    )
    mock_add_community = mock_call(
        mocker=mocker, method="add_community", return_value=None
    )
    mock_upload_draft_files = mock_call(
        mocker=mocker, method="upload_draft_files", return_value=None
    )
    mock_publish_draft_record = mock_call(
        mocker=mocker, method="publish_draft_record", return_value=None
    )

    result = await flows.create_record(
        credentials=credentials, files=dir_files, config=config, auto_publish=False
    )

    mock_create_draft_record.assert_called_once_with(
        credentials=credentials, config=config
    )
    mock_add_community.assert_called_once_with(
        credentials=credentials, record_id=1, community_id="test community id"
    )
    mock_upload_draft_files.assert_called_once_with(
        credentials=credentials, record_id=1, files=dir_files
    )
    mock_publish_draft_record.assert_not_called()

    assert result == APIResult(successful=True, api_response=create_response)


async def test_upload_draft_files_successful(
    mocker: Any, credentials: InvenioRDMCredentials, dir_files: List[str]
) -> None:
    """
    Tests that upload_draft_files() successfully uploads
    all of the files.
    """

    mock_start_draft_file_uploads = mock_call(
        mocker=mocker, method="start_draft_file_uploads", return_value=None
    )

    mock_upload_draft_file = Mock(return_value=None)
    mock_upload_draft_file.map.result.return_value = None
    mocker.patch("prefect_invenio_rdm.flows.upload_draft_file", mock_upload_draft_file)

    mock_commit_draft_file_upload = Mock(return_value=None)
    mock_commit_draft_file_upload.map.result.return_value = None
    mocker.patch(
        "prefect_invenio_rdm.flows.commit_draft_file_upload",
        mock_commit_draft_file_upload,
    )

    await flows.upload_draft_files(
        credentials=credentials, record_id=1, files=dir_files
    )

    mock_start_draft_file_uploads.assert_called_once_with(
        credentials=credentials,
        record_id=1,
        file_keys=[{"key": "file.txt"}, {"key": "image.png"}],
    )

    mock_upload_draft_file.map.assert_called_once_with(
        credentials=unmapped(credentials),
        record_id=unmapped(1),
        file_name=["file.txt", "image.png"],
        file=dir_files,
    )
    mock_upload_draft_file.map.return_value.result.assert_called_once_with(
        raise_on_failure=True
    )

    mock_commit_draft_file_upload.map.assert_called_once_with(
        credentials=unmapped(credentials),
        record_id=unmapped(1),
        file_name=["file.txt", "image.png"],
    )
    mock_commit_draft_file_upload.map.return_value.result.assert_called_once_with(
        raise_on_failure=True
    )