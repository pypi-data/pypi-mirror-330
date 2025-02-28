import typing_extensions

from chkp_harmony_endpoint_management_sdk.generated.cloud.paths import PathValues
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_asset_management_computers_filtered import V1AssetManagementComputersFiltered
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_ioc_get import V1IocGet
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_ioc_edit import V1IocEdit
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_ioc_create import V1IocCreate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_ioc_delete_all import V1IocDeleteAll
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_ioc_delete import V1IocDelete
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_jobs_job_id import V1JobsJobId
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_organization_tree_search import V1OrganizationTreeSearch
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_organization_virtual_group_create import V1OrganizationVirtualGroupCreate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_organization_virtual_group_virtual_group_id_members_add import V1OrganizationVirtualGroupVirtualGroupIdMembersAdd
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_organization_virtual_group_virtual_group_id_members_remove import V1OrganizationVirtualGroupVirtualGroupIdMembersRemove
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id_assignments import V1PolicyRuleIdAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id_assignments_add import V1PolicyRuleIdAssignmentsAdd
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id_assignments_remove import V1PolicyRuleIdAssignmentsRemove
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_install import V1PolicyInstall
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id_install import V1PolicyRuleIdInstall
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id_modifications import V1PolicyRuleIdModifications
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id import V1PolicyRuleId
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_rule_id_metadata import V1PolicyRuleIdMetadata
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_policy_metadata import V1PolicyMetadata
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.policy_threat_prevention_rule_id import PolicyThreatPreventionRuleId
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.policy_threat_prevention_rule_id_template import PolicyThreatPreventionRuleIdTemplate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_posture_vulnerability_data import V1PostureVulnerabilityData
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_posture_vulnerability_devices import V1PostureVulnerabilityDevices
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_posture_vulnerability_scan import V1PostureVulnerabilityScan
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_posture_vulnerability_scan_status import V1PostureVulnerabilityScanStatus
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_posture_vulnerability_patch import V1PostureVulnerabilityPatch
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_posture_vulnerability_patch_status import V1PostureVulnerabilityPatchStatus
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_reset_computer import V1RemediationAgentResetComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_shutdown_computer import V1RemediationAgentShutdownComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_repair_computer import V1RemediationAgentRepairComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_collect_logs import V1RemediationAgentCollectLogs
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_registry_key_add import V1RemediationAgentRegistryKeyAdd
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_registry_key_delete import V1RemediationAgentRegistryKeyDelete
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_file_copy import V1RemediationAgentFileCopy
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_file_move import V1RemediationAgentFileMove
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_file_delete import V1RemediationAgentFileDelete
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_process_information import V1RemediationAgentProcessInformation
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_process_terminate import V1RemediationAgentProcessTerminate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_vpn_site_add import V1RemediationAgentVpnSiteAdd
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_agent_vpn_site_remove import V1RemediationAgentVpnSiteRemove
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_anti_malware_scan import V1RemediationAntiMalwareScan
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_anti_malware_update import V1RemediationAntiMalwareUpdate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_anti_malware_restore import V1RemediationAntiMalwareRestore
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_analyze_by_indicator_url import V1RemediationForensicsAnalyzeByIndicatorUrl
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_analyze_by_indicator_ip import V1RemediationForensicsAnalyzeByIndicatorIp
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_analyze_by_indicator_path import V1RemediationForensicsAnalyzeByIndicatorPath
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_analyze_by_indicator_file_name import V1RemediationForensicsAnalyzeByIndicatorFileName
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_analyze_by_indicator_md5 import V1RemediationForensicsAnalyzeByIndicatorMd5
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_file_quarantine import V1RemediationForensicsFileQuarantine
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_forensics_file_restore import V1RemediationForensicsFileRestore
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_isolate import V1RemediationIsolate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_de_isolate import V1RemediationDeIsolate
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_status import V1RemediationStatus
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_id_status import V1RemediationIdStatus
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_id_abort import V1RemediationIdAbort
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_remediation_id_results_slim import V1RemediationIdResultsSlim
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_quarantine_management_file_data import V1QuarantineManagementFileData
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_quarantine_management_file_restore import V1QuarantineManagementFileRestore
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_quarantine_management_file_fetch import V1QuarantineManagementFileFetch
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_session_keepalive import V1SessionKeepalive
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.paths.v1_session_login_cloud import V1SessionLoginCloud

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_ASSETMANAGEMENT_COMPUTERS_FILTERED: V1AssetManagementComputersFiltered,
        PathValues.V1_IOC_GET: V1IocGet,
        PathValues.V1_IOC_EDIT: V1IocEdit,
        PathValues.V1_IOC_CREATE: V1IocCreate,
        PathValues.V1_IOC_DELETE_ALL: V1IocDeleteAll,
        PathValues.V1_IOC_DELETE: V1IocDelete,
        PathValues.V1_JOBS_JOB_ID: V1JobsJobId,
        PathValues.V1_ORGANIZATION_TREE_SEARCH: V1OrganizationTreeSearch,
        PathValues.V1_ORGANIZATION_VIRTUALGROUP_CREATE: V1OrganizationVirtualGroupCreate,
        PathValues.V1_ORGANIZATION_VIRTUALGROUP_VIRTUAL_GROUP_ID_MEMBERS_ADD: V1OrganizationVirtualGroupVirtualGroupIdMembersAdd,
        PathValues.V1_ORGANIZATION_VIRTUALGROUP_VIRTUAL_GROUP_ID_MEMBERS_REMOVE: V1OrganizationVirtualGroupVirtualGroupIdMembersRemove,
        PathValues.V1_POLICY_RULE_ID_ASSIGNMENTS: V1PolicyRuleIdAssignments,
        PathValues.V1_POLICY_RULE_ID_ASSIGNMENTS_ADD: V1PolicyRuleIdAssignmentsAdd,
        PathValues.V1_POLICY_RULE_ID_ASSIGNMENTS_REMOVE: V1PolicyRuleIdAssignmentsRemove,
        PathValues.V1_POLICY_INSTALL: V1PolicyInstall,
        PathValues.V1_POLICY_RULE_ID_INSTALL: V1PolicyRuleIdInstall,
        PathValues.V1_POLICY_RULE_ID_MODIFICATIONS: V1PolicyRuleIdModifications,
        PathValues.V1_POLICY_RULE_ID: V1PolicyRuleId,
        PathValues.V1_POLICY_RULE_ID_METADATA: V1PolicyRuleIdMetadata,
        PathValues.V1_POLICY_METADATA: V1PolicyMetadata,
        PathValues.POLICY_THREATPREVENTION_RULE_ID: PolicyThreatPreventionRuleId,
        PathValues.POLICY_THREATPREVENTION_RULE_ID_TEMPLATE: PolicyThreatPreventionRuleIdTemplate,
        PathValues.V1_POSTURE_VULNERABILITY_DATA: V1PostureVulnerabilityData,
        PathValues.V1_POSTURE_VULNERABILITY_DEVICES: V1PostureVulnerabilityDevices,
        PathValues.V1_POSTURE_VULNERABILITY_SCAN: V1PostureVulnerabilityScan,
        PathValues.V1_POSTURE_VULNERABILITY_SCAN_STATUS: V1PostureVulnerabilityScanStatus,
        PathValues.V1_POSTURE_VULNERABILITY_PATCH: V1PostureVulnerabilityPatch,
        PathValues.V1_POSTURE_VULNERABILITY_PATCH_STATUS: V1PostureVulnerabilityPatchStatus,
        PathValues.V1_REMEDIATION_AGENT_RESETCOMPUTER: V1RemediationAgentResetComputer,
        PathValues.V1_REMEDIATION_AGENT_SHUTDOWNCOMPUTER: V1RemediationAgentShutdownComputer,
        PathValues.V1_REMEDIATION_AGENT_REPAIRCOMPUTER: V1RemediationAgentRepairComputer,
        PathValues.V1_REMEDIATION_AGENT_COLLECTLOGS: V1RemediationAgentCollectLogs,
        PathValues.V1_REMEDIATION_AGENT_REGISTRY_KEY_ADD: V1RemediationAgentRegistryKeyAdd,
        PathValues.V1_REMEDIATION_AGENT_REGISTRY_KEY_DELETE: V1RemediationAgentRegistryKeyDelete,
        PathValues.V1_REMEDIATION_AGENT_FILE_COPY: V1RemediationAgentFileCopy,
        PathValues.V1_REMEDIATION_AGENT_FILE_MOVE: V1RemediationAgentFileMove,
        PathValues.V1_REMEDIATION_AGENT_FILE_DELETE: V1RemediationAgentFileDelete,
        PathValues.V1_REMEDIATION_AGENT_PROCESS_INFORMATION: V1RemediationAgentProcessInformation,
        PathValues.V1_REMEDIATION_AGENT_PROCESS_TERMINATE: V1RemediationAgentProcessTerminate,
        PathValues.V1_REMEDIATION_AGENT_VPN_SITE_ADD: V1RemediationAgentVpnSiteAdd,
        PathValues.V1_REMEDIATION_AGENT_VPN_SITE_REMOVE: V1RemediationAgentVpnSiteRemove,
        PathValues.V1_REMEDIATION_ANTIMALWARE_SCAN: V1RemediationAntiMalwareScan,
        PathValues.V1_REMEDIATION_ANTIMALWARE_UPDATE: V1RemediationAntiMalwareUpdate,
        PathValues.V1_REMEDIATION_ANTIMALWARE_RESTORE: V1RemediationAntiMalwareRestore,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_URL: V1RemediationForensicsAnalyzeByIndicatorUrl,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_IP: V1RemediationForensicsAnalyzeByIndicatorIp,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_PATH: V1RemediationForensicsAnalyzeByIndicatorPath,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_FILENAME: V1RemediationForensicsAnalyzeByIndicatorFileName,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_MD5: V1RemediationForensicsAnalyzeByIndicatorMd5,
        PathValues.V1_REMEDIATION_FORENSICS_FILE_QUARANTINE: V1RemediationForensicsFileQuarantine,
        PathValues.V1_REMEDIATION_FORENSICS_FILE_RESTORE: V1RemediationForensicsFileRestore,
        PathValues.V1_REMEDIATION_ISOLATE: V1RemediationIsolate,
        PathValues.V1_REMEDIATION_DEISOLATE: V1RemediationDeIsolate,
        PathValues.V1_REMEDIATION_STATUS: V1RemediationStatus,
        PathValues.V1_REMEDIATION_ID_STATUS: V1RemediationIdStatus,
        PathValues.V1_REMEDIATION_ID_ABORT: V1RemediationIdAbort,
        PathValues.V1_REMEDIATION_ID_RESULTS_SLIM: V1RemediationIdResultsSlim,
        PathValues.V1_QUARANTINEMANAGEMENT_FILE_DATA: V1QuarantineManagementFileData,
        PathValues.V1_QUARANTINEMANAGEMENT_FILE_RESTORE: V1QuarantineManagementFileRestore,
        PathValues.V1_QUARANTINEMANAGEMENT_FILE_FETCH: V1QuarantineManagementFileFetch,
        PathValues.V1_SESSION_KEEPALIVE: V1SessionKeepalive,
        PathValues.V1_SESSION_LOGIN_CLOUD: V1SessionLoginCloud,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_ASSETMANAGEMENT_COMPUTERS_FILTERED: V1AssetManagementComputersFiltered,
        PathValues.V1_IOC_GET: V1IocGet,
        PathValues.V1_IOC_EDIT: V1IocEdit,
        PathValues.V1_IOC_CREATE: V1IocCreate,
        PathValues.V1_IOC_DELETE_ALL: V1IocDeleteAll,
        PathValues.V1_IOC_DELETE: V1IocDelete,
        PathValues.V1_JOBS_JOB_ID: V1JobsJobId,
        PathValues.V1_ORGANIZATION_TREE_SEARCH: V1OrganizationTreeSearch,
        PathValues.V1_ORGANIZATION_VIRTUALGROUP_CREATE: V1OrganizationVirtualGroupCreate,
        PathValues.V1_ORGANIZATION_VIRTUALGROUP_VIRTUAL_GROUP_ID_MEMBERS_ADD: V1OrganizationVirtualGroupVirtualGroupIdMembersAdd,
        PathValues.V1_ORGANIZATION_VIRTUALGROUP_VIRTUAL_GROUP_ID_MEMBERS_REMOVE: V1OrganizationVirtualGroupVirtualGroupIdMembersRemove,
        PathValues.V1_POLICY_RULE_ID_ASSIGNMENTS: V1PolicyRuleIdAssignments,
        PathValues.V1_POLICY_RULE_ID_ASSIGNMENTS_ADD: V1PolicyRuleIdAssignmentsAdd,
        PathValues.V1_POLICY_RULE_ID_ASSIGNMENTS_REMOVE: V1PolicyRuleIdAssignmentsRemove,
        PathValues.V1_POLICY_INSTALL: V1PolicyInstall,
        PathValues.V1_POLICY_RULE_ID_INSTALL: V1PolicyRuleIdInstall,
        PathValues.V1_POLICY_RULE_ID_MODIFICATIONS: V1PolicyRuleIdModifications,
        PathValues.V1_POLICY_RULE_ID: V1PolicyRuleId,
        PathValues.V1_POLICY_RULE_ID_METADATA: V1PolicyRuleIdMetadata,
        PathValues.V1_POLICY_METADATA: V1PolicyMetadata,
        PathValues.POLICY_THREATPREVENTION_RULE_ID: PolicyThreatPreventionRuleId,
        PathValues.POLICY_THREATPREVENTION_RULE_ID_TEMPLATE: PolicyThreatPreventionRuleIdTemplate,
        PathValues.V1_POSTURE_VULNERABILITY_DATA: V1PostureVulnerabilityData,
        PathValues.V1_POSTURE_VULNERABILITY_DEVICES: V1PostureVulnerabilityDevices,
        PathValues.V1_POSTURE_VULNERABILITY_SCAN: V1PostureVulnerabilityScan,
        PathValues.V1_POSTURE_VULNERABILITY_SCAN_STATUS: V1PostureVulnerabilityScanStatus,
        PathValues.V1_POSTURE_VULNERABILITY_PATCH: V1PostureVulnerabilityPatch,
        PathValues.V1_POSTURE_VULNERABILITY_PATCH_STATUS: V1PostureVulnerabilityPatchStatus,
        PathValues.V1_REMEDIATION_AGENT_RESETCOMPUTER: V1RemediationAgentResetComputer,
        PathValues.V1_REMEDIATION_AGENT_SHUTDOWNCOMPUTER: V1RemediationAgentShutdownComputer,
        PathValues.V1_REMEDIATION_AGENT_REPAIRCOMPUTER: V1RemediationAgentRepairComputer,
        PathValues.V1_REMEDIATION_AGENT_COLLECTLOGS: V1RemediationAgentCollectLogs,
        PathValues.V1_REMEDIATION_AGENT_REGISTRY_KEY_ADD: V1RemediationAgentRegistryKeyAdd,
        PathValues.V1_REMEDIATION_AGENT_REGISTRY_KEY_DELETE: V1RemediationAgentRegistryKeyDelete,
        PathValues.V1_REMEDIATION_AGENT_FILE_COPY: V1RemediationAgentFileCopy,
        PathValues.V1_REMEDIATION_AGENT_FILE_MOVE: V1RemediationAgentFileMove,
        PathValues.V1_REMEDIATION_AGENT_FILE_DELETE: V1RemediationAgentFileDelete,
        PathValues.V1_REMEDIATION_AGENT_PROCESS_INFORMATION: V1RemediationAgentProcessInformation,
        PathValues.V1_REMEDIATION_AGENT_PROCESS_TERMINATE: V1RemediationAgentProcessTerminate,
        PathValues.V1_REMEDIATION_AGENT_VPN_SITE_ADD: V1RemediationAgentVpnSiteAdd,
        PathValues.V1_REMEDIATION_AGENT_VPN_SITE_REMOVE: V1RemediationAgentVpnSiteRemove,
        PathValues.V1_REMEDIATION_ANTIMALWARE_SCAN: V1RemediationAntiMalwareScan,
        PathValues.V1_REMEDIATION_ANTIMALWARE_UPDATE: V1RemediationAntiMalwareUpdate,
        PathValues.V1_REMEDIATION_ANTIMALWARE_RESTORE: V1RemediationAntiMalwareRestore,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_URL: V1RemediationForensicsAnalyzeByIndicatorUrl,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_IP: V1RemediationForensicsAnalyzeByIndicatorIp,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_PATH: V1RemediationForensicsAnalyzeByIndicatorPath,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_FILENAME: V1RemediationForensicsAnalyzeByIndicatorFileName,
        PathValues.V1_REMEDIATION_FORENSICS_ANALYZEBYINDICATOR_MD5: V1RemediationForensicsAnalyzeByIndicatorMd5,
        PathValues.V1_REMEDIATION_FORENSICS_FILE_QUARANTINE: V1RemediationForensicsFileQuarantine,
        PathValues.V1_REMEDIATION_FORENSICS_FILE_RESTORE: V1RemediationForensicsFileRestore,
        PathValues.V1_REMEDIATION_ISOLATE: V1RemediationIsolate,
        PathValues.V1_REMEDIATION_DEISOLATE: V1RemediationDeIsolate,
        PathValues.V1_REMEDIATION_STATUS: V1RemediationStatus,
        PathValues.V1_REMEDIATION_ID_STATUS: V1RemediationIdStatus,
        PathValues.V1_REMEDIATION_ID_ABORT: V1RemediationIdAbort,
        PathValues.V1_REMEDIATION_ID_RESULTS_SLIM: V1RemediationIdResultsSlim,
        PathValues.V1_QUARANTINEMANAGEMENT_FILE_DATA: V1QuarantineManagementFileData,
        PathValues.V1_QUARANTINEMANAGEMENT_FILE_RESTORE: V1QuarantineManagementFileRestore,
        PathValues.V1_QUARANTINEMANAGEMENT_FILE_FETCH: V1QuarantineManagementFileFetch,
        PathValues.V1_SESSION_KEEPALIVE: V1SessionKeepalive,
        PathValues.V1_SESSION_LOGIN_CLOUD: V1SessionLoginCloud,
    }
)
