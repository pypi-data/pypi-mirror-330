# Wrk Platform SDK

A Python Wrk Platform SDK. It is a library that provides a set of tools to interact with the Wrk Platform.

## Requirements.

Python 3.8+

## Installation & Usage

```sh
pip install wrk-platform-sdk
```

Then import the package:
```python
import wrk_platform_sdk
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import wrk_platform_sdk
from wrk_platform_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://account.wrk.com/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = wrk_platform_sdk.Configuration(
    host = "https://account.wrk.com/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key_prefix['ApiKeyAuth'] = 'Api-Key'
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Enter a context with an instance of the API client
with wrk_platform_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = wrk_platform_sdk.LaunchesApi(api_client)
    launch_id = 'launch_id_example' # str |

    try:
        # Fetch a specific Wrkflow Launch
        api_response = api_instance.get_launch_by_id(launch_id)
        print("The response of LaunchesApi->get_launch_by_id:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LaunchesApi->get_launch_by_id: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://account.wrk.com/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*LaunchesApi* | [**get_launch_by_id**](docs/LaunchesApi.md#get_launch_by_id) | **GET** /launch/{launch_id} | Fetch a specific Wrkflow Launch
*LaunchesApi* | [**get_launches**](docs/LaunchesApi.md#get_launches) | **GET** /launch | Fetch multiple Wrkflow Launches
*LaunchesApi* | [**launch_wrkflow**](docs/LaunchesApi.md#launch_wrkflow) | **POST** /wrkflow/{wrkflow_uuid}/launch | Launch a Wrkflow
*LaunchesApi* | [**pause_launch**](docs/LaunchesApi.md#pause_launch) | **POST** /launch/{launch_id}/pause | Pause a Wrkflow Launch
*LaunchesApi* | [**resume_launch**](docs/LaunchesApi.md#resume_launch) | **POST** /launch/{launch_id}/resume | Resume a Wrkflow Launch
*WrkflowsApi* | [**get_wrkflow_by_uuid**](docs/WrkflowsApi.md#get_wrkflow_by_uuid) | **GET** /wrkflow/{wrkflow_uuid} | Fetch a specific Wrkflow
*WrkflowsApi* | [**get_wrkflows**](docs/WrkflowsApi.md#get_wrkflows) | **GET** /wrkflow | Fetch multiple Wrkflows


## Documentation For Models

 - [GetLaunchByIdResponse](docs/GetLaunchByIdResponse.md)
 - [GetLaunchesResponse](docs/GetLaunchesResponse.md)
 - [GetWrkflowByUuidResponse](docs/GetWrkflowByUuidResponse.md)
 - [GetWrkflowsResponse](docs/GetWrkflowsResponse.md)
 - [Launch](docs/Launch.md)
 - [LaunchState](docs/LaunchState.md)
 - [LaunchWrkflowRequest](docs/LaunchWrkflowRequest.md)
 - [LaunchWrkflowResponse](docs/LaunchWrkflowResponse.md)
 - [WrkError](docs/WrkError.md)
 - [WrkErrorDetails](docs/WrkErrorDetails.md)
 - [Wrkflow](docs/Wrkflow.md)
 - [WrkflowSchedule](docs/WrkflowSchedule.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="ApiKeyAuth"></a>
### ApiKeyAuth

- **Type**: API key
- **API key parameter name**: Authorization
- **API key prefix**: Api-Key
- **Location**: HTTP header
