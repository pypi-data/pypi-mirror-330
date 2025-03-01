# DeviceServer.AttenuatorApi

All URIs are relative to *http://localhost/DeviceServer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_attenuator_state**](AttenuatorApi.md#get_attenuator_state) | **GET** /Attenuator/{device_id}/Attenuate | GET attenuation state
[**get_channel_attenuation**](AttenuatorApi.md#get_channel_attenuation) | **GET** /Attenuator/{device_id}/AttenuateChannel | GET attenuation channel state
[**get_device_attenuation_configuration**](AttenuatorApi.md#get_device_attenuation_configuration) | **GET** /Attenuator/{device_id}/AttenuatorConfig | GET attenuation device config
[**put_attenuator_state**](AttenuatorApi.md#put_attenuator_state) | **PUT** /Attenuator/{device_id}/Attenuate | PUT attenuation state
[**put_channel_attenuation**](AttenuatorApi.md#put_channel_attenuation) | **PUT** /Attenuator/{device_id}/AttenuateChannel | PUT attenuation state


# **get_attenuator_state**
> AttenuationState get_attenuator_state(device_id, expander_index, expander_port_index=expander_port_index)

GET attenuation state

Get attenuation state by expander port index.

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
    api_instance = DeviceServer.AttenuatorApi(api_client)
    device_id = 'device_id_example' # str | 
expander_index = 56 # int | expander index
expander_port_index = 56 # int | expander port index (optional)

    try:
        # GET attenuation state
        api_response = api_instance.get_attenuator_state(device_id, expander_index, expander_port_index=expander_port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AttenuatorApi->get_attenuator_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **expander_index** | **int**| expander index | 
 **expander_port_index** | **int**| expander port index | [optional] 

### Return type

[**AttenuationState**](AttenuationState.md)

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

# **get_channel_attenuation**
> ChannelAttenuationState get_channel_attenuation(device_id, channel_index)

GET attenuation channel state

Get attenuation state sof selected channel

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
    api_instance = DeviceServer.AttenuatorApi(api_client)
    device_id = 'device_id_example' # str | 
channel_index = 56 # int | channel index

    try:
        # GET attenuation channel state
        api_response = api_instance.get_channel_attenuation(device_id, channel_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AttenuatorApi->get_channel_attenuation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **channel_index** | **int**| channel index | 

### Return type

[**ChannelAttenuationState**](ChannelAttenuationState.md)

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

# **get_device_attenuation_configuration**
> object get_device_attenuation_configuration(device_id)

GET attenuation device config

Getattenuation condig sent through by the device

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
    api_instance = DeviceServer.AttenuatorApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET attenuation device config
        api_response = api_instance.get_device_attenuation_configuration(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AttenuatorApi->get_device_attenuation_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

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

# **put_attenuator_state**
> str put_attenuator_state(device_id, expander_index, expander_port_index, value)

PUT attenuation state

Get attenuation state selected expander port

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
    api_instance = DeviceServer.AttenuatorApi(api_client)
    device_id = 'device_id_example' # str | 
expander_index = 56 # int | expander index
expander_port_index = 56 # int | expander port
value = 56 # int | attenuation value

    try:
        # PUT attenuation state
        api_response = api_instance.put_attenuator_state(device_id, expander_index, expander_port_index, value)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AttenuatorApi->put_attenuator_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **expander_index** | **int**| expander index | 
 **expander_port_index** | **int**| expander port | 
 **value** | **int**| attenuation value | 

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
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_channel_attenuation**
> str put_channel_attenuation(device_id, channel_index, value)

PUT attenuation state

Put attenuation state of selected channel

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
    api_instance = DeviceServer.AttenuatorApi(api_client)
    device_id = 'device_id_example' # str | 
channel_index = 56 # int | channel index
value = 56 # int | attenuation value

    try:
        # PUT attenuation state
        api_response = api_instance.put_channel_attenuation(device_id, channel_index, value)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AttenuatorApi->put_channel_attenuation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **channel_index** | **int**| channel index | 
 **value** | **int**| attenuation value | 

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
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

