import typing_extensions

from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags import TagValues
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.session_api import SessionApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.jobs_api import JobsApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.asset_management_api import AssetManagementApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.posture_management_vulnerabilities_api import PostureManagementVulnerabilitiesApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.quarantine_management_api import QuarantineManagementApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.indicators_of_compromise_api import IndicatorsOfCompromiseApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.remediation_response_general_api import RemediationResponseGeneralApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.remediation_response_agent_api import RemediationResponseAgentApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.remediation_response_threat_prevention_api import RemediationResponseThreatPreventionApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.policy_general_api import PolicyGeneralApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.policy_threat_prevention_api import PolicyThreatPreventionApi
from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tags.organizational_structure_api import OrganizationalStructureApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.SESSION: SessionApi,
        TagValues.JOBS: JobsApi,
        TagValues.ASSET_MANAGEMENT: AssetManagementApi,
        TagValues.POSTURE_MANAGEMENT__VULNERABILITIES: PostureManagementVulnerabilitiesApi,
        TagValues.QUARANTINE_MANAGEMENT: QuarantineManagementApi,
        TagValues.INDICATORS_OF_COMPROMISE: IndicatorsOfCompromiseApi,
        TagValues.REMEDIATION__RESPONSE__GENERAL: RemediationResponseGeneralApi,
        TagValues.REMEDIATION__RESPONSE__AGENT: RemediationResponseAgentApi,
        TagValues.REMEDIATION__RESPONSE__THREAT_PREVENTION: RemediationResponseThreatPreventionApi,
        TagValues.POLICY__GENERAL: PolicyGeneralApi,
        TagValues.POLICY__THREAT_PREVENTION: PolicyThreatPreventionApi,
        TagValues.ORGANIZATIONAL_STRUCTURE: OrganizationalStructureApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.SESSION: SessionApi,
        TagValues.JOBS: JobsApi,
        TagValues.ASSET_MANAGEMENT: AssetManagementApi,
        TagValues.POSTURE_MANAGEMENT__VULNERABILITIES: PostureManagementVulnerabilitiesApi,
        TagValues.QUARANTINE_MANAGEMENT: QuarantineManagementApi,
        TagValues.INDICATORS_OF_COMPROMISE: IndicatorsOfCompromiseApi,
        TagValues.REMEDIATION__RESPONSE__GENERAL: RemediationResponseGeneralApi,
        TagValues.REMEDIATION__RESPONSE__AGENT: RemediationResponseAgentApi,
        TagValues.REMEDIATION__RESPONSE__THREAT_PREVENTION: RemediationResponseThreatPreventionApi,
        TagValues.POLICY__GENERAL: PolicyGeneralApi,
        TagValues.POLICY__THREAT_PREVENTION: PolicyThreatPreventionApi,
        TagValues.ORGANIZATIONAL_STRUCTURE: OrganizationalStructureApi,
    }
)
