# chkp-harmony-endpoint-management-sdk.generated.cloud
<style>details{user-select:none}details>summary span.icon{width:24px;height:24px;transition:all .3s;margin-left:auto}details>ol>li{padding-bottom:20px}summary{cursor:pointer}summary::-webkit-details-marker{display:none}</style><h2>Today more than ever, endpoint security plays a critical role in enabling your remote workforce.</h2><h4>Harmony Endpoint provides comprehensive endpoint protection at the highest security level that is crucial to avoid security breaches and data compromise.</h4><p>The following documentation provides the operations supported by the Harmony Endpoint's External API.</p><p>To use the Harmony Endpoint External API service:</p><ol><li><p>In the <em>Infinity Portal</em>, create a suitable API Key. In the <em>Service</em> field, enter <em>Endpoint</em>.<br>For more information, refer to the <a href=\"https://sc1.checkpoint.com/documents/Infinity_Portal/WebAdminGuides/EN/Infinity-Portal-Admin-Guide/Content/Topics-Infinity-Portal/API-Keys.htm?tocpath=Global%20Settings%7C_____7#API_Keys\">Infinity Portal Administration Guide</a>.<br>Once a key has been created, it may be used indefinitely (unless an expiration date was explicitly set for it).</p>During the key's creation, note the presented <em>Authentication URL</em>. This URL is used to obtain <em>Bearer tokens</em> for the next step</li><li><p>Authenticate using the <em>Infinity Portal's</em> External Authentication Service.<br>The authentication request should be made to the <em>Authentication URL</em> obtained during the previous step.</p><p>Example (<em>Your tenant's authentication URL may differ</em>):</p><p><img src=\"data:image/png;base64,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\"></p><p>Note, image is for reference only. Exact <em>CURL</em> syntax may differ.</p></li><li><p>Include the resulting <em>token</em> in the <em>Authorization</em> header in the form of a <em>Bearer</em> (For example, 'Authorization': 'Bearer {TOKEN}') in every request made to the API service</p></li><li><p>Call the <a href=\"#/Session/LoginCloud\">Cloud Login API</a></p></li><li><p>Include the resulting <em>x-mgmt-api-token</em> in Header <em>x-mgmt-api-token</em> of all subsequent requests</p></li></ol><br><div><p>For your convinience, <em>Harmony Endpoint</em> API SDKs are available here:</p><ul><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-py-sdk\">Python 3.8 and newer</a></li><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-js-ts-sdk\">TypeScript</a></li></ul></div><div><p>In addition, a command-line interface is available <a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-cli\">here</a></p></div><br><div style=\"margin-top:15px;padding-top:30px;padding-bottom:30px\"><h3>Important Notes:</h3><div style=\"margin-left:25px\"><p></p><ul><li style=\"margin-bottom:30px\"><p>When creating an API key, the selected service <b><em>must</em></b> be <em>Endpoint</em> or requests will not be delivered to the service.</p></li><li style=\"margin-bottom:30px\"><p>Operation payload examples should be treated as guidelines and should not be used as-is.</p><p style=\"margin-top:-7px\">Calling a remediation operation, for instance, with the contents of its example will fail.</p></li><li style=\"margin-bottom:30px\"><p>The <em>Harmony Endpoint</em> API service enforces rate-limiting.</p><p style=\"margin-top:-7px\">Please ensure your integration correctly handles <code>HTTP 429 (Too many requests)</code> responses by using appropriate delays and back-off mechanisms.</p></li><li style=\"margin-bottom:30px\"><p>Errors returned by the <em>Harmony Endpoint</em> API service conform, to a large degree, to <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> and convey useful data.</p><p style=\"margin-top:-7px\">It is highly recommended your integration logs the full error as most issues can quickly be pinpointed and rectified by viewing the error contents.</p></li></ul><p></p></div></div><br><div style=\"padding-top:30px;padding-bottom:30px\"><details><summary style=\"font-size:large;font-weight:600;padding-bottom:20px\">Troubleshooting</summary><div style=\"margin-left:25px\"><p>During usage, you may encounter different issues and errors.</p><p>To facilitate resolution of such issues, the <em>Harmony Endpoint API service uses an <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> compliant error structure</em> which conveys information like the type of error that occurred and its source and even potential fixes.<br>This is the first and often last step in diagnosing API related issues.</p><p>The below list is of common errors that may not be obvious from the error message alone.</p><h5>Important notes</h5><ol><li>API errors may be wrapped by a separate object. The content of the errors however is as specified</li><li>Errors that do not follow <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> can be assumed to originate from <em>Infinity Portal</em> which implies a failure in authentication.</li></ol><p></p><p style=\"margin-top:40px\">If you encounter an error that is not listed here and require help, please open a support ticket or request assistance via the e-mail address at the bottom of this documentation page.</p><p style=\"padding-top:10px\">When opening a support ticket, please also provide the following information:</p><ul><li style=\"padding-bottom:8px\">The name and/or address of the API operation</li><li style=\"padding-bottom:8px\">The approximate date and time (including timezone) when you last encountered the issue</li><li style=\"padding-bottom:8px\"><p>The full request (body and headers).</p><p style=\"margin-top:-15px\">For issues pertaining to authentication/login, include your expired <em>Infinity Portal</em> bearer token.</p></li><li style=\"padding-bottom:8px\">The full response returned by the <em>Harmony Endpoint</em> API service</li><li style=\"padding-bottom:8px\">Your use case. For example, \"<em>Retrieving asset information for SIEM integration</em>\" (<b>Optional</b>)</li></ul><p></p><hr style=\"margin-top:25px;margin-bottom:25px\"><div style=\"margin-left:30px\"><details style=\"padding-bottom:15px\"><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"An error has occurred\" }</samp> when authenticating against the <em>Infinity Portal</em></summary><div><h4>Issue:</h4><p>This error usually indicates your authentication request was malformed.</p><h4>Possible Solutions:</h4><p>Make sure your request is a valid JSON, includes header <samp>Content-Type</samp> with a value of <samp>application/json</samp> and looks like <samp>{ \"clientId\": \"{{ciClientId}}\", \"accessKey\": \"{{ciAccessKey}}\" }</samp></p></div></details><details><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"Authentication required\", \"forceLogout\": true }</samp> when invoking Harmony Endpoint API operations</summary><div><h4>Issue:</h4><p>This error indicates that you have attempted to access a resource without a valid Bearer authoriztion token.</p><p>An example could be an attempt to invoke a Harmony Endpoint API operation without providing an <em>Infinity Portal</em> token in the request's <samp>Authorization</samp> header</p><p>Specific cases where this error is raised include:</p><ol><li>A request was made without providing an <em>Infinity Portal</em> bearer token in the <samp>Authorization</samp> header</li><li>A request was directed to to an <em>Infinity Portal</em> gateway other than the one that issued the bearer token</li><li>The provided token is intended for another <em>Infinity Portal</em> application</li><li>The provided token is expired</li><li>The provided token is malformed</li></ol><p></p><h4>Possible Solutions:</h4><p></p><ol><li>Verify the token was created to target the correct application (<em>Endpoint</em>)</li><li>Verify the token has not expired</li><li>Verify the token is being used correctly in the requst (<samp>Authorization: Bearer {{TOKEN}}</samp>)</li></ol><p></p></div></details></div></div></details><br><br></div>

The `chkp_harmony_endpoint_management_sdk.generated.cloud` package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 1.9.221
- Package version: 1.0.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python &gt;&#x3D;3.7

## Installation & Usage

This python library package is generated without supporting files like setup.py or requirements files

To be able to use it, you will need these dependencies in your own package that uses this library:

* urllib3 >= 1.15
* certifi
* python-dateutil

## Getting Started

In your own code, to use this library to connect and interact with chkp-harmony-endpoint-management-sdk.generated.cloud,
you can run the following:

```python

import time
import chkp_harmony_endpoint_management_sdk.generated.cloud
from pprint import pprint
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags import asset_management_api
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.computers_by_filter_args import ComputersByFilterArgs
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.forbidden_error_example import ForbiddenErrorExample
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.internal_error_example import InternalErrorExample
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.job_or_result_i_computer_list import JobOrResultIComputerList
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.missing_api_token_error_example import MissingApiTokenErrorExample
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.run_as_job_onon import RunAsJobONOn
from chkp_harmony_endpoint_management_sdk.generated.cloud.model.unprocessable_entry_error_example import UnprocessableEntryErrorExample
# Defining the host is optional and defaults to https://cloudinfra-gw.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api
# See configuration.py for a list of all supported configuration parameters.
configuration = chkp_harmony_endpoint_management_sdk.generated.cloud.Configuration(
    host = "https://cloudinfra-gw.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (Infinity Portal Token): cloudInfraJwt
configuration = chkp_harmony_endpoint_management_sdk.generated.cloud.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Configure API key authorization: apiJwt
configuration.api_key['apiJwt'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiJwt'] = 'Bearer'

# Enter a context with an instance of the API client
with chkp_harmony_endpoint_management_sdk.generated.cloud.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = asset_management_api.AssetManagementApi(api_client)
    x_mgmt_run_as_job = RunAsJobONOn("on") # RunAsJobONOn | 
computers_by_filter_args = ComputersByFilterArgs(
        filters=[
            IFilter(
                column_name=ComputerColumnNames("emonJsonDataColumns"),
                filter_values=[
                    "filter_values_example"
                ],
                filter_type=FilterType("Contains"),
                is_json=True,
            )
        ],
        paging=ComputersByFilterPaging(
            page_size=1,
            offset=0,
        ),
        view_type=AssetView("ALL_DEVICES"),
    ) # ComputersByFilterArgs | 

    try:
        # Get computers matching the given filters
        api_response = api_instance.computers_by_filter(x_mgmt_run_as_jobcomputers_by_filter_args)
        pprint(api_response)
    except chkp_harmony_endpoint_management_sdk.generated.cloud.ApiException as e:
        print("Exception when calling AssetManagementApi->computers_by_filter: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://cloudinfra-gw.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AssetManagementApi* | [**computers_by_filter**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/AssetManagementApi.md#computers_by_filter) | **post** /v1/asset-management/computers/filtered | Get computers matching the given filters
*IndicatorsOfCompromiseApi* | [**create_ioc**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/IndicatorsOfCompromiseApi.md#create_ioc) | **post** /v1/ioc/create | Create new Indicators of Compromise
*IndicatorsOfCompromiseApi* | [**delete_all_ioc**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/IndicatorsOfCompromiseApi.md#delete_all_ioc) | **delete** /v1/ioc/delete/all | Delete all existing Indicators of Compromise
*IndicatorsOfCompromiseApi* | [**delete_ioc_by_ids**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/IndicatorsOfCompromiseApi.md#delete_ioc_by_ids) | **delete** /v1/ioc/delete | Delete Indicators of Compromise by ID
*IndicatorsOfCompromiseApi* | [**edit_ioc**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/IndicatorsOfCompromiseApi.md#edit_ioc) | **put** /v1/ioc/edit | Update existing Indicators of Compromise
*IndicatorsOfCompromiseApi* | [**get_ioc_paged**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/IndicatorsOfCompromiseApi.md#get_ioc_paged) | **post** /v1/ioc/get | Get existing Indicators of Compromise
*JobsApi* | [**get_job_by_id**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/JobsApi.md#get_job_by_id) | **get** /v1/jobs/{jobId} | Retrieve the status and result of an asynchronous operation
*OrganizationalStructureApi* | [**add_members_to_virtual_group**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/OrganizationalStructureApi.md#add_members_to_virtual_group) | **put** /v1/organization/virtual-group/{virtualGroupId}/members/add | Add entities to a Virtual Group
*OrganizationalStructureApi* | [**create**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/OrganizationalStructureApi.md#create) | **post** /v1/organization/virtual-group/create | Create a new Virtual Group
*OrganizationalStructureApi* | [**remove_members_from_virtual_group**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/OrganizationalStructureApi.md#remove_members_from_virtual_group) | **put** /v1/organization/virtual-group/{virtualGroupId}/members/remove | Remove entities from a Virtual Group
*OrganizationalStructureApi* | [**search_in_organization**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/OrganizationalStructureApi.md#search_in_organization) | **post** /v1/organization/tree/search | Search the organization for entities matching a query
*PolicyGeneralApi* | [**add_rule_assignments**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#add_rule_assignments) | **put** /v1/policy/{ruleId}/assignments/add | Assign entities to a given rule
*PolicyGeneralApi* | [**clone_rule**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#clone_rule) | **post** /v1/policy/{ruleId} | Clones the specified rule and puts the clone in the provided position inside the rulebase
*PolicyGeneralApi* | [**get_all_rules_metadata**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#get_all_rules_metadata) | **get** /v1/policy/metadata | Get the metadata of all rules
*PolicyGeneralApi* | [**get_modifications_pending_installation_by_rule_id**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#get_modifications_pending_installation_by_rule_id) | **get** /v1/policy/{ruleId}/modifications | Get information on modifications to a given rule
*PolicyGeneralApi* | [**get_rule_assignments**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#get_rule_assignments) | **get** /v1/policy/{ruleId}/assignments | Get entities assigned to a rule
*PolicyGeneralApi* | [**get_rule_metadata_by_id**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#get_rule_metadata_by_id) | **get** /v1/policy/{ruleId}/metadata | Get a rule&#x27;s metadata
*PolicyGeneralApi* | [**install_all_policies**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#install_all_policies) | **post** /v1/policy/install | Install all policies
*PolicyGeneralApi* | [**install_policies_for_rule**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#install_policies_for_rule) | **post** /v1/policy/{ruleId}/install | Install all policies of a given rule
*PolicyGeneralApi* | [**remove_rule_assignments**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyGeneralApi.md#remove_rule_assignments) | **put** /v1/policy/{ruleId}/assignments/remove | Remove entities from a rule
*PolicyThreatPreventionApi* | [**get_threat_prevention_policy**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyThreatPreventionApi.md#get_threat_prevention_policy) | **get** /policy/threat-prevention/{ruleId} | Get a rule&#x27;s Threat-Prevention policy
*PolicyThreatPreventionApi* | [**set_threat_prevention_policy**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyThreatPreventionApi.md#set_threat_prevention_policy) | **patch** /policy/threat-prevention/{ruleId} | Update a rule&#x27;s Threat-Prevention policy
*PolicyThreatPreventionApi* | [**set_threat_prevention_policy_template**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PolicyThreatPreventionApi.md#set_threat_prevention_policy_template) | **put** /policy/threat-prevention/{ruleId}/template | Sets a rule&#x27;s Threat-Prevention policy template
*PostureManagementVulnerabilitiesApi* | [**get_device_vulnerabilities_device**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PostureManagementVulnerabilitiesApi.md#get_device_vulnerabilities_device) | **post** /v1/posture/vulnerability/devices | Get vulnerabilities of given devices
*PostureManagementVulnerabilitiesApi* | [**get_vulnerabilities_data**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PostureManagementVulnerabilitiesApi.md#get_vulnerabilities_data) | **get** /v1/posture/vulnerability/data | Get information about vulnerabilities
*PostureManagementVulnerabilitiesApi* | [**vulnerability_patch**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PostureManagementVulnerabilitiesApi.md#vulnerability_patch) | **post** /v1/posture/vulnerability/patch | Patch vulnerable applications
*PostureManagementVulnerabilitiesApi* | [**vulnerability_patch_status**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PostureManagementVulnerabilitiesApi.md#vulnerability_patch_status) | **post** /v1/posture/vulnerability/patch/status | Get patch operation statuses
*PostureManagementVulnerabilitiesApi* | [**vulnerability_scan**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PostureManagementVulnerabilitiesApi.md#vulnerability_scan) | **post** /v1/posture/vulnerability/scan | Start a vulnerability scan on given devices
*PostureManagementVulnerabilitiesApi* | [**vulnerability_scan_status**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/PostureManagementVulnerabilitiesApi.md#vulnerability_scan_status) | **post** /v1/posture/vulnerability/scan/status | Get a vulnerability scan&#x27;s status
*QuarantineManagementApi* | [**get_quarantine_file_data**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/QuarantineManagementApi.md#get_quarantine_file_data) | **get** /v1/quarantine-management/file/data | 
*QuarantineManagementApi* | [**get_quarantine_file_data_by_device**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/QuarantineManagementApi.md#get_quarantine_file_data_by_device) | **post** /v1/quarantine-management/file/data | 
*QuarantineManagementApi* | [**quarantine_file_fetch**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/QuarantineManagementApi.md#quarantine_file_fetch) | **post** /v1/quarantine-management/file/fetch | 
*QuarantineManagementApi* | [**quarantine_file_restore**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/QuarantineManagementApi.md#quarantine_file_restore) | **post** /v1/quarantine-management/file/restore | 
*RemediationResponseAgentApi* | [**agent_add_registry_key**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_add_registry_key) | **post** /v1/remediation/agent/registry/key/add | Add a registry key and/or value to computers matching the given query
*RemediationResponseAgentApi* | [**agent_add_vpn_site**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_add_vpn_site) | **post** /v1/remediation/agent/vpn/site/add | Add the VPN Site&#x27;s configuration to computers matching the given query
*RemediationResponseAgentApi* | [**agent_collect_process_information**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_collect_process_information) | **post** /v1/remediation/agent/process/information | Collect information about processes on computers matching the given query
*RemediationResponseAgentApi* | [**agent_copy_file**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_copy_file) | **post** /v1/remediation/agent/file/copy | Copy a given file on computers matching the given query
*RemediationResponseAgentApi* | [**agent_delete_file**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_delete_file) | **post** /v1/remediation/agent/file/delete | Delete a given file on computers matching the given query
*RemediationResponseAgentApi* | [**agent_move_file**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_move_file) | **post** /v1/remediation/agent/file/move | Move a given file on computers matching the given query
*RemediationResponseAgentApi* | [**agent_remove_registry_key**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_remove_registry_key) | **post** /v1/remediation/agent/registry/key/delete | Remove a registry key or value to computers matching the given query
*RemediationResponseAgentApi* | [**agent_remove_vpn_site**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_remove_vpn_site) | **post** /v1/remediation/agent/vpn/site/remove | Remove the given VPN Site&#x27;s configuration to computers matching the given query
*RemediationResponseAgentApi* | [**agent_terminate_process**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#agent_terminate_process) | **post** /v1/remediation/agent/process/terminate | Terminate the given process on computers matching the given query
*RemediationResponseAgentApi* | [**collect_logs**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#collect_logs) | **post** /v1/remediation/agent/collect-logs | Collect diagnostic information from computers matching a given query
*RemediationResponseAgentApi* | [**repair_computer**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#repair_computer) | **post** /v1/remediation/agent/repair-computer | Repair client installations on computers matching a given query
*RemediationResponseAgentApi* | [**reset_computer**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#reset_computer) | **post** /v1/remediation/agent/reset-computer | Restart computers matching a given query
*RemediationResponseAgentApi* | [**shutdown_computer**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseAgentApi.md#shutdown_computer) | **post** /v1/remediation/agent/shutdown-computer | Shut-down computers matching a given query
*RemediationResponseGeneralApi* | [**abort_remediation_operation_by_id**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseGeneralApi.md#abort_remediation_operation_by_id) | **post** /v1/remediation/{id}/abort | Abort a given Remediation Operation
*RemediationResponseGeneralApi* | [**get_all_remediation_operation_statuses**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseGeneralApi.md#get_all_remediation_operation_statuses) | **get** /v1/remediation/status | Get the status of all Remediation Operations
*RemediationResponseGeneralApi* | [**get_remediation_operation_slim_results_by_id**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseGeneralApi.md#get_remediation_operation_slim_results_by_id) | **post** /v1/remediation/{id}/results/slim | Get the results of a given Remediation Operation.
*RemediationResponseGeneralApi* | [**get_remediation_operation_status_by_id**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseGeneralApi.md#get_remediation_operation_status_by_id) | **get** /v1/remediation/{id}/status | Get the status of a given Remediation Operation
*RemediationResponseThreatPreventionApi* | [**analyze_by_file_name**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#analyze_by_file_name) | **post** /v1/remediation/forensics/analyze-by-indicator/file-name | Collect forensic information on computers matching a given query
*RemediationResponseThreatPreventionApi* | [**analyze_by_ip**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#analyze_by_ip) | **post** /v1/remediation/forensics/analyze-by-indicator/ip | Collect forensic information on computers matching a given query
*RemediationResponseThreatPreventionApi* | [**analyze_by_md5**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#analyze_by_md5) | **post** /v1/remediation/forensics/analyze-by-indicator/md5 | Collect forensic information on computers matching a given query
*RemediationResponseThreatPreventionApi* | [**analyze_by_path**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#analyze_by_path) | **post** /v1/remediation/forensics/analyze-by-indicator/path | Collect forensic information on computers matching a given query
*RemediationResponseThreatPreventionApi* | [**analyze_by_url**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#analyze_by_url) | **post** /v1/remediation/forensics/analyze-by-indicator/url | Collect forensic information on computers matching a given query
*RemediationResponseThreatPreventionApi* | [**anti_malware_restore**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#anti_malware_restore) | **post** /v1/remediation/anti-malware/restore | Restore a file that was quarantined by the Harmony Endpoint Client&#x27;s Anti-Malware
*RemediationResponseThreatPreventionApi* | [**anti_malware_scan**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#anti_malware_scan) | **post** /v1/remediation/anti-malware/scan | Perform an Anti-Malware scan on computers matching a query
*RemediationResponseThreatPreventionApi* | [**anti_malware_update**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#anti_malware_update) | **post** /v1/remediation/anti-malware/update | Update the Anti-Malware Signature Database on computers matching a query
*RemediationResponseThreatPreventionApi* | [**de_isolate_computer**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#de_isolate_computer) | **post** /v1/remediation/de-isolate | De-isolate computers matching a given query
*RemediationResponseThreatPreventionApi* | [**isolate_computer**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#isolate_computer) | **post** /v1/remediation/isolate | Isolate computers matching a given query
*RemediationResponseThreatPreventionApi* | [**quarantine_file**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#quarantine_file) | **post** /v1/remediation/forensics/file/quarantine | Quarantine given files on computers matching a given query
*RemediationResponseThreatPreventionApi* | [**restore_quarantined_file**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/RemediationResponseThreatPreventionApi.md#restore_quarantined_file) | **post** /v1/remediation/forensics/file/restore | Restore given file from quarantine on computers matching a given query
*SessionApi* | [**keep_alive**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/SessionApi.md#keep_alive) | **post** /v1/session/keepalive | Refresh an API work-session
*SessionApi* | [**login_cloud**](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/apis/tags/SessionApi.md#login_cloud) | **post** /v1/session/login/cloud | Create a new API work-session

## Documentation For Models

 - [AcknowledgeResponse](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AcknowledgeResponse.md)
 - [AddRegistryKeyParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AddRegistryKeyParams.md)
 - [AddVpnSiteParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AddVpnSiteParams.md)
 - [AgentCollectLogsDetailsLevel](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AgentCollectLogsDetailsLevel.md)
 - [AgentCollectLogsOperationProtocol](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AgentCollectLogsOperationProtocol.md)
 - [AgentCollectLogsParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AgentCollectLogsParameters.md)
 - [AgentRebootOrShutdownParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AgentRebootOrShutdownParameters.md)
 - [AmRestoreParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AmRestoreParameters.md)
 - [AmScanParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AmScanParameters.md)
 - [AmTreatment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AmTreatment.md)
 - [AmUpdateParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AmUpdateParameters.md)
 - [AnonymousBrowsingMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AnonymousBrowsingMode.md)
 - [AntiBot](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AntiBot.md)
 - [AntiMalware](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AntiMalware.md)
 - [AnyFamily](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AnyFamily.md)
 - [ApplianceEmulationEnvironment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ApplianceEmulationEnvironment.md)
 - [AssetView](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/AssetView.md)
 - [BaseFileRelocationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BaseFileRelocationParams.md)
 - [BasePushOperationParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BasePushOperationParameters.md)
 - [BasePushOperationRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BasePushOperationRequest.md)
 - [BehavioralGuardRestoration](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BehavioralGuardRestoration.md)
 - [BehavioralGuardRestorationMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BehavioralGuardRestorationMode.md)
 - [BladeAntiBot](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BladeAntiBot.md)
 - [BladeAntiMalware](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BladeAntiMalware.md)
 - [BladeFamily](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BladeFamily.md)
 - [BladeForensics](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BladeForensics.md)
 - [BladeThreatEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BladeThreatEmulation.md)
 - [BlockBitLockerOptions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BlockBitLockerOptions.md)
 - [BrowserExtension](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BrowserExtension.md)
 - [BrowserExtensionSettings](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/BrowserExtensionSettings.md)
 - [CapabilityMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CapabilityMode.md)
 - [CleaningMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CleaningMode.md)
 - [CloneRulePositionAbove](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CloneRulePositionAbove.md)
 - [CloneRulePositionBelow](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CloneRulePositionBelow.md)
 - [CloneRulePositionTop](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CloneRulePositionTop.md)
 - [CollectProcessInformationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CollectProcessInformationParams.md)
 - [Computer](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/Computer.md)
 - [ComputerColumnNames](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ComputerColumnNames.md)
 - [ComputerType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ComputerType.md)
 - [ComputersByFilterArgs](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ComputersByFilterArgs.md)
 - [ComputersByFilterPaging](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ComputersByFilterPaging.md)
 - [ComputersByUnlimitedFilterArgs](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ComputersByUnlimitedFilterArgs.md)
 - [ComputersQuery](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ComputersQuery.md)
 - [ConnectionState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ConnectionState.md)
 - [ConnectionStates](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ConnectionStates.md)
 - [CreateVirtualGroupRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CreateVirtualGroupRequest.md)
 - [CustomIocState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CustomIocState.md)
 - [CustomSetting](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/CustomSetting.md)
 - [DaWinPatchInformation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DaWinPatchInformation.md)
 - [DeleteFileParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DeleteFileParams.md)
 - [DeploymentStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DeploymentStatus.md)
 - [DetailedVulnerabilityPatchStatusEnum](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DetailedVulnerabilityPatchStatusEnum.md)
 - [DetailsLevel](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DetailsLevel.md)
 - [DeviceVulnerabilityInfo](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DeviceVulnerabilityInfo.md)
 - [DeviceVulnerabilityPatchInfo](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DeviceVulnerabilityPatchInfo.md)
 - [DeviceVulnerabilityScanStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DeviceVulnerabilityScanStatus.md)
 - [DeviceVulnerabilityScanStatusEnum](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DeviceVulnerabilityScanStatusEnum.md)
 - [DomainPermission](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DomainPermission.md)
 - [DownloadProtectionExtractMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/DownloadProtectionExtractMode.md)
 - [Efr](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/Efr.md)
 - [EmonView](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EmonView.md)
 - [EmulationEnvironment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EmulationEnvironment.md)
 - [EmulationEnvironmentMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EmulationEnvironmentMode.md)
 - [EmulationEnvironmentType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EmulationEnvironmentType.md)
 - [EndpointClientSensorType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EndpointClientSensorType.md)
 - [EndpointForServers](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EndpointForServers.md)
 - [EndpointTypeStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EndpointTypeStatus.md)
 - [EntityType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/EntityType.md)
 - [ErrorSource](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorSource.md)
 - [ErrorSourceClient](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorSourceClient.md)
 - [ErrorSourceUnknown](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorSourceUnknown.md)
 - [ErrorTypes](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypes.md)
 - [ErrorTypesGeneric](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypesGeneric.md)
 - [ErrorTypesGenericForbidden](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypesGenericForbidden.md)
 - [ErrorTypesGenericUnauthorized](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypesGenericUnauthorized.md)
 - [ErrorTypesMissingApiToken](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypesMissingApiToken.md)
 - [ErrorTypesMissingCiToken](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypesMissingCiToken.md)
 - [ErrorTypesTsoaInputValidation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ErrorTypesTsoaInputValidation.md)
 - [ExtractionMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ExtractionMode.md)
 - [FailAction](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FailAction.md)
 - [FailCloseMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FailCloseMode.md)
 - [FdeRemoteOperation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FdeRemoteOperation.md)
 - [FetchQuarantinedFileParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FetchQuarantinedFileParams.md)
 - [FileReputationState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileReputationState.md)
 - [FileTransferProtocol](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileTransferProtocol.md)
 - [FileTransferServerConnection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileTransferServerConnection.md)
 - [FileTransferServerUploadParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileTransferServerUploadParams.md)
 - [FileTypeActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileTypeActions.md)
 - [FileTypeOverrideActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileTypeOverrideActions.md)
 - [FileUploadSupportedFilesMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileUploadSupportedFilesMode.md)
 - [FileUploadUnsupportedFilesMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FileUploadUnsupportedFilesMode.md)
 - [FilterType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FilterType.md)
 - [ForbiddenErrorExample](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForbiddenErrorExample.md)
 - [ForensicsAnalyzeByIndicatorParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForensicsAnalyzeByIndicatorParameters.md)
 - [ForensicsQuarantineItem](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForensicsQuarantineItem.md)
 - [ForensicsQuarantineItemType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForensicsQuarantineItemType.md)
 - [ForensicsQuarantineOperationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForensicsQuarantineOperationParams.md)
 - [ForensicsRemediationItem](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForensicsRemediationItem.md)
 - [ForensicsTriggerCondition](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ForensicsTriggerCondition.md)
 - [FreeSearchFilterType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/FreeSearchFilterType.md)
 - [GetPolicyResult](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/GetPolicyResult.md)
 - [IBaseGroup](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBaseGroup.md)
 - [IBehavioralProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBehavioralProtection.md)
 - [IBehavioralProtectionAntiRansomware](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBehavioralProtectionAntiRansomware.md)
 - [IBehavioralProtectionBackup](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBehavioralProtectionBackup.md)
 - [IBehavioralProtectionBackupFileTypes](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBehavioralProtectionBackupFileTypes.md)
 - [IBehavioralProtectionEdr](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBehavioralProtectionEdr.md)
 - [IBehavioralProtectionForensics](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBehavioralProtectionForensics.md)
 - [IBotProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBotProtection.md)
 - [IBotProtectionConfidenceThresholds](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBotProtectionConfidenceThresholds.md)
 - [IBotProtectionConnectionInspectionModeEnum](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBotProtectionConnectionInspectionModeEnum.md)
 - [IBotProtectionReporting](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBotProtectionReporting.md)
 - [IBotProtectionSslInspection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IBotProtectionSslInspection.md)
 - [ICapabilities](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ICapabilities.md)
 - [ICloneRuleInput](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ICloneRuleInput.md)
 - [IComputerList](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IComputerList.md)
 - [IExploitProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IExploitProtection.md)
 - [IFilesProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtection.md)
 - [IFilesProtectionBrowser](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionBrowser.md)
 - [IFilesProtectionEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulation.md)
 - [IFilesProtectionEmulationDownload](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationDownload.md)
 - [IFilesProtectionEmulationDownloadFileActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationDownloadFileActions.md)
 - [IFilesProtectionEmulationDownloadFileActionsFileTypeOverrides](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationDownloadFileActionsFileTypeOverrides.md)
 - [IFilesProtectionEmulationDownloadThreatExtraction](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationDownloadThreatExtraction.md)
 - [IFilesProtectionEmulationDownloadThreatExtractionElements](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationDownloadThreatExtractionElements.md)
 - [IFilesProtectionEmulationFileSystemFileTypesOverrides](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationFileSystemFileTypesOverrides.md)
 - [IFilesProtectionEmulationUnsupportedFileTypeActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationUnsupportedFileTypeActions.md)
 - [IFilesProtectionEmulationUpload](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationUpload.md)
 - [IFilesProtectionEmulationUploadFileActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationUploadFileActions.md)
 - [IFilesProtectionEmulationUploadFileActionsFileTypeOverrides](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationUploadFileActionsFileTypeOverrides.md)
 - [IFilesProtectionEmulationUploadFileProtectionDomainsActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilesProtectionEmulationUploadFileProtectionDomainsActions.md)
 - [IFilter](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IFilter.md)
 - [IMalwareProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtection.md)
 - [IMalwareProtectionScan](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScan.md)
 - [IMalwareProtectionScanOnAccessScan](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScanOnAccessScan.md)
 - [IMalwareProtectionScanOnAccessScanReputationServices](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScanOnAccessScanReputationServices.md)
 - [IMalwareProtectionScanRandomizedScan](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScanRandomizedScan.md)
 - [IMalwareProtectionScanScanOnIdle](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScanScanOnIdle.md)
 - [IMalwareProtectionScanScanTargets](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScanScanTargets.md)
 - [IMalwareProtectionScanScheduledScan](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionScanScheduledScan.md)
 - [IMalwareProtectionSignatures](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionSignatures.md)
 - [IMalwareProtectionSignaturesSignatureServers](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionSignaturesSignatureServers.md)
 - [IMalwareProtectionTreatment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionTreatment.md)
 - [IMalwareProtectionTreatmentTreatmentRiskware](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IMalwareProtectionTreatmentTreatmentRiskware.md)
 - [IPasswordReuseProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IPasswordReuseProtection.md)
 - [IPhishingProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IPhishingProtection.md)
 - [IRemediation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IRemediation.md)
 - [IRemediationFile](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IRemediationFile.md)
 - [IRemediationQuarantine](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IRemediationQuarantine.md)
 - [ISearchProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ISearchProtection.md)
 - [IThreatPreventionPolicy](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IThreatPreventionPolicy.md)
 - [IThreatPreventionProtections](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IThreatPreventionProtections.md)
 - [IThreatPreventionProtectionsNetwork](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IThreatPreventionProtectionsNetwork.md)
 - [IThreatPreventionProtectionsSystem](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IThreatPreventionProtectionsSystem.md)
 - [IThreatPreventionRemediation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IThreatPreventionRemediation.md)
 - [IUrlFilteringProtection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IUrlFilteringProtection.md)
 - [IUrlFilteringProtectionUserOverrides](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IUrlFilteringProtectionUserOverrides.md)
 - [IUrlFilteringProtectionUserOverridesRules](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IUrlFilteringProtectionUserOverridesRules.md)
 - [Id](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/Id.md)
 - [IndicatorOfCompromise](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IndicatorOfCompromise.md)
 - [IndicatorOfCompromiseDto](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IndicatorOfCompromiseDto.md)
 - [InternalErrorExample](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/InternalErrorExample.md)
 - [IntervalPeriod](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IntervalPeriod.md)
 - [IocFieldsComment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IocFieldsComment.md)
 - [IocFieldsValue](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IocFieldsValue.md)
 - [IocPagedRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IocPagedRequest.md)
 - [IocType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/IocType.md)
 - [JobCreationResult](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobCreationResult.md)
 - [JobOrResultAcknowledgeResponse](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultAcknowledgeResponse.md)
 - [JobOrResultIComputerList](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultIComputerList.md)
 - [JobOrResultId](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultId.md)
 - [JobOrResultIndicatorOfCompromiseArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultIndicatorOfCompromiseArray.md)
 - [JobOrResultModifiedRule](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultModifiedRule.md)
 - [JobOrResultPageOfIoc](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultPageOfIoc.md)
 - [JobOrResultPushOperationClientResultSlimResponse](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultPushOperationClientResultSlimResponse.md)
 - [JobOrResultPushOperationCreationResult](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultPushOperationCreationResult.md)
 - [JobOrResultPushOperationId](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultPushOperationId.md)
 - [JobOrResultPushOperationStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultPushOperationStatus.md)
 - [JobOrResultPushOperationStatusArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultPushOperationStatusArray.md)
 - [JobOrResultQuarantinedFileArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultQuarantinedFileArray.md)
 - [JobOrResultRuleAssignmentArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultRuleAssignmentArray.md)
 - [JobOrResultRuleMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultRuleMetadata.md)
 - [JobOrResultRuleMetadataArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultRuleMetadataArray.md)
 - [JobOrResultSlimEntityArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultSlimEntityArray.md)
 - [JobOrResultVulnerabilityPatchStatusArray](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultVulnerabilityPatchStatusArray.md)
 - [JobOrResultVulnerableDeviceSearchResults](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobOrResultVulnerableDeviceSearchResults.md)
 - [JobState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobState.md)
 - [JobStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/JobStatus.md)
 - [LegacyBladeFamily](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/LegacyBladeFamily.md)
 - [LimitedIocSorting](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/LimitedIocSorting.md)
 - [LoginCredentials](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/LoginCredentials.md)
 - [LoginResponse](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/LoginResponse.md)
 - [LogsMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/LogsMode.md)
 - [MissingApiTokenErrorExample](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/MissingApiTokenErrorExample.md)
 - [MissingCITokenErrorExample](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/MissingCITokenErrorExample.md)
 - [ModifiedRule](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ModifiedRule.md)
 - [NonePrimarySignatureServerType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/NonePrimarySignatureServerType.md)
 - [NotificationsMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/NotificationsMode.md)
 - [OfflineReputationState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/OfflineReputationState.md)
 - [OffsetPosture](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/OffsetPosture.md)
 - [OffsetQuarantine](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/OffsetQuarantine.md)
 - [OperatingSystemSlimInfo](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/OperatingSystemSlimInfo.md)
 - [OperatingSystemType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/OperatingSystemType.md)
 - [PageOfIoc](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PageOfIoc.md)
 - [PageSizePosture](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PageSizePosture.md)
 - [PageSizeQuarantine](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PageSizeQuarantine.md)
 - [PagedResponseMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PagedResponseMetadata.md)
 - [Paging](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/Paging.md)
 - [PolicyOrientation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicyOrientation.md)
 - [PolicySettingsIBehavioralProtectionBladeForensics](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIBehavioralProtectionBladeForensics.md)
 - [PolicySettingsIBehavioralProtectionBladeForensicsMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIBehavioralProtectionBladeForensicsMetadata.md)
 - [PolicySettingsIBotProtectionBladeAntiBot](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIBotProtectionBladeAntiBot.md)
 - [PolicySettingsIExploitProtectionBladeThreatEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIExploitProtectionBladeThreatEmulation.md)
 - [PolicySettingsIFilesProtectionBladeThreatEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIFilesProtectionBladeThreatEmulation.md)
 - [PolicySettingsIFilesProtectionBladeThreatEmulationMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIFilesProtectionBladeThreatEmulationMetadata.md)
 - [PolicySettingsIMalwareProtectionBladeAntiMalware](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIMalwareProtectionBladeAntiMalware.md)
 - [PolicySettingsIMalwareProtectionBladeAntiMalwareMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIMalwareProtectionBladeAntiMalwareMetadata.md)
 - [PolicySettingsIPasswordReuseProtectionBladeThreatEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIPasswordReuseProtectionBladeThreatEmulation.md)
 - [PolicySettingsIPhishingProtectionBladeThreatEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIPhishingProtectionBladeThreatEmulation.md)
 - [PolicySettingsIRemediationBladeForensics](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIRemediationBladeForensics.md)
 - [PolicySettingsISearchProtectionBladeAntiBot](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsISearchProtectionBladeAntiBot.md)
 - [PolicySettingsIUrlFilteringProtectionBladeAntiBot](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIUrlFilteringProtectionBladeAntiBot.md)
 - [PolicySettingsIUrlFilteringProtectionBladeAntiBotMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicySettingsIUrlFilteringProtectionBladeAntiBotMetadata.md)
 - [PolicyTemplateName](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PolicyTemplateName.md)
 - [PossibleOperationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PossibleOperationParams.md)
 - [Posture](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/Posture.md)
 - [PosturePaging](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PosturePaging.md)
 - [ProcessProperties](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ProcessProperties.md)
 - [ProtectedNetworkResourceDomain](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ProtectedNetworkResourceDomain.md)
 - [ProtectedNetworkResourceIpRange](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ProtectedNetworkResourceIpRange.md)
 - [PushOperationClientMachineInfoSlim](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationClientMachineInfoSlim.md)
 - [PushOperationClientOperationStatusSlim](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationClientOperationStatusSlim.md)
 - [PushOperationClientOperationStatusSlimResponse](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationClientOperationStatusSlimResponse.md)
 - [PushOperationClientResultSlim](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationClientResultSlim.md)
 - [PushOperationClientResultSlimResponse](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationClientResultSlimResponse.md)
 - [PushOperationClientStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationClientStatus.md)
 - [PushOperationCreationResult](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationCreationResult.md)
 - [PushOperationId](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationId.md)
 - [PushOperationOverallStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationOverallStatus.md)
 - [PushOperationRequestAgentCollectLogsParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestAgentCollectLogsParameters.md)
 - [PushOperationRequestAgentRebootOrShutdownParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestAgentRebootOrShutdownParameters.md)
 - [PushOperationRequestAmRestoreParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestAmRestoreParameters.md)
 - [PushOperationRequestAmScanParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestAmScanParameters.md)
 - [PushOperationRequestAmUpdateParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestAmUpdateParameters.md)
 - [PushOperationRequestBasePushOperationParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestBasePushOperationParameters.md)
 - [PushOperationRequestCollectProcessInformationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestCollectProcessInformationParams.md)
 - [PushOperationRequestWithMandatoryParamsAddRegistryKeyParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsAddRegistryKeyParams.md)
 - [PushOperationRequestWithMandatoryParamsAddVpnSiteParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsAddVpnSiteParams.md)
 - [PushOperationRequestWithMandatoryParamsBaseFileRelocationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsBaseFileRelocationParams.md)
 - [PushOperationRequestWithMandatoryParamsDeleteFileParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsDeleteFileParams.md)
 - [PushOperationRequestWithMandatoryParamsFetchQuarantinedFileParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsFetchQuarantinedFileParams.md)
 - [PushOperationRequestWithMandatoryParamsForensicsAnalyzeByIndicatorParameters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsForensicsAnalyzeByIndicatorParameters.md)
 - [PushOperationRequestWithMandatoryParamsForensicsQuarantineOperationParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsForensicsQuarantineOperationParams.md)
 - [PushOperationRequestWithMandatoryParamsRemoveRegistryKeyParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsRemoveRegistryKeyParams.md)
 - [PushOperationRequestWithMandatoryParamsRemoveVpnSiteParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsRemoveVpnSiteParams.md)
 - [PushOperationRequestWithMandatoryParamsRestoreQuarantinedFileParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsRestoreQuarantinedFileParams.md)
 - [PushOperationRequestWithMandatoryParamsTerminateProcessParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationRequestWithMandatoryParamsTerminateProcessParams.md)
 - [PushOperationResultsRequestFilters](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationResultsRequestFilters.md)
 - [PushOperationResultsRequestSlim](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationResultsRequestSlim.md)
 - [PushOperationSchedulingType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationSchedulingType.md)
 - [PushOperationSlimResultsRequestPaging](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationSlimResultsRequestPaging.md)
 - [PushOperationStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationStatus.md)
 - [PushOperationTargeting](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationTargeting.md)
 - [PushOperationTiming](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationTiming.md)
 - [PushOperationType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/PushOperationType.md)
 - [QuarantineManagementFileByDeviceNameRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantineManagementFileByDeviceNameRequest.md)
 - [QuarantineManagementFileByDeviceNameRequestDevice](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantineManagementFileByDeviceNameRequestDevice.md)
 - [QuarantinePaging](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantinePaging.md)
 - [QuarantinedFile](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantinedFile.md)
 - [QuarantinedFileDevice](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantinedFileDevice.md)
 - [QuarantinedFileFile](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantinedFileFile.md)
 - [QuarantinedFileMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/QuarantinedFileMetadata.md)
 - [RegistryHive](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RegistryHive.md)
 - [RegistryValueType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RegistryValueType.md)
 - [RemediationAction](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RemediationAction.md)
 - [RemediationMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RemediationMode.md)
 - [RemediationTrustedAction](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RemediationTrustedAction.md)
 - [RemediationType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RemediationType.md)
 - [RemoveRegistryKeyParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RemoveRegistryKeyParams.md)
 - [RemoveVpnSiteParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RemoveVpnSiteParams.md)
 - [RestoreQuarantinedFileParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RestoreQuarantinedFileParams.md)
 - [RiskLevel](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RiskLevel.md)
 - [RuleAssignment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleAssignment.md)
 - [RuleAssignmentsModification](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleAssignmentsModification.md)
 - [RuleId](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleId.md)
 - [RuleMetadata](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleMetadata.md)
 - [RuleModifications](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleModifications.md)
 - [RuleOrderModification](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleOrderModification.md)
 - [RulePositionRelative](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RulePositionRelative.md)
 - [RulePositionTop](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RulePositionTop.md)
 - [RuleSettingsModifications](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleSettingsModifications.md)
 - [RuleTemplateAssignment](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RuleTemplateAssignment.md)
 - [RunAsJob](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RunAsJob.md)
 - [RunAsJobONOn](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RunAsJobONOn.md)
 - [RunAsJobOn](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/RunAsJobOn.md)
 - [SSLInspectionMode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SSLInspectionMode.md)
 - [SearchInOrganizationRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SearchInOrganizationRequest.md)
 - [SearchableEntityTypes](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SearchableEntityTypes.md)
 - [Sections](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/Sections.md)
 - [ServerOptimizationTemplate](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ServerOptimizationTemplate.md)
 - [SignatureServerType](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SignatureServerType.md)
 - [SlimDeviceParentNode](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SlimDeviceParentNode.md)
 - [SlimDeviceParentNodeNodeTypeEnum](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SlimDeviceParentNodeNodeTypeEnum.md)
 - [SlimEntity](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SlimEntity.md)
 - [SortDirection](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/SortDirection.md)
 - [StandardTimestamp](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/StandardTimestamp.md)
 - [StandardToggleState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/StandardToggleState.md)
 - [StandardizedTimestamp](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/StandardizedTimestamp.md)
 - [StaticAnalysisFileTypes](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/StaticAnalysisFileTypes.md)
 - [StaticAnalysisState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/StaticAnalysisState.md)
 - [StatusCodes](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/StatusCodes.md)
 - [TargetComputer](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TargetComputer.md)
 - [TargetingExclusions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TargetingExclusions.md)
 - [TargetingInclusions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TargetingInclusions.md)
 - [TeImage](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TeImage.md)
 - [TeUnsupportedFileAction](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TeUnsupportedFileAction.md)
 - [TemplateAssignmentState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TemplateAssignmentState.md)
 - [TerminateProcessParams](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/TerminateProcessParams.md)
 - [ThreatEmulation](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ThreatEmulation.md)
 - [ThreatEmulationAppliance](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ThreatEmulationAppliance.md)
 - [ThreatPreventionSensors](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/ThreatPreventionSensors.md)
 - [UnauthorizedErrorExample](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UnauthorizedErrorExample.md)
 - [UnprocessableEntryErrorExample](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UnprocessableEntryErrorExample.md)
 - [UpdateIoc](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UpdateIoc.md)
 - [UploadFileTypeActions](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UploadFileTypeActions.md)
 - [UrlFilteringCategoryAction](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UrlFilteringCategoryAction.md)
 - [UrlFilteringCategoryNames](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UrlFilteringCategoryNames.md)
 - [UrlFilteringCategoryRule](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/UrlFilteringCategoryRule.md)
 - [VirtualGroupMembers](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VirtualGroupMembers.md)
 - [VpnSiteAuth](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VpnSiteAuth.md)
 - [VpnSiteAuthMethod](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VpnSiteAuthMethod.md)
 - [VpnSiteCustomAuth](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VpnSiteCustomAuth.md)
 - [VpnSiteCustomAuthMethod](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VpnSiteCustomAuthMethod.md)
 - [VulnerabilityAffectedDevice](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityAffectedDevice.md)
 - [VulnerabilityAffectedDeviceInfo](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityAffectedDeviceInfo.md)
 - [VulnerabilityPatchRequestFilter](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPatchRequestFilter.md)
 - [VulnerabilityPatchStatus](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPatchStatus.md)
 - [VulnerabilityPatchStatusDevice](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPatchStatusDevice.md)
 - [VulnerabilityPatchStatusEnum](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPatchStatusEnum.md)
 - [VulnerabilityPatchStatusPatch](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPatchStatusPatch.md)
 - [VulnerabilityPatchStatusVulnerability](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPatchStatusVulnerability.md)
 - [VulnerabilityPosturePatchStatusRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityPosturePatchStatusRequest.md)
 - [VulnerabilityScanRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityScanRequest.md)
 - [VulnerabilityScanRequestPaging](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityScanRequestPaging.md)
 - [VulnerabilityScanStatusRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerabilityScanStatusRequest.md)
 - [VulnerableApplicationInfoSlim](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerableApplicationInfoSlim.md)
 - [VulnerableDeviceSearchResults](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerableDeviceSearchResults.md)
 - [VulnerableDevicesByIdPagedRequest](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerableDevicesByIdPagedRequest.md)
 - [VulnerableDriverProtectionState](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/VulnerableDriverProtectionState.md)
 - [WeekDay](chkp_harmony_endpoint_management_sdk/generated/cloud/docs/models/WeekDay.md)

## Documentation For Authorization

Authentication schemes defined for the API:
<a id="cloudInfraJwt"></a>
### cloudInfraJwt

- **Type**: Bearer authentication (Infinity Portal Token)

<a id="apiJwt"></a>
### apiJwt

- **Type**: API key
- **API key parameter name**: x-mgmt-api-token
- **Location**: HTTP header


## Author

harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com
harmony-endpoint-external-api@checkpoint.com

## Notes for Large OpenAPI documents
If the OpenAPI document is large, imports in chkp_harmony_endpoint_management_sdk.generated.cloud.apis and chkp_harmony_endpoint_management_sdk.generated.cloud.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.default_api import DefaultApi`
- `from chkp_harmony_endpoint_management_sdk.generated.cloud.model.pet import Pet`

Solution 1:
Before importing the package, adjust the maximum recursion limit as shown below:
```
import sys
sys.setrecursionlimit(1500)
import chkp_harmony_endpoint_management_sdk.generated.cloud
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis import *
from chkp_harmony_endpoint_management_sdk.generated.cloud.models import *
```
