# coding: utf-8

# flake8: noqa

"""
    Harmony Endpoint Management API

    <style>details{user-select:none}details>summary span.icon{width:24px;height:24px;transition:all .3s;margin-left:auto}details>ol>li{padding-bottom:20px}summary{cursor:pointer}summary::-webkit-details-marker{display:none}</style><h2>Today more than ever, endpoint security plays a critical role in enabling your remote workforce.</h2><h4>Harmony Endpoint provides comprehensive endpoint protection at the highest security level that is crucial to avoid security breaches and data compromise.</h4><p>The following documentation provides the operations supported by the Harmony Endpoint's External API.</p><p>To use the Harmony Endpoint External API service:</p><ol><li><p>In the <em>Infinity Portal</em>, create a suitable API Key. In the <em>Service</em> field, enter <em>Endpoint</em>.<br>For more information, refer to the <a href=\"https://sc1.checkpoint.com/documents/Infinity_Portal/WebAdminGuides/EN/Infinity-Portal-Admin-Guide/Content/Topics-Infinity-Portal/API-Keys.htm?tocpath=Global%20Settings%7C_____7#API_Keys\">Infinity Portal Administration Guide</a>.<br>Once a key has been created, it may be used indefinitely (unless an expiration date was explicitly set for it).</p>During the key's creation, note the presented <em>Authentication URL</em>. This URL is used to obtain <em>Bearer tokens</em> for the next step</li><li><p>Authenticate using the <em>Infinity Portal's</em> External Authentication Service.<br>The authentication request should be made to the <em>Authentication URL</em> obtained during the previous step.</p><p>Example (<em>Your tenant's authentication URL may differ</em>):</p><p><img src=\"data:image/png;base64,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\"></p><p>Note, image is for reference only. Exact <em>CURL</em> syntax may differ.</p></li><li><p>Include the resulting <em>token</em> in the <em>Authorization</em> header in the form of a <em>Bearer</em> (For example, 'Authorization': 'Bearer {TOKEN}') in every request made to the API service</p></li><li><p>Call the <a href=\"#/Session/LoginCloud\">Cloud Login API</a></p></li><li><p>Include the resulting <em>x-mgmt-api-token</em> in Header <em>x-mgmt-api-token</em> of all subsequent requests</p></li></ol><br><div><p>For your convinience, <em>Harmony Endpoint</em> API SDKs are available here:</p><ul><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-py-sdk\">Python 3.8 and newer</a></li><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-js-ts-sdk\">TypeScript</a></li></ul></div><div><p>In addition, a command-line interface is available <a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-cli\">here</a></p></div><br><div style=\"margin-top:15px;padding-top:30px;padding-bottom:30px\"><h3>Important Notes:</h3><div style=\"margin-left:25px\"><p></p><ul><li style=\"margin-bottom:30px\"><p>When creating an API key, the selected service <b><em>must</em></b> be <em>Endpoint</em> or requests will not be delivered to the service.</p></li><li style=\"margin-bottom:30px\"><p>Operation payload examples should be treated as guidelines and should not be used as-is.</p><p style=\"margin-top:-7px\">Calling a remediation operation, for instance, with the contents of its example will fail.</p></li><li style=\"margin-bottom:30px\"><p>The <em>Harmony Endpoint</em> API service enforces rate-limiting.</p><p style=\"margin-top:-7px\">Please ensure your integration correctly handles <code>HTTP 429 (Too many requests)</code> responses by using appropriate delays and back-off mechanisms.</p></li><li style=\"margin-bottom:30px\"><p>Errors returned by the <em>Harmony Endpoint</em> API service conform, to a large degree, to <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> and convey useful data.</p><p style=\"margin-top:-7px\">It is highly recommended your integration logs the full error as most issues can quickly be pinpointed and rectified by viewing the error contents.</p></li></ul><p></p></div></div><br><div style=\"padding-top:30px;padding-bottom:30px\"><details><summary style=\"font-size:large;font-weight:600;padding-bottom:20px\">Troubleshooting</summary><div style=\"margin-left:25px\"><p>During usage, you may encounter different issues and errors.</p><p>To facilitate resolution of such issues, the <em>Harmony Endpoint API service uses an <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> compliant error structure</em> which conveys information like the type of error that occurred and its source and even potential fixes.<br>This is the first and often last step in diagnosing API related issues.</p><p>The below list is of common errors that may not be obvious from the error message alone.</p><h5>Important notes</h5><ol><li>API errors may be wrapped by a separate object. The content of the errors however is as specified</li><li>Errors that do not follow <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> can be assumed to originate from <em>Infinity Portal</em> which implies a failure in authentication.</li></ol><p></p><p style=\"margin-top:40px\">If you encounter an error that is not listed here and require help, please open a support ticket or request assistance via the e-mail address at the bottom of this documentation page.</p><p style=\"padding-top:10px\">When opening a support ticket, please also provide the following information:</p><ul><li style=\"padding-bottom:8px\">The name and/or address of the API operation</li><li style=\"padding-bottom:8px\">The approximate date and time (including timezone) when you last encountered the issue</li><li style=\"padding-bottom:8px\"><p>The full request (body and headers).</p><p style=\"margin-top:-15px\">For issues pertaining to authentication/login, include your expired <em>Infinity Portal</em> bearer token.</p></li><li style=\"padding-bottom:8px\">The full response returned by the <em>Harmony Endpoint</em> API service</li><li style=\"padding-bottom:8px\">Your use case. For example, \"<em>Retrieving asset information for SIEM integration</em>\" (<b>Optional</b>)</li></ul><p></p><hr style=\"margin-top:25px;margin-bottom:25px\"><div style=\"margin-left:30px\"><details style=\"padding-bottom:15px\"><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"An error has occurred\" }</samp> when authenticating against the <em>Infinity Portal</em></summary><div><h4>Issue:</h4><p>This error usually indicates your authentication request was malformed.</p><h4>Possible Solutions:</h4><p>Make sure your request is a valid JSON, includes header <samp>Content-Type</samp> with a value of <samp>application/json</samp> and looks like <samp>{ \"clientId\": \"{{ciClientId}}\", \"accessKey\": \"{{ciAccessKey}}\" }</samp></p></div></details><details><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"Authentication required\", \"forceLogout\": true }</samp> when invoking Harmony Endpoint API operations</summary><div><h4>Issue:</h4><p>This error indicates that you have attempted to access a resource without a valid Bearer authoriztion token.</p><p>An example could be an attempt to invoke a Harmony Endpoint API operation without providing an <em>Infinity Portal</em> token in the request's <samp>Authorization</samp> header</p><p>Specific cases where this error is raised include:</p><ol><li>A request was made without providing an <em>Infinity Portal</em> bearer token in the <samp>Authorization</samp> header</li><li>A request was directed to to an <em>Infinity Portal</em> gateway other than the one that issued the bearer token</li><li>The provided token is intended for another <em>Infinity Portal</em> application</li><li>The provided token is expired</li><li>The provided token is malformed</li></ol><p></p><h4>Possible Solutions:</h4><p></p><ol><li>Verify the token was created to target the correct application (<em>Endpoint</em>)</li><li>Verify the token has not expired</li><li>Verify the token is being used correctly in the requst (<samp>Authorization: Bearer {{TOKEN}}</samp>)</li></ol><p></p></div></details></div></div></details><br><br></div>  # noqa: E501

    The version of the OpenAPI document: 1.9.221
    Contact: harmony-endpoint-external-api@checkpoint.com
    Generated by: https://openapi-generator.tech
"""

__version__ = "1.0.0"

# import ApiClient
from chkp_harmony_endpoint_management_sdk.generated.cloud.api_client import ApiClient

# import Configuration
from chkp_harmony_endpoint_management_sdk.generated.cloud.configuration import Configuration

# import exceptions
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import OpenApiException
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiAttributeError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiTypeError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiValueError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiKeyError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiException

from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiException

# Code generation part of HarmonyEndpoint

import json
from chkp_harmony_endpoint_management_sdk.core.logger import logger
from chkp_harmony_endpoint_management_sdk.classes.sdk_connection_state import SDKConnectionState
from chkp_harmony_endpoint_management_sdk.classes.harmony_endpoint_sdk_info import HarmonyEndpointSDKInfo
from chkp_harmony_endpoint_management_sdk.generated.cloud.sdk_build import sdk_build_info

from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_asset_management_computers_filtered.post import ComputersByFilter
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_create.post import CreateIoc
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_delete_all.delete import DeleteAllIoc
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_delete.delete import DeleteIocByIds
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_edit.put import EditIoc
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_get.post import GetIocPaged
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_jobs_job_id.get import GetJobById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_virtual_group_virtual_group_id_members_add.put import AddMembersToVirtualGroup
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_virtual_group_create.post import Create
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_virtual_group_virtual_group_id_members_remove.put import RemoveMembersFromVirtualGroup
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_tree_search.post import SearchInOrganization
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_assignments_add.put import AddRuleAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id.post import CloneRule
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_metadata.get import GetAllRulesMetadata
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_modifications.get import GetModificationsPendingInstallationByRuleId
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_assignments.get import GetRuleAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_metadata.get import GetRuleMetadataById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_install.post import InstallAllPolicies
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_install.post import InstallPoliciesForRule
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_assignments_remove.put import RemoveRuleAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.policy_threat_prevention_rule_id.get import GetThreatPreventionPolicy
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.policy_threat_prevention_rule_id.patch import SetThreatPreventionPolicy
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.policy_threat_prevention_rule_id_template.put import SetThreatPreventionPolicyTemplate
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_posture_vulnerability_devices.post import GetDeviceVulnerabilitiesDevice
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_posture_vulnerability_data.get import GetVulnerabilitiesData
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_posture_vulnerability_patch.post import VulnerabilityPatch
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_posture_vulnerability_patch_status.post import VulnerabilityPatchStatus
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_posture_vulnerability_scan.post import VulnerabilityScan
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_posture_vulnerability_scan_status.post import VulnerabilityScanStatus
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_quarantine_management_file_data.get import GetQuarantineFileData
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_quarantine_management_file_data.post import GetQuarantineFileDataByDevice
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_quarantine_management_file_fetch.post import QuarantineFileFetch
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_quarantine_management_file_restore.post import QuarantineFileRestore
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_registry_key_add.post import AgentAddRegistryKey
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_vpn_site_add.post import AgentAddVpnSite
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_process_information.post import AgentCollectProcessInformation
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_file_copy.post import AgentCopyFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_file_delete.post import AgentDeleteFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_file_move.post import AgentMoveFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_registry_key_delete.post import AgentRemoveRegistryKey
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_vpn_site_remove.post import AgentRemoveVpnSite
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_process_terminate.post import AgentTerminateProcess
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_collect_logs.post import CollectLogs
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_repair_computer.post import RepairComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_reset_computer.post import ResetComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_shutdown_computer.post import ShutdownComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_id_abort.post import AbortRemediationOperationById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_status.get import GetAllRemediationOperationStatuses
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_id_results_slim.post import GetRemediationOperationSlimResultsById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_id_status.get import GetRemediationOperationStatusById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_file_name.post import AnalyzeByFileName
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_ip.post import AnalyzeByIp
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_md5.post import AnalyzeByMd5
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_path.post import AnalyzeByPath
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_url.post import AnalyzeByUrl
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_anti_malware_restore.post import AntiMalwareRestore
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_anti_malware_scan.post import AntiMalwareScan
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_anti_malware_update.post import AntiMalwareUpdate
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_de_isolate.post import DeIsolateComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_isolate.post import IsolateComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_file_quarantine.post import QuarantineFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_file_restore.post import RestoreQuarantinedFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_session_keepalive.post import KeepAlive
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_session_login_cloud.post import LoginCloud

client = ApiClient()

class AssetManagementApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def computers_by_filter(self):
        return ComputersByFilter(self.__session_manager.client).computers_by_filter

class IndicatorsOfCompromiseApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def create_ioc(self):
        return CreateIoc(self.__session_manager.client).create_ioc

    @property
    def delete_all_ioc(self):
        return DeleteAllIoc(self.__session_manager.client).delete_all_ioc

    @property
    def delete_ioc_by_ids(self):
        return DeleteIocByIds(self.__session_manager.client).delete_ioc_by_ids

    @property
    def edit_ioc(self):
        return EditIoc(self.__session_manager.client).edit_ioc

    @property
    def get_ioc_paged(self):
        return GetIocPaged(self.__session_manager.client).get_ioc_paged

class JobsApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def get_job_by_id(self):
        return GetJobById(self.__session_manager.client).get_job_by_id

class OrganizationalStructureApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def add_members_to_virtual_group(self):
        return AddMembersToVirtualGroup(self.__session_manager.client).add_members_to_virtual_group

    @property
    def create(self):
        return Create(self.__session_manager.client).create

    @property
    def remove_members_from_virtual_group(self):
        return RemoveMembersFromVirtualGroup(self.__session_manager.client).remove_members_from_virtual_group

    @property
    def search_in_organization(self):
        return SearchInOrganization(self.__session_manager.client).search_in_organization

class PolicyGeneralApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def add_rule_assignments(self):
        return AddRuleAssignments(self.__session_manager.client).add_rule_assignments

    @property
    def clone_rule(self):
        return CloneRule(self.__session_manager.client).clone_rule

    @property
    def get_all_rules_metadata(self):
        return GetAllRulesMetadata(self.__session_manager.client).get_all_rules_metadata

    @property
    def get_modifications_pending_installation_by_rule_id(self):
        return GetModificationsPendingInstallationByRuleId(self.__session_manager.client).get_modifications_pending_installation_by_rule_id

    @property
    def get_rule_assignments(self):
        return GetRuleAssignments(self.__session_manager.client).get_rule_assignments

    @property
    def get_rule_metadata_by_id(self):
        return GetRuleMetadataById(self.__session_manager.client).get_rule_metadata_by_id

    @property
    def install_all_policies(self):
        return InstallAllPolicies(self.__session_manager.client).install_all_policies

    @property
    def install_policies_for_rule(self):
        return InstallPoliciesForRule(self.__session_manager.client).install_policies_for_rule

    @property
    def remove_rule_assignments(self):
        return RemoveRuleAssignments(self.__session_manager.client).remove_rule_assignments

class PolicyThreatPreventionApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def get_threat_prevention_policy(self):
        return GetThreatPreventionPolicy(self.__session_manager.client).get_threat_prevention_policy

    @property
    def set_threat_prevention_policy(self):
        return SetThreatPreventionPolicy(self.__session_manager.client).set_threat_prevention_policy

    @property
    def set_threat_prevention_policy_template(self):
        return SetThreatPreventionPolicyTemplate(self.__session_manager.client).set_threat_prevention_policy_template

class PostureManagementVulnerabilitiesApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def get_device_vulnerabilities_device(self):
        return GetDeviceVulnerabilitiesDevice(self.__session_manager.client).get_device_vulnerabilities_device

    @property
    def get_vulnerabilities_data(self):
        return GetVulnerabilitiesData(self.__session_manager.client).get_vulnerabilities_data

    @property
    def vulnerability_patch(self):
        return VulnerabilityPatch(self.__session_manager.client).vulnerability_patch

    @property
    def vulnerability_patch_status(self):
        return VulnerabilityPatchStatus(self.__session_manager.client).vulnerability_patch_status

    @property
    def vulnerability_scan(self):
        return VulnerabilityScan(self.__session_manager.client).vulnerability_scan

    @property
    def vulnerability_scan_status(self):
        return VulnerabilityScanStatus(self.__session_manager.client).vulnerability_scan_status

class QuarantineManagementApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def get_quarantine_file_data(self):
        return GetQuarantineFileData(self.__session_manager.client).get_quarantine_file_data

    @property
    def get_quarantine_file_data_by_device(self):
        return GetQuarantineFileDataByDevice(self.__session_manager.client).get_quarantine_file_data_by_device

    @property
    def quarantine_file_fetch(self):
        return QuarantineFileFetch(self.__session_manager.client).quarantine_file_fetch

    @property
    def quarantine_file_restore(self):
        return QuarantineFileRestore(self.__session_manager.client).quarantine_file_restore

class RemediationResponseAgentApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def agent_add_registry_key(self):
        return AgentAddRegistryKey(self.__session_manager.client).agent_add_registry_key

    @property
    def agent_add_vpn_site(self):
        return AgentAddVpnSite(self.__session_manager.client).agent_add_vpn_site

    @property
    def agent_collect_process_information(self):
        return AgentCollectProcessInformation(self.__session_manager.client).agent_collect_process_information

    @property
    def agent_copy_file(self):
        return AgentCopyFile(self.__session_manager.client).agent_copy_file

    @property
    def agent_delete_file(self):
        return AgentDeleteFile(self.__session_manager.client).agent_delete_file

    @property
    def agent_move_file(self):
        return AgentMoveFile(self.__session_manager.client).agent_move_file

    @property
    def agent_remove_registry_key(self):
        return AgentRemoveRegistryKey(self.__session_manager.client).agent_remove_registry_key

    @property
    def agent_remove_vpn_site(self):
        return AgentRemoveVpnSite(self.__session_manager.client).agent_remove_vpn_site

    @property
    def agent_terminate_process(self):
        return AgentTerminateProcess(self.__session_manager.client).agent_terminate_process

    @property
    def collect_logs(self):
        return CollectLogs(self.__session_manager.client).collect_logs

    @property
    def repair_computer(self):
        return RepairComputer(self.__session_manager.client).repair_computer

    @property
    def reset_computer(self):
        return ResetComputer(self.__session_manager.client).reset_computer

    @property
    def shutdown_computer(self):
        return ShutdownComputer(self.__session_manager.client).shutdown_computer

class RemediationResponseGeneralApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def abort_remediation_operation_by_id(self):
        return AbortRemediationOperationById(self.__session_manager.client).abort_remediation_operation_by_id

    @property
    def get_all_remediation_operation_statuses(self):
        return GetAllRemediationOperationStatuses(self.__session_manager.client).get_all_remediation_operation_statuses

    @property
    def get_remediation_operation_slim_results_by_id(self):
        return GetRemediationOperationSlimResultsById(self.__session_manager.client).get_remediation_operation_slim_results_by_id

    @property
    def get_remediation_operation_status_by_id(self):
        return GetRemediationOperationStatusById(self.__session_manager.client).get_remediation_operation_status_by_id

class RemediationResponseThreatPreventionApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def analyze_by_file_name(self):
        return AnalyzeByFileName(self.__session_manager.client).analyze_by_file_name

    @property
    def analyze_by_ip(self):
        return AnalyzeByIp(self.__session_manager.client).analyze_by_ip

    @property
    def analyze_by_md5(self):
        return AnalyzeByMd5(self.__session_manager.client).analyze_by_md5

    @property
    def analyze_by_path(self):
        return AnalyzeByPath(self.__session_manager.client).analyze_by_path

    @property
    def analyze_by_url(self):
        return AnalyzeByUrl(self.__session_manager.client).analyze_by_url

    @property
    def anti_malware_restore(self):
        return AntiMalwareRestore(self.__session_manager.client).anti_malware_restore

    @property
    def anti_malware_scan(self):
        return AntiMalwareScan(self.__session_manager.client).anti_malware_scan

    @property
    def anti_malware_update(self):
        return AntiMalwareUpdate(self.__session_manager.client).anti_malware_update

    @property
    def de_isolate_computer(self):
        return DeIsolateComputer(self.__session_manager.client).de_isolate_computer

    @property
    def isolate_computer(self):
        return IsolateComputer(self.__session_manager.client).isolate_computer

    @property
    def quarantine_file(self):
        return QuarantineFile(self.__session_manager.client).quarantine_file

    @property
    def restore_quarantined_file(self):
        return RestoreQuarantinedFile(self.__session_manager.client).restore_quarantined_file

class SessionApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def keep_alive(self):
        return KeepAlive(self.__session_manager.client).keep_alive

    @property
    def login_cloud(self):
        return LoginCloud(self.__session_manager.client).login_cloud


operations = [
    {
        'class_name': 'asset_management_api',
        'class_description' : 'Gain insight and control over the organization&#x27;s assets',
        'methods': [
            {
                'method_name': 'computers_by_filter',
                'method_description': 'Gets a list of computers matching the given filters  &lt;p&gt; This API Endpoint provides a low-level view into the information provided by the Harmony Endpoint agent. Available information includes all information available within the Infinity Portal&#x27;s Harmony Endpoint Asset Management Tab. Please note that security events are not covered by this API with the exception of Anti-Malware detections &lt;/p&gt;  &lt;p&gt;While working with the API you may get a unique field &lt;em&gt;value&lt;/em&gt; - &lt;b&gt;999&lt;/b&gt;.&lt;/br&gt; This value is a placeholder for &#x27;null&#x27;.&lt;/br&gt;For example, when &#x27;&lt;em&gt;computerAmVersion&lt;/em&gt;&#x27; is &#x27;999&#x27;, it means there are no infections for a given computer. In the context of &#x27;deploymentStatus&#x27; though, for example, the same &#x27;999&#x27; (e.g. &#x27;null&#x27;) means &#x27;deploymentStatus&#x27; in unknown. &lt;/p&gt;',
            },]
    },
    {
        'class_name': 'indicators_of_compromise_api',
        'class_description' : 'Rapidly and globally adapt to engage potential or active threats',
        'methods': [
            {
                'method_name': 'create_ioc',
                'method_description': '&lt;p&gt;Creates new Indicators of Compromise using the given parameters&lt;/p&gt;  &lt;br&gt;  &lt;p&gt;     Each IOC may have one of several types who&#x27;s     formats are provided in ECMAScript-flavored Regular Expression syntax. &lt;/p&gt;  &lt;ul&gt;     &lt;li&gt;         &lt;p&gt;&lt;code&gt;Domain&lt;/code&gt; - A domain-only string. For example, &lt;em&gt;xyz.com&lt;/em&gt;&lt;/p&gt;         &lt;p&gt;A protocol (e.g &lt;em&gt;https://&lt;/em&gt; or specific URLs (e.g. &lt;em&gt;xyz.com/file.php&lt;/em&gt;) are invalid in this context&lt;/p&gt;         &lt;p&gt;Format: &lt;code&gt;/^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]/i&lt;/code&gt;&lt;/p&gt;         &lt;br&gt;     &lt;/li&gt;     &lt;li&gt;         &lt;p&gt;&lt;code&gt;IP&lt;/code&gt; - An IPv4 address (e.g. &lt;em&gt;1.1.1.1&lt;/em&gt;)&lt;/p&gt;         &lt;p&gt;Format: &lt;code&gt;/(((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3})(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/&lt;/code&gt;&lt;/p&gt;         &lt;br&gt;     &lt;/li&gt;     &lt;li&gt;         &lt;p&gt;&lt;code&gt;URL&lt;/code&gt; - A URL (e.g. &lt;em&gt;https://www.checkpoint.com/harmony/advanced-endpoint-protection&lt;/em&gt;)&lt;/p&gt;         &lt;p&gt;Format: &lt;code&gt;/^(((http(s?|\\??)://([\\p{L}\\p{N}()\\*\\?].)*)|([\\p{L}\\p{N}()\\*\\?].)*)[-\\p{L}\\p{N}@:%_\\?\\*\\+~#&#x3D;]{0,256}\\.[\\p{L}\\p{N}()\\*\\?]+([-\\p{L}\\p{N}()@:%_\\?\\*\\+.~#?&amp;//&#x3D;]*))$/u&lt;/code&gt;&lt;/p&gt;         &lt;br&gt;     &lt;/li&gt;     &lt;li&gt;         &lt;p&gt;&lt;code&gt;MD5&lt;/code&gt; - An MD5 string&lt;/p&gt;         &lt;p&gt;Format: &lt;code&gt;/^(?:([A-F0-9]{8}-){3}[A-F0-9]{8})$|^([a-f0-9]{32})$/i&lt;/code&gt;&lt;/p&gt;         &lt;br&gt;     &lt;/li&gt;     &lt;li&gt;         &lt;p&gt;&lt;code&gt;SHA1&lt;/code&gt; - A SHA1 string&lt;/p&gt;         &lt;p&gt;Format: &lt;code&gt;/^(?:([A-F0-9]{8}-){4}[A-F0-9]{8})$|^([a-fA-F0-9]{40})$/i&lt;/code&gt;&lt;/p&gt;         &lt;br&gt;     &lt;/li&gt; &lt;/ul',
            },
            {
                'method_name': 'delete_all_ioc',
                'method_description': 'Deletes all existing Indicators of Compromise. &lt;p&gt;This action &lt;b&gt;permanently deletes&lt;/b&gt; &lt;b&gt;all&lt;/b&gt; Indicators of Compromise and &lt;b&gt;cannot be undone&lt;/b&gt;&lt;/p',
            },
            {
                'method_name': 'delete_ioc_by_ids',
                'method_description': 'Deletes the given Indicators of Compromise by their ID',
            },
            {
                'method_name': 'edit_ioc',
                'method_description': 'Updates the given Indicators of Compromise with the given parameters',
            },
            {
                'method_name': 'get_ioc_paged',
                'method_description': 'Gets a list of Indicators of Compromise matching the given parameters',
            },]
    },
    {
        'class_name': 'jobs_api',
        'class_description' : 'Query for the state of active managerial operations',
        'methods': [
            {
                'method_name': 'get_job_by_id',
                'method_description': 'Retrieves the status and result (if any) of a given asynchronous operation. &lt;p&gt;A Job is a way to monitor the progress of an asynchronous operation whilst avoiding issues that may manifest during long synchronous waits.&lt;/p&gt;  &lt;p&gt;For example, a search for a particular computer in the organization may take a considerable amount of time in large organizations so the &#x27;/computers/by-filter&#x27; API has been made to return a Job. &lt;/br&gt;This means that, when invoked, the operation returns an object with a &#x27;jobId&#x27; field. That Job can then be queried and, when completed, will contain the result of the &#x27;/computers/by-filter&#x27; operation.&lt;/p&gt; &lt;p&gt;&lt;h3&gt;It is important to note that once a job concludes (i.e. is &#x27;DONE&#x27; or &#x27;FAILED&#x27;) it has fulfilled its purpose and is no longer useful&lt;/h3&gt;&lt;/p&gt; &lt;p&gt;As such, Jobs should be treated as &#x27;single-use&#x27;. Once concluded, they should be &#x27;discarded&#x27;&lt;/p&gt;',
            },]
    },
    {
        'class_name': 'organizational_structure_api',
        'class_description' : 'Gain insight and control over the organization&#x27;s structure and assignments',
        'methods': [
            {
                'method_name': 'add_members_to_virtual_group',
                'method_description': 'Adds the specified entities to the given Virtual Group &lt;p&gt;Entities that are already assigned to the Virtual Group are ignored&lt;/p&gt;',
            },
            {
                'method_name': 'create',
                'method_description': 'Creates a new Virtual Group',
            },
            {
                'method_name': 'remove_members_from_virtual_group',
                'method_description': 'Removes the specified entities from the given Virtual Group. &lt;p&gt;Entities that are not assigned to the Virtual Group are ignored&lt;/p&gt;',
            },
            {
                'method_name': 'search_in_organization',
                'method_description': 'Searches the organization for entities matching the given query',
            },]
    },
    {
        'class_name': 'policy_general_api',
        'class_description' : 'Manage general aspects of the Harmony Endpoint organizational policies',
        'methods': [
            {
                'method_name': 'add_rule_assignments',
                'method_description': 'Assigns the specified entities to the given rule. &lt;p&gt;Specified IDs that are already assigned to the rule are ignored&lt;/p&gt;',
            },
            {
                'method_name': 'clone_rule',
                'method_description': ' Clones the specified rule and puts the clone in the provided position inside the rulebase',
            },
            {
                'method_name': 'get_all_rules_metadata',
                'method_description': 'Gets the metadata of all runes. &lt;p&gt;Metadata refers to all information relating to the rule except it&#x27;s actual settings&lt;/p&gt;',
            },
            {
                'method_name': 'get_modifications_pending_installation_by_rule_id',
                'method_description': ' Gets information on modifications to a given rule since it was last installed',
            },
            {
                'method_name': 'get_rule_assignments',
                'method_description': 'Gets all entities directly assigned to the given rule',
            },
            {
                'method_name': 'get_rule_metadata_by_id',
                'method_description': 'Gets the given rule&#x27;s metadata. &lt;p&gt;Metadata refers to all information relating to the rule except it&#x27;s actual settings&lt;/p&gt;',
            },
            {
                'method_name': 'install_all_policies',
                'method_description': 'Installs all policies. &lt;p&gt;Changes to rule settings are only enforced after policy installation&lt;/p&gt;',
            },
            {
                'method_name': 'install_policies_for_rule',
                'method_description': 'Installs all policies of a given rule. &lt;p&gt;Changes to rule settings are only enforced after policy installation&lt;/p&gt;',
            },
            {
                'method_name': 'remove_rule_assignments',
                'method_description': 'Removes the specified entities from the given rule&#x27;s assignments. &lt;p&gt;Specified IDs that are not assigned to the rule are ignored&lt;/p&gt;',
            },]
    },
    {
        'class_name': 'policy_threat_prevention_api',
        'class_description' : 'Manage Threat Prevention rules and policies',
        'methods': [
            {
                'method_name': 'get_threat_prevention_policy',
                'method_description': ' Gets the Threat-Prevention policy of the given rule',
            },
            {
                'method_name': 'set_threat_prevention_policy',
                'method_description': 'Updates the given Threat-Prevention rule',
            },
            {
                'method_name': 'set_threat_prevention_policy_template',
                'method_description': 'Sets the Threat-Prevention policy template for the given rule.  &lt;p&gt; Setting a template instructs the policy to adhere to the Check Point&#x27;s recommended configuration &lt;/p&gt;',
            },]
    },
    {
        'class_name': 'posture_management_vulnerabilities_api',
        'class_description' : 'Monitor vulnerabilities, scan devices and patch applications',
        'methods': [
            {
                'method_name': 'get_device_vulnerabilities_device',
                'method_description': 'Gets vulnerabilities affecting the given devices',
            },
            {
                'method_name': 'get_vulnerabilities_data',
                'method_description': 'Gets all vulnerability related information',
            },
            {
                'method_name': 'vulnerability_patch',
                'method_description': 'Initiates an application/s patch operation on devices matching the given query',
            },
            {
                'method_name': 'vulnerability_patch_status',
                'method_description': 'Gets the application patch operation statuses for devices and/or CVEs matching the given query',
            },
            {
                'method_name': 'vulnerability_scan',
                'method_description': 'Initiates a vulnerability scan on devices matching the given query',
            },
            {
                'method_name': 'vulnerability_scan_status',
                'method_description': 'Gets the current statuses of the vulnerability scans running on devices matching the given query',
            },]
    },
    {
        'class_name': 'quarantine_management_api',
        'class_description' : 'Monitor, restore and fetch quarantine files',
        'methods': [
            {
                'method_name': 'get_quarantine_file_data',
                'method_description': '',
            },
            {
                'method_name': 'get_quarantine_file_data_by_device',
                'method_description': '',
            },
            {
                'method_name': 'quarantine_file_fetch',
                'method_description': '',
            },
            {
                'method_name': 'quarantine_file_restore',
                'method_description': '',
            },]
    },
    {
        'class_name': 'remediation_response_agent_api',
        'class_description' : 'Remotely perform managerial operations on Harmony Endpoint Clients',
        'methods': [
            {
                'method_name': 'agent_add_registry_key',
                'method_description': 'Adds a given registry key and/or value to the registry of computers matching the given query',
            },
            {
                'method_name': 'agent_add_vpn_site',
                'method_description': 'Adds the given VPN Site&#x27;s configuration to computers matching the given query &lt;p&gt;Adding a VPN Site allows Harmony Endpoint Clients to connect to it&lt;/p&gt;',
            },
            {
                'method_name': 'agent_collect_process_information',
                'method_description': 'Collects information about processes on computers matching the given query',
            },
            {
                'method_name': 'agent_copy_file',
                'method_description': 'Copies the given file from the given source to the given destination on computers matching the given query',
            },
            {
                'method_name': 'agent_delete_file',
                'method_description': 'Deletes the given file from the given source on computers matching the given query',
            },
            {
                'method_name': 'agent_move_file',
                'method_description': 'Moves the given file from the given source to the given destination on computers matching the given query',
            },
            {
                'method_name': 'agent_remove_registry_key',
                'method_description': 'Removes the given registry key or value to the registry of computers matching the given query',
            },
            {
                'method_name': 'agent_remove_vpn_site',
                'method_description': 'Removes the given VPN Site&#x27;s configuration to computers matching the given query',
            },
            {
                'method_name': 'agent_terminate_process',
                'method_description': 'Terminates the given process on computers matching the given query',
            },
            {
                'method_name': 'collect_logs',
                'method_description': 'Collects all Harmony Endpoint Client logs as well as diagnostic information from computers matching the given query',
            },
            {
                'method_name': 'repair_computer',
                'method_description': 'Repairs the Harmony Endpoint Client installation on computers matching the given query',
            },
            {
                'method_name': 'reset_computer',
                'method_description': 'Restarts computers matching the given query',
            },
            {
                'method_name': 'shutdown_computer',
                'method_description': 'Shuts-down computers matching the given query',
            },]
    },
    {
        'class_name': 'remediation_response_general_api',
        'class_description' : 'Gain insight and control over active Remediation Operations',
        'methods': [
            {
                'method_name': 'abort_remediation_operation_by_id',
                'method_description': 'Aborts the given Remediation Operation. &lt;p&gt;Aborting an operation prevents it from being sent to further Harmony Endpoint Clients.&lt;/p&gt; &lt;p&gt;Clients that have already received the operation are not affected&lt;/p&gt;',
            },
            {
                'method_name': 'get_all_remediation_operation_statuses',
                'method_description': 'Gets the current statuses of all Remediation Operations',
            },
            {
                'method_name': 'get_remediation_operation_slim_results_by_id',
                'method_description': 'Gets the results of a given Remediation Operation.  &lt;p&gt;Remediation Operations may produce results such a Forensics Report or yield status updates such as an Anti-Malware scan progress.&lt;/p&gt; &lt;p&gt;Note: this operation is a &#x27;&lt;em&gt;slim&lt;/em&gt;&#x27; version, returning only essential information&lt;/p&gt;',
            },
            {
                'method_name': 'get_remediation_operation_status_by_id',
                'method_description': 'Gets the current status of the given Remediation Operation &lt;p&gt;&lt;b&gt;Note:&lt;/b&gt; By default, the operation returns a &lt;i&gt;Job&lt;/i&gt; that needs to be queried by the &lt;em&gt;GET /job/{id}&lt;/em&gt; API&lt;/p&gt; &lt;p&gt;When completed, the job will contain the operation&#x27;s current status.&lt;/br&gt;The &lt;i&gt;job&lt;/i&gt; itself &lt;b&gt;should not be re-used&lt;/b&gt;. Doing so will yield the same result&lt;/p&gt;',
            },]
    },
    {
        'class_name': 'remediation_response_threat_prevention_api',
        'class_description' : 'Remotely perform security-oriented operations on Harmony Endpoint Clients',
        'methods': [
            {
                'method_name': 'analyze_by_file_name',
                'method_description': 'Collects forensics data whenever a computer that matches the given query accesses or executes the given file',
            },
            {
                'method_name': 'analyze_by_ip',
                'method_description': 'Collects forensics data whenever a computer that matches the given query accesses or executes a resource matching the given MD5',
            },
            {
                'method_name': 'analyze_by_md5',
                'method_description': 'Collects forensics data whenever a computer that matches the given query accesses or executes a resource matching the given MD5',
            },
            {
                'method_name': 'analyze_by_path',
                'method_description': ' Collects forensics data whenever a computer that matches the given query accesses or executes a resource residing in the given path',
            },
            {
                'method_name': 'analyze_by_url',
                'method_description': 'Collects forensics data whenever a computer that matches the given query accesses the given URL',
            },
            {
                'method_name': 'anti_malware_restore',
                'method_description': 'Restores a file that was previously quarantined by the Harmony Endpoint Client&#x27;s Anti-Malware capability',
            },
            {
                'method_name': 'anti_malware_scan',
                'method_description': 'Performs an Anti-Malware scan on computers matching the given query',
            },
            {
                'method_name': 'anti_malware_update',
                'method_description': 'Updates the Anti-Malware Signature Database on computers matching the given query',
            },
            {
                'method_name': 'de_isolate_computer',
                'method_description': 'De-Isolates the computers matching the given query. &lt;p&gt;De-isolating a computer restores its access to network resources. Affects only isolated computers&lt;/p&gt;',
            },
            {
                'method_name': 'isolate_computer',
                'method_description': 'Isolates the computers matching the given query. &lt;p&gt;Isolation is the act of denying all network access from a given computer&lt;/p&gt;',
            },
            {
                'method_name': 'quarantine_file',
                'method_description': 'Quarantines files given by path or MD5 or detections relating to a forensic incident',
            },
            {
                'method_name': 'restore_quarantined_file',
                'method_description': 'Restores previously quarantined files given by path or MD5 or detections relating to a forensic incident',
            },]
    },
    {
        'class_name': 'session_api',
        'class_description' : 'Authenticate for and maintain Harmony Endpoint API sessions',
        'methods': [
            {
                'method_name': 'keep_alive',
                'method_description': 'Resets the expiration time for the session back to its default value &lt;p&gt;Keep-alive calls are used to extend the useful lifespan of a session without performing any meaningful operations&lt;/p&gt;',
            },
            {
                'method_name': 'login_cloud',
                'method_description': 'Creates a new API work-session. &lt;p&gt;By default, API sessions last 6 minutes before expiring. Performing any authenticated operation will reset the expiry&lt;/p&gt; &lt;/br&gt; &lt;p&gt;&lt;em&gt;&lt;b&gt;Note:&lt;/b&gt;&lt;/em&gt; The session created by this API Endpoint is unrelated to the Infinity Portal session conveyed via the &#x27;cloudinfraJwt&#x27; bearer token&lt;/p&gt; &lt;p&gt;To manually reset the expiry without performing any meaningful operations see the &#x27;keepalive&#x27; operation&lt;/p&gt;',
            },]
    },
]

class HarmonyEndpointBase:
    
    @staticmethod
    def info() -> HarmonyEndpointSDKInfo:
        return sdk_build_info()

    def __init__(self, instance_schema: str, session_manager):
        logger(f'A new instance "{instance_schema}" of sdk created, full version info: {HarmonyEndpointBase.info()}')
        self._session_manager = session_manager


    def disconnect(self):
        self._session_manager.disconnect()

    def reconnect(self):
        self._session_manager.reconnect()

    def connection_state(self) -> SDKConnectionState:
        self._session_manager.connection_state()


    @property
    def asset_management_api(self):
        return AssetManagementApi(self._session_manager)

    @property
    def indicators_of_compromise_api(self):
        return IndicatorsOfCompromiseApi(self._session_manager)

    @property
    def jobs_api(self):
        return JobsApi(self._session_manager)

    @property
    def organizational_structure_api(self):
        return OrganizationalStructureApi(self._session_manager)

    @property
    def policy_general_api(self):
        return PolicyGeneralApi(self._session_manager)

    @property
    def policy_threat_prevention_api(self):
        return PolicyThreatPreventionApi(self._session_manager)

    @property
    def posture_management_vulnerabilities_api(self):
        return PostureManagementVulnerabilitiesApi(self._session_manager)

    @property
    def quarantine_management_api(self):
        return QuarantineManagementApi(self._session_manager)

    @property
    def remediation_response_agent_api(self):
        return RemediationResponseAgentApi(self._session_manager)

    @property
    def remediation_response_general_api(self):
        return RemediationResponseGeneralApi(self._session_manager)

    @property
    def remediation_response_threat_prevention_api(self):
        return RemediationResponseThreatPreventionApi(self._session_manager)

    @property
    def _session_api(self):
        return SessionApi(self._session_manager)

