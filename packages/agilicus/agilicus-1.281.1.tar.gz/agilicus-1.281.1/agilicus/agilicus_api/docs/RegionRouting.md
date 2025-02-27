# RegionRouting

Describes how a Region may be accessed over the Internet. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**domains** | [**[Domain]**](Domain.md) | The domains that address this Region. Use these when configuring external systems such as a DNS CNAME or a firewall.  | 
**requests_enabled** | **bool** | If true, allow this Region to serve RoutingRequests. | [optional] 
**org_domains** | [**[Domain]**](Domain.md) | Organisation subdomains supported by this region | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


