# prefect-invenio-rdm

`prefect-invenio-rdm` is a collection of prebuilt Prefect tasks and flows that can be used to publish local data to an [InvenioRDM](https://inveniordm.docs.cern.ch/reference/) instance.

## Getting started

Requires an installation of Python 3.9+.

### Installation

Install `prefect-invenio-rdm`:

```bash
pip install prefect-invenio-rdm
```

### Authentication
To authenticate with an InvenioRDM instance, either define the following environment variables:

```bash
export INVENIO_RDM_ACCESS_TOKEN=<access_token>
export INVENIO_RDM_BASE_URL=<base url>
```

or create and provide instance of `InvenioRDMCredentials`:

```python
from prefect_invenio_rdm.credentials import InvenioRDMCredentials

credentials = InvenioRDMCredentials(
    base_url="https://sandbox.zenodo.org/api/",
    token="access token",
)
```
### Concurrency

To configure concurrency for API calls, create a global concurrency limit named `rate-limit:invenio-rdm-api`:

```bash
prefect gcl create rate-limit:invenio-rdm-api --limit 5 --slot-decay-per-second 1.0
```

### Example
```python
import asyncio
from prefect import flow
from prefect_invenio_rdm.flows import create_record_dir, create_record_files
from prefect_invenio_rdm.models.records import DraftConfig, Access
from prefect_invenio_rdm.credentials import InvenioRDMCredentials
from prefect_invenio_rdm.models.api import APIResult


@flow(log_prints=True)
async def upload_data() -> None:
    # create credentials
    credentials = InvenioRDMCredentials(
        base_url="https://sandbox.zenodo.org/api/",
        token="access token",
    )

    # provide draft record configurations
    config = DraftConfig(
        record_access=Access.PUBLIC,
        files_access=Access.PUBLIC,
        files_enabled=True,
        metadata={
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Collins",
                        "given_name": "Thomas",
                        "identifiers": [
                            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                        ],
                        "name": "Collins, Thomas",
                        "type": "personal",
                    },
                    "affiliations": [{"id": "01ggx4157", "name": "Entity One"}],
                },
            ],
            "publisher": "InvenioRDM",
            "publication_date": "2025-01-10",
            "resource_type": {"id": "dataset"},
            "title": "My dataset",
        },
        community_id="9d50c9c1-afd0-4dc1-ad50-91040788af4f",
        custom_fields={
            "code:codeRepository": "https://github.com/organization/repository",
            "code:developmentStatus": {"id": "wip"},
            "code:programmingLanguage": [{"id": "python"}],
        },
    )

    # upload data from a directory
    result: APIResult = await create_record_dir(
        credentials=credentials,
        directory="/home/user/data/dataset/",
        config=config,
        file_pattern="*.zip",
        # delete created record if any downstream process (e.g file upload) fails 
        delete_on_failure=True,
        # automatically publishes the draft record if no failures arise
        auto_publish=False,
    )

    # or upload data from a list of files
    result: APIResult = await create_record_files(
        credentials=credentials,
        files=["/home/user/data/dataset/content.zip", "/home/user/images/image.png"],
        config=config,
        delete_on_failure=True,
        auto_publish=False,
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(upload_data())
```