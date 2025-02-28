import typing_extensions

from chkp_harmony_endpoint_management_sdk.generated.saas.paths import PathValues
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_operational import PublicMsspV1Operational
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_operational_trends_connected import PublicMsspV1OperationalTrendsConnected
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_service_status import PublicMsspV1ServiceStatus
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_service_operation import PublicMsspV1ServiceOperation
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_service_terminate import PublicMsspV1ServiceTerminate
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_service_deploy import PublicMsspV1ServiceDeploy
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_v1_self_service_status import PublicV1SelfServiceStatus
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_v1_self_service_deploy import PublicV1SelfServiceDeploy
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_v1_self_service_terminate_machine_id import PublicV1SelfServiceTerminateMachineId
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_session_login import PublicMsspV1SessionLogin
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.paths.public_mssp_v1_session_keep_alive import PublicMsspV1SessionKeepAlive

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.PUBLIC_MSSP_V1_OPERATIONAL: PublicMsspV1Operational,
        PathValues.PUBLIC_MSSP_V1_OPERATIONAL_TRENDS_CONNECTED: PublicMsspV1OperationalTrendsConnected,
        PathValues.PUBLIC_MSSP_V1_SERVICE_STATUS: PublicMsspV1ServiceStatus,
        PathValues.PUBLIC_MSSP_V1_SERVICE_OPERATION: PublicMsspV1ServiceOperation,
        PathValues.PUBLIC_MSSP_V1_SERVICE_TERMINATE: PublicMsspV1ServiceTerminate,
        PathValues.PUBLIC_MSSP_V1_SERVICE_DEPLOY: PublicMsspV1ServiceDeploy,
        PathValues.PUBLIC_V1_SELFSERVICE_STATUS: PublicV1SelfServiceStatus,
        PathValues.PUBLIC_V1_SELFSERVICE_DEPLOY: PublicV1SelfServiceDeploy,
        PathValues.PUBLIC_V1_SELFSERVICE_TERMINATE_MACHINE_ID: PublicV1SelfServiceTerminateMachineId,
        PathValues.PUBLIC_MSSP_V1_SESSION_LOGIN: PublicMsspV1SessionLogin,
        PathValues.PUBLIC_MSSP_V1_SESSION_KEEPALIVE: PublicMsspV1SessionKeepAlive,
    }
)

path_to_api = PathToApi(
    {
        PathValues.PUBLIC_MSSP_V1_OPERATIONAL: PublicMsspV1Operational,
        PathValues.PUBLIC_MSSP_V1_OPERATIONAL_TRENDS_CONNECTED: PublicMsspV1OperationalTrendsConnected,
        PathValues.PUBLIC_MSSP_V1_SERVICE_STATUS: PublicMsspV1ServiceStatus,
        PathValues.PUBLIC_MSSP_V1_SERVICE_OPERATION: PublicMsspV1ServiceOperation,
        PathValues.PUBLIC_MSSP_V1_SERVICE_TERMINATE: PublicMsspV1ServiceTerminate,
        PathValues.PUBLIC_MSSP_V1_SERVICE_DEPLOY: PublicMsspV1ServiceDeploy,
        PathValues.PUBLIC_V1_SELFSERVICE_STATUS: PublicV1SelfServiceStatus,
        PathValues.PUBLIC_V1_SELFSERVICE_DEPLOY: PublicV1SelfServiceDeploy,
        PathValues.PUBLIC_V1_SELFSERVICE_TERMINATE_MACHINE_ID: PublicV1SelfServiceTerminateMachineId,
        PathValues.PUBLIC_MSSP_V1_SESSION_LOGIN: PublicMsspV1SessionLogin,
        PathValues.PUBLIC_MSSP_V1_SESSION_KEEPALIVE: PublicMsspV1SessionKeepAlive,
    }
)
