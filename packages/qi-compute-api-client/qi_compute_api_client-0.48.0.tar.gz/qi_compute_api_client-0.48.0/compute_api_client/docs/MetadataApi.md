# compute_api_client.MetadataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_metadata_self_metadata_post**](MetadataApi.md#create_metadata_self_metadata_post) | **POST** /metadata | Create metadata
[**read_metadata_by_backend_id_metadata_backend_backend_id_get**](MetadataApi.md#read_metadata_by_backend_id_metadata_backend_backend_id_get) | **GET** /metadata/backend/{backend_id} | Retrieve metadata by backend ID
[**read_metadata_metadata_id_get**](MetadataApi.md#read_metadata_metadata_id_get) | **GET** /metadata/{id} | Get metadata by ID


# **create_metadata_self_metadata_post**
> Metadata create_metadata_self_metadata_post(metadata_in)

Create metadata

Create new metadata.

### Example

* Api Key Authentication (backend):
```python
import time
import os
import compute_api_client
from compute_api_client.models.metadata import Metadata
from compute_api_client.models.metadata_in import MetadataIn
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: backend
configuration.api_key['backend'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['backend'] = 'Bearer'

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.MetadataApi(api_client)
    metadata_in = compute_api_client.MetadataIn() # MetadataIn | 

    try:
        # Create metadata
        api_response = await api_instance.create_metadata_self_metadata_post(metadata_in)
        print("The response of MetadataApi->create_metadata_self_metadata_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetadataApi->create_metadata_self_metadata_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metadata_in** | [**MetadataIn**](MetadataIn.md)|  | 

### Return type

[**Metadata**](Metadata.md)

### Authorization

[backend](../README.md#backend)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_metadata_by_backend_id_metadata_backend_backend_id_get**
> PageMetadata read_metadata_by_backend_id_metadata_backend_backend_id_get(backend_id, sort_by=sort_by, latest=latest, page=page, size=size)

Retrieve metadata by backend ID

Get metadata by job ID.

### Example

* OAuth Authentication (user_bearer):
```python
import time
import os
import compute_api_client
from compute_api_client.models.page_metadata import PageMetadata
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.MetadataApi(api_client)
    backend_id = 56 # int | 
    sort_by = 'sort_by_example' # str | The field name to sort on. Prefix with '-' for descending order. E.g., '-created_on'. (optional)
    latest = True # bool | If True gets the most recently created object. (optional)
    page = 1 # int | Page number (optional) (default to 1)
    size = 50 # int | Page size (optional) (default to 50)

    try:
        # Retrieve metadata by backend ID
        api_response = await api_instance.read_metadata_by_backend_id_metadata_backend_backend_id_get(backend_id, sort_by=sort_by, latest=latest, page=page, size=size)
        print("The response of MetadataApi->read_metadata_by_backend_id_metadata_backend_backend_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetadataApi->read_metadata_by_backend_id_metadata_backend_backend_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **backend_id** | **int**|  | 
 **sort_by** | **str**| The field name to sort on. Prefix with &#39;-&#39; for descending order. E.g., &#39;-created_on&#39;. | [optional] 
 **latest** | **bool**| If True gets the most recently created object. | [optional] 
 **page** | **int**| Page number | [optional] [default to 1]
 **size** | **int**| Page size | [optional] [default to 50]

### Return type

[**PageMetadata**](PageMetadata.md)

### Authorization

[user_bearer](../README.md#user_bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_metadata_metadata_id_get**
> Metadata read_metadata_metadata_id_get(id)

Get metadata by ID

Get metadata by ID.

### Example

* OAuth Authentication (user_bearer):
```python
import time
import os
import compute_api_client
from compute_api_client.models.metadata import Metadata
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.MetadataApi(api_client)
    id = 56 # int | 

    try:
        # Get metadata by ID
        api_response = await api_instance.read_metadata_metadata_id_get(id)
        print("The response of MetadataApi->read_metadata_metadata_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetadataApi->read_metadata_metadata_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Metadata**](Metadata.md)

### Authorization

[user_bearer](../README.md#user_bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

