# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from chkp_harmony_endpoint_management_sdk.generated.saas.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    MANAGE_SESSION = "Manage Session"
    MSSP_SERVICE = "Mssp Service"
    OPERATIONAL = "Operational"
    SELF_SERVICE = "Self Service"
