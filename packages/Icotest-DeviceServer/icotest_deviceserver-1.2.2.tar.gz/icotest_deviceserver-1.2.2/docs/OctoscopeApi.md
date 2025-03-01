# DeviceServer.OctoscopeApi

All URIs are relative to *http://localhost/DeviceServer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_tray_description**](OctoscopeApi.md#get_tray_description) | **GET** /Octoscope/{device_id}/Tray/Description | GET description of Tray
[**get_tray_present**](OctoscopeApi.md#get_tray_present) | **GET** /Octoscope/{device_id}/Tray/Present | GET state of Port Module Relay
[**get_tray_uuid**](OctoscopeApi.md#get_tray_uuid) | **GET** /Octoscope/{device_id}/Tray/UUID | GET UUID of Tray
[**put_tray_description**](OctoscopeApi.md#put_tray_description) | **PUT** /Octoscope/{device_id}/Tray/Description | PUT description of Tray
[**put_tray_uuid**](OctoscopeApi.md#put_tray_uuid) | **PUT** /Octoscope/{device_id}/Tray/UUID | PUT UUID of Tray


# **get_tray_description**
> object get_tray_description(device_id)

GET description of Tray

Returns the connected tray's Description.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.OctoscopeApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET description of Tray
        api_response = api_instance.get_tray_description(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OctoscopeApi->get_tray_description: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tray_present**
> bool get_tray_present(device_id)

GET state of Port Module Relay

Returns state of tray connectivity.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.OctoscopeApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET state of Port Module Relay
        api_response = api_instance.get_tray_present(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OctoscopeApi->get_tray_present: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tray_uuid**
> object get_tray_uuid(device_id)

GET UUID of Tray

Returns the connected tray's UUID.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.OctoscopeApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET UUID of Tray
        api_response = api_instance.get_tray_uuid(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OctoscopeApi->get_tray_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_tray_description**
> str put_tray_description(device_id, tray_description)

PUT description of Tray

Sets the connected tray's Description.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.OctoscopeApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
tray_description = 'tray_description_example' # str | Description for Octoscope Tray

    try:
        # PUT description of Tray
        api_response = api_instance.put_tray_description(device_id, tray_description)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OctoscopeApi->put_tray_description: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **tray_description** | **str**| Description for Octoscope Tray | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_tray_uuid**
> str put_tray_uuid(device_id, tray_uuid)

PUT UUID of Tray

Sets the connected tray's UUID.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.OctoscopeApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
tray_uuid = 'tray_uuid_example' # str | UUID for Octoscope Tray

    try:
        # PUT UUID of Tray
        api_response = api_instance.put_tray_uuid(device_id, tray_uuid)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OctoscopeApi->put_tray_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **tray_uuid** | **str**| UUID for Octoscope Tray | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

