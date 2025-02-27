"""Tests for the tasks.py module"""

# pylint: disable=redefined-outer-name
from typing import Generator, Any
from unittest.mock import Mock, AsyncMock, patch, mock_open, call
import pytest
import respx
import httpx

from prefect.testing.utilities import prefect_test_harness
from prefect.logging import disable_run_logger

from prefect_invenio_rdm.models.records import DraftConfig, Access
from prefect_invenio_rdm.credentials import InvenioRDMCredentials
from prefect_invenio_rdm import tasks
from prefect_invenio_rdm.models.api import (
    APIError,
    ErrorType,
)
from prefect_invenio_rdm.constants import (
    INVENIO_RDM_ACCESS_TOKEN,
    INVENIO_RDM_BASE_URL,
    ACCESS_TOKEN_BLOCK,
)


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
    Creates a test instance of InvenioRDMCredentials
    """
    return InvenioRDMCredentials(
        base_url="https://example.org/api/",
        token="testing_token",
    )


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mocks environment variables.
    """
    monkeypatch.setenv(INVENIO_RDM_ACCESS_TOKEN, "test access token")
    monkeypatch.setenv(INVENIO_RDM_BASE_URL, "test base url")


@pytest.fixture
def mock_api() -> Generator[respx.MockRouter, Any, None]:
    """Configures RESPX router settings"""
    base_url = "https://example.org/api/"
    with respx.mock(
        base_url=base_url, assert_all_called=True, assert_all_mocked=True
    ) as mock:
        yield mock


@patch("prefect_invenio_rdm.tasks.Secret")
async def test_get_access_token(mock_secret: Mock) -> None:
    """
    Tests that get_access_token() successfully loads an access token
    from the env var into a Prefect Secret Block.
    """

    mock_instance = mock_secret.return_value
    mock_instance.save = AsyncMock(return_value=None)

    secret = await tasks.get_access_token.fn()
    assert secret == mock_instance

    mock_secret.assert_called_once_with(value="test access token")
    mock_instance.save.assert_called_once_with(name=ACCESS_TOKEN_BLOCK, overwrite=True)


@patch("prefect_invenio_rdm.tasks.os.getenv")
@patch("prefect_invenio_rdm.tasks.Secret")
async def test_get_access_token_raises_error_on_missing_env_var(
    mock_secret: Mock,
    mock_get_env: Mock,
) -> None:
    """
    Tests that get_access_token() raises an error if the expected
    env var is not set.
    """

    mock_get_env.return_value = None

    with pytest.raises(
        ValueError, match="Environment variable 'INVENIO_RDM_ACCESS_TOKEN' is not set."
    ):
        await tasks.get_access_token.fn()

    mock_get_env.assert_called_once_with(INVENIO_RDM_ACCESS_TOKEN)
    mock_secret.assert_not_called()


async def test_get_base_url() -> None:
    """
    Tests that get_base_url() returns the defined base URL.
    """
    url = await tasks.get_base_url.fn()
    assert url == "test base url"


@patch("prefect_invenio_rdm.tasks.os.getenv")
async def test_get_base_url_raises_error_on_missing_env_var(
    mock_get_env: Mock,
) -> None:
    """
    Tests that get_base_url() raises an error if the expected
    env var is not set.
    """

    mock_get_env.return_value = None

    with pytest.raises(
        ValueError, match="Environment variable 'INVENIO_RDM_BASE_URL' is not set."
    ):
        await tasks.get_base_url.fn()

    mock_get_env.assert_called_once_with(INVENIO_RDM_BASE_URL)


@patch("prefect_invenio_rdm.tasks.os.path")
async def test_validate_upload_files_with_existing_files(
    mock_path: Mock,
) -> None:
    """
    Tests that validate_upload_files() returns True if all files exist.
    """

    mock_path.exists.side_effect = [True, True]

    await tasks.validate_upload_files.fn(files=["files/file.txt", "image.png"])

    assert mock_path.exists.call_args_list == [
        call("files/file.txt"),
        call("image.png"),
    ]


@patch("prefect_invenio_rdm.tasks.os.path")
async def test_validate_files_with_invalid_files(
    mock_path: Mock,
) -> None:
    """
    Tests that validate_upload_files() successfully returns False
    if one or more files does not exist.
    """

    mock_path.exists.side_effect = [True, False]

    with pytest.raises(ValueError, match="The list of file paths cannot be empty"):
        await tasks.validate_upload_files.fn(files=[])

    with pytest.raises(
        ValueError, match="Cannot find one or more files in the list of paths provided"
    ):
        await tasks.validate_upload_files.fn(files=["files/file.txt", "image.png"])

    assert mock_path.exists.call_args_list == [
        call("files/file.txt"),
        call("image.png"),
    ]


async def test_validate_file_uploads_without_errors() -> None:
    """
    Tests that validate_file_uploads() returns True if all
    file upload results were successful.
    """

    result = await tasks.validate_file_uploads.fn(
        upload_results=[{"key": "file.txt"}, {"key": "image.png"}],
        files=["files/file.txt", "image.png"],
    )

    assert result is True


async def test_validate_file_uploads_with_errors() -> None:
    """
    Tests that validate_file_uploads() returns False if one
    or more file upload results are errors.
    """

    result = await tasks.validate_file_uploads.fn(
        upload_results=[{"key": "file.txt"}, httpx.HTTPError("error")],
        files=["files/file.txt", "image.png"],
    )

    assert result is False


async def test_validate_file_uploads_does_not_match_file_count() -> None:
    """
    Tests that validate_file_uploads() returns False if the number of
    file upload results does not match the number of files.
    """

    result = await tasks.validate_file_uploads.fn(
        upload_results=[{"key": "file.txt"}], files=["files/file.txt", "image.png"]
    )

    assert result is False


async def test_get_file_upload_errors() -> None:
    """
    Tests that get_file_upload_errors() successfully creates
    an instance of APIError for all failed file upload requests.
    """

    result = await tasks.get_file_upload_errors.fn(
        upload_results=[{"key": "file.txt"}, httpx.HTTPError("file upload error")],
    )

    assert result == [
        APIError(type=ErrorType.FILE_UPLOAD, error_message="file upload error")
    ]


@patch("prefect_invenio_rdm.tasks.glob")
@patch("prefect_invenio_rdm.tasks.os.path.isfile")
@patch("prefect_invenio_rdm.tasks.os.path.exists")
async def test_get_dir_files(
    mock_exists: Mock,
    mock_is_file: Mock,
    mock_glob: Mock,
) -> None:
    """
    Tests that get_dir_files() successfully retrieves all
    matching files for each directory.
    """

    mock_exists.return_value = True
    mock_is_file.side_effect = [True, False, True]

    mock_glob.glob.return_value = [
        "files/file.txt",
        "files/other/",
        "files/other/test.txt",
    ]

    result = await tasks.get_dir_files.fn(
        directory="files/", pattern="**/*", recursive=True
    )

    assert mock_exists.call_args_list == [call("files/")]
    assert mock_glob.glob.call_args_list == [
        call("files/**/*", recursive=True),
    ]

    assert result == ["files/file.txt", "files/other/test.txt"]


@patch("prefect_invenio_rdm.tasks.os.path.exists")
async def test_get_dir_files_raises_error_for_invalid_dir(
    mock_path_exists: Mock,
) -> None:
    """
    Tests that get_dir_files() raises an error if a directory does
    not exist.
    """

    mock_path_exists.return_value = False

    with pytest.raises(ValueError, match="The directory 'files/' does not exist."):
        await tasks.get_dir_files.fn(directory="files/", pattern="*.txt")

    mock_path_exists.assert_called_with("files/")


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_create_draft_record_successful(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that create_draft_record() successfully executes a
    request to create a record.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    expected_json = {"id": 1}

    mock_api.post(
        "records",
        json={
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": True},
            "metadata": {},
        },
    ).mock(return_value=httpx.Response(201, json=expected_json))

    response = await tasks.create_draft_record.fn(
        credentials=credentials,
        config=DraftConfig(
            record_access=Access.PUBLIC,
            files_access=Access.PUBLIC,
            files_enabled=True,
            metadata={},
        ),
    )

    assert response == expected_json

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_create_draft_record_raises_status_error(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that create_draft_record() raises a status
    error for unsuccessful requests.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    mock_api.post("records").mock(return_value=httpx.Response(400, json=None))

    with pytest.raises(httpx.HTTPStatusError):
        await tasks.create_draft_record.fn(
            credentials=credentials,
            config=DraftConfig(
                record_access=Access.PUBLIC,
                files_access=Access.PUBLIC,
                files_enabled=True,
                metadata={},
            ),
        )

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_publish_draft_record_successful(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that publish_draft_record() successfully executes a
    request to publish a record.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    expected_json = {"id": 1005, "published": True}

    mock_api.post("records/1005/draft/actions/publish").mock(
        return_value=httpx.Response(201, json=expected_json)
    )

    response = await tasks.publish_draft_record.fn(
        credentials=credentials,
        record_id=1005,
    )

    assert response == expected_json

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_publish_draft_record_raises_status_error(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that publish_draft_record() raises a status
    error for unsuccessful requests.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    mock_api.post("records/1005/draft/actions/publish").mock(
        return_value=httpx.Response(400, json=None)
    )

    with pytest.raises(httpx.HTTPStatusError):
        await tasks.publish_draft_record.fn(
            credentials=credentials,
            record_id=1005,
        )

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_delete_draft_record_successful(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that delete_draft_record() successfully executes a
    request to delete a record.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    mock_api.delete("records/1005/draft").mock(return_value=httpx.Response(201))

    await tasks.delete_draft_record.fn(
        credentials=credentials,
        record_id=1005,
    )

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_delete_draft_record_raises_status_error(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that delete_draft_record() raises a status
    error for unsuccessful requests.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    mock_api.delete("records/1005/draft").mock(
        return_value=httpx.Response(400, json=None)
    )

    with pytest.raises(httpx.HTTPStatusError):
        await tasks.delete_draft_record.fn(
            credentials=credentials,
            record_id=1005,
        )

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_start_draft_file_uploads_successful(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that start_draft_file_uploads() successfully executes a
    request to start file uploads.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    file_keys = [{"key": "file.txt"}, {"key": "image.png"}]
    expected_json = {"enabled": True, "entries": []}

    mock_api.post("records/1005/draft/files", json=file_keys).mock(
        return_value=httpx.Response(201, json=expected_json)
    )

    response = await tasks.start_draft_file_uploads.fn(
        credentials=credentials, record_id=1005, file_keys=file_keys
    )

    assert response == expected_json
    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_start_draft_file_uploads_raises_status_error(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that start_draft_file_uploads() raises a status
    error for unsuccessful requests.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    file_keys = [{"key": "file.txt"}, {"key": "image.png"}]

    mock_api.post("records/1005/draft/files", json=file_keys).mock(
        return_value=httpx.Response(400, json=None)
    )

    with pytest.raises(httpx.HTTPStatusError):
        await tasks.start_draft_file_uploads.fn(
            credentials=credentials, record_id=1005, file_keys=file_keys
        )

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.os.path")
@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_upload_draft_file_successful(
    mock_rate_limit: Mock,
    mock_path: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Tests that upload_draft_file() successfully executes a
    request to upload a file to a record.
    """

    caplog.set_level("INFO")

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    mock_path.getsize.return_value = 1024 * 1024

    open_mocked = mock_open(read_data=b"test file data")

    file = "folder/test.txt"
    with patch("builtins.open", open_mocked):
        expected_json = {"key": "test.txt"}
        mock_api.put(
            "https://example.org/api/records/1005/draft/files/test.txt/content"
        ).mock(return_value=httpx.Response(201, json=expected_json))

        response = await tasks.upload_draft_file.fn(
            credentials=credentials,
            record_id=1005,
            file_name="test.txt",
            file=file,
        )

        assert response == expected_json

        mock_path.getsize.assert_called_once_with(file)

        assert "Uploading file 'folder/test.txt', size: 1MB" in caplog.text
        mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.os.path")
@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_upload_draft_file_raises_status_error(
    mock_rate_limit: Mock,
    mock_path: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that upload_draft_file() raises a status
    error for unsuccessful requests.
    """
    mock_rate_limit.return_value = AsyncMock(return_value=None)
    mock_path.getsize.return_value = 1024 * 1024
    open_mocked = mock_open(read_data=b"test file data")

    with patch("builtins.open", open_mocked):
        mock_api.put(
            "https://example.org/api/records/1005/draft/files/test.txt/content"
        ).mock(return_value=httpx.Response(400, json=None))

        with pytest.raises(httpx.HTTPStatusError):
            await tasks.upload_draft_file.fn(
                credentials=credentials,
                record_id=1005,
                file_name="test.txt",
                file="folder/test.txt",
            )

    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_commit_draft_file_upload_successful(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that commit_draft_file_upload() successfully executes a
    request to commit an uploaded file.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    expected_json = {"file_id": "test_file_id"}
    mock_api.post("records/1005/draft/files/test.txt/commit").mock(
        return_value=httpx.Response(201, json=expected_json)
    )

    response = await tasks.commit_draft_file_upload.fn(
        credentials=credentials, record_id=1005, file_name="test.txt"
    )

    assert response == expected_json
    mock_rate_limit.assert_awaited()


@patch("prefect_invenio_rdm.tasks.rate_limit")
async def test_commit_draft_file_upload_raises_status_error(
    mock_rate_limit: Mock,
    credentials: InvenioRDMCredentials,
    mock_api: respx.MockRouter,
) -> None:
    """
    Tests that commit_draft_file_upload() raises a status
    error for unsuccessful requests.
    """

    mock_rate_limit.return_value = AsyncMock(return_value=None)

    mock_api.post("records/1005/draft/files/test.txt/commit").mock(
        return_value=httpx.Response(400, json=None)
    )

    with pytest.raises(httpx.HTTPStatusError):
        await tasks.commit_draft_file_upload.fn(
            credentials=credentials, record_id=1005, file_name="test.txt"
        )

    mock_rate_limit.assert_awaited()
