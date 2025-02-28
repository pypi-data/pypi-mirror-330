# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from chkp_harmony_endpoint_management_sdk.generated.saas.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    PUBLIC_MSSP_V1_OPERATIONAL = "/public/mssp/v1/operational"
    PUBLIC_MSSP_V1_OPERATIONAL_TRENDS_CONNECTED = "/public/mssp/v1/operational/trends/connected"
    PUBLIC_MSSP_V1_SERVICE_STATUS = "/public/mssp/v1/service/status"
    PUBLIC_MSSP_V1_SERVICE_OPERATION = "/public/mssp/v1/service/operation"
    PUBLIC_MSSP_V1_SERVICE_TERMINATE = "/public/mssp/v1/service/terminate"
    PUBLIC_MSSP_V1_SERVICE_DEPLOY = "/public/mssp/v1/service/deploy"
    PUBLIC_V1_SELFSERVICE_STATUS = "/public/v1/self-service/status"
    PUBLIC_V1_SELFSERVICE_DEPLOY = "/public/v1/self-service/deploy"
    PUBLIC_V1_SELFSERVICE_TERMINATE_MACHINE_ID = "/public/v1/self-service/terminate/{machineId}"
    PUBLIC_MSSP_V1_SESSION_LOGIN = "/public/mssp/v1/session/login"
    PUBLIC_MSSP_V1_SESSION_KEEPALIVE = "/public/mssp/v1/session/keep-alive"
