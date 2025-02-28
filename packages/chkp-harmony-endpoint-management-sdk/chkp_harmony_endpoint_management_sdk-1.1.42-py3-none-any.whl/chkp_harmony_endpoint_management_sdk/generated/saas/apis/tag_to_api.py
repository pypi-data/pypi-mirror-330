import typing_extensions

from chkp_harmony_endpoint_management_sdk.generated.saas.apis.tags import TagValues
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.tags.manage_session_api import ManageSessionApi
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.tags.mssp_service_api import MsspServiceApi
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.tags.operational_api import OperationalApi
from chkp_harmony_endpoint_management_sdk.generated.saas.apis.tags.self_service_api import SelfServiceApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.MANAGE_SESSION: ManageSessionApi,
        TagValues.MSSP_SERVICE: MsspServiceApi,
        TagValues.OPERATIONAL: OperationalApi,
        TagValues.SELF_SERVICE: SelfServiceApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.MANAGE_SESSION: ManageSessionApi,
        TagValues.MSSP_SERVICE: MsspServiceApi,
        TagValues.OPERATIONAL: OperationalApi,
        TagValues.SELF_SERVICE: SelfServiceApi,
    }
)
