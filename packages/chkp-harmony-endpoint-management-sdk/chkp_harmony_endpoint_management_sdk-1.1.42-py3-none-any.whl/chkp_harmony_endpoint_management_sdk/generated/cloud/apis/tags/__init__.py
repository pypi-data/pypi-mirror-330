# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from chkp_harmony_endpoint_management_sdk.generated.cloud.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    SESSION = "Session"
    JOBS = "Jobs"
    ASSET_MANAGEMENT = "Asset Management"
    POSTURE_MANAGEMENT__VULNERABILITIES = "Posture Management - Vulnerabilities"
    QUARANTINE_MANAGEMENT = "Quarantine Management"
    INDICATORS_OF_COMPROMISE = "Indicators of Compromise"
    REMEDIATION__RESPONSE__GENERAL = "Remediation &amp; Response - General"
    REMEDIATION__RESPONSE__AGENT = "Remediation &amp; Response - Agent"
    REMEDIATION__RESPONSE__THREAT_PREVENTION = "Remediation &amp; Response - Threat Prevention"
    POLICY__GENERAL = "Policy - General"
    POLICY__THREAT_PREVENTION = "Policy - Threat Prevention"
    ORGANIZATIONAL_STRUCTURE = "Organizational Structure"
