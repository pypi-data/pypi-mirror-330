# ma-kyc-ri-pfpy

This is the `pfpy` (pronounced "puff py") package, a python package for integrating with PassFort. The goal of this package is to provide common utils, such as signature validation that allow web applications to integrate easily with PassFort.

<img src="logo.jpg" width="200" height="200">

## Installation

The package is now available via PyPi: [https://pypi.org/project/ma-kyc-ri-pfpy/](https://pypi.org/project/ma-kyc-ri-pfpy/)

If you want to use this package in your project, just install it using pip:

- `pip install ma-kyc-ri-pfpy`

Alternatively, if you want the latest version from the repo here (which may be unpublished), you can do the following. This is an example using `uv` (Python package installer and resolver, written in Rust). More info on `uv` can be found here: (https://github.com/astral-sh/uv)[https://github.com/astral-sh/uv]:

- `uv pip install git+https://github.com/moodysanalytics/ma-kyc-ri-pf-pfpy.git@main#egg=pfpy`

The package will be pulle directly from the github repo that sits inside the Moody's Github org.

## Usage

You need to have set a `PASSFORT_INTEGRATION_SECRET_KEY` environment variable, which is used to sign requests.

After that is set, simply import the relevant classes from `pfpy.auth` and use them in your request handlers.

NOTE: At the moment only FastApi has been tested in deployment with the validation classes (but theoretically any framework should work).

`pfpy` uses Pydantic to validate different kinds of data. If the data is not valid, an exception will be thrown that should be handled by the application.

An example with FastApi is below:

```python
from pfpy.auth.parsed_header import ParsedSignedHeaderRequest
from pfpy.auth.parsed_url import ParsedSignedUrl
from pfpy.types.response_types import PassFortEntityDataCheck


@router.post("/checks")
async def checks(
    request: Request, request_body: PassfortIntegrationEntityDataCheckRequest
) -> PassFortEntityDataCheck | dict[str, Any]:

    try:
        # If parsing fails, then we know the signature in the header was invalid
        ParsedSignedHeaderRequest(
            method=request.method,
            request_url=str(request.url),
            request_method=request.method,
            headers=dict(request.headers),
        )

        if request_body.demo_result:
            return PassfortIntegrationService.run_demo_check(request_body.demo_result).model_dump(
                exclude_none=True, mode="json"
            )

        return PassfortIntegrationService.entity_check(request_body)

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Signature header validation failed: {e}.")

@router.get("/external-resources/{bvd_id}/")
async def external_resources(
    request: Request,
    bvd_id: str,
    version: str,
    valid_until: str,
    auditee_id: str,
    signature: str,
    custom_data: Optional[str] = None,
):
    try:
        # If parsing fails, then we know the signature in the url was invalid
        ParsedSignedUrl(
            request_url=str(request.url),
            version=version,
            valid_until=valid_until,
            auditee_id=auditee_id,
            signature=signature,
            custom_data=custom_data,
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"URL signature validation failed.: {e}")
```

## Contributing

- If you wish to contribute to the package, the easiest way would be to install it as an editable local package, then pull it in as a local dependency. 

- This way you can edit the code and just run the local install command below to see the latest changes in whatever app you are using `pfpy` as a dependency:

- git clone the repo
- `uv pip install -e /Users/path-to-the-package/ma-kyc-ri-pf-pfpy`

Replace the path with the actual place where you cloned the repo.

Now, every time you change/add a bit of code, you can simply run the local install to reflect those changes.

### How can I quickly set up my working environment?

- The repo contains a Makefile. Simply running `make` will create a `.venv` and pull in all the dependencies of `pfpy`.

Some other commands you may find useful as you are developing for `pfpy`:

- `make test`: This will run the unit test suite
- `make lint`: This will run the flake8 linter
- `make format`: This will format the repo using `black`
- `make pyright`: This will type check everything using Pyright
- `make requirements`: This will emit the requirements.txt file