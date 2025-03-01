# DeviceServer.InternalApi

All URIs are relative to *http://localhost/DeviceServer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_device_uuid**](InternalApi.md#get_device_uuid) | **GET** /Internal/{device_serial} | GET uuid from database
[**get_message_from_rx_buffer**](InternalApi.md#get_message_from_rx_buffer) | **GET** /Internal/messages/rx | GET message from RX table
[**get_message_from_tx_buffer**](InternalApi.md#get_message_from_tx_buffer) | **GET** /Internal/messages/tx | GET message from TX table
[**put_device**](InternalApi.md#put_device) | **PUT** /Internal/AddDevice | PUT Add Device


# **get_device_uuid**
> object get_device_uuid(device_serial)

GET uuid from database

Query database for device_id by device_serial.

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
    api_instance = DeviceServer.InternalApi(api_client)
    device_serial = 'device_serial_example' # str | Serial number of device

    try:
        # GET uuid from database
        api_response = api_instance.get_device_uuid(device_serial)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling InternalApi->get_device_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_serial** | **str**| Serial number of device | 

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

# **get_message_from_rx_buffer**
> object get_message_from_rx_buffer(device_id=device_id)

GET message from RX table

GET a message from the rx table.

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
    api_instance = DeviceServer.InternalApi(api_client)
    device_id = 'device_id_example' # str |  (optional)

    try:
        # GET message from RX table
        api_response = api_instance.get_message_from_rx_buffer(device_id=device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling InternalApi->get_message_from_rx_buffer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | [optional] 

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

# **get_message_from_tx_buffer**
> str get_message_from_tx_buffer(device_id=device_id, device_serial=device_serial, device_type=device_type)

GET message from TX table

GET a message from the tx table.

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
    api_instance = DeviceServer.InternalApi(api_client)
    device_id = 'device_id_example' # str |  (optional)
device_serial = 'device_serial_example' # str |  (optional)
device_type = 'device_type_example' # str |  (optional)

    try:
        # GET message from TX table
        api_response = api_instance.get_message_from_tx_buffer(device_id=device_id, device_serial=device_serial, device_type=device_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling InternalApi->get_message_from_tx_buffer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | [optional] 
 **device_serial** | **str**|  | [optional] 
 **device_type** | **str**|  | [optional] 

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

# **put_device**
> str put_device(device_id=device_id, config_file_name=config_file_name, device_serial=device_serial)

PUT Add Device

Add Device to database.

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
    api_instance = DeviceServer.InternalApi(api_client)
    device_id = 'device_id_example' # str | Device UUID (optional)
config_file_name = 'config_file_name_example' # str | Config file name (optional)
device_serial = 'device_serial_example' # str | Device Serial (optional)

    try:
        # PUT Add Device
        api_response = api_instance.put_device(device_id=device_id, config_file_name=config_file_name, device_serial=device_serial)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling InternalApi->put_device: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| Device UUID | [optional] 
 **config_file_name** | **str**| Config file name | [optional] 
 **device_serial** | **str**| Device Serial | [optional] 

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

