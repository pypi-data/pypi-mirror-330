# coding: utf-8

"""
    Harmony Endpoint Management API

    <style>details{user-select:none}details>summary span.icon{width:24px;height:24px;transition:all .3s;margin-left:auto}details>ol>li{padding-bottom:20px}summary{cursor:pointer}summary::-webkit-details-marker{display:none}</style><h2>Today more than ever, endpoint security plays a critical role in enabling your remote workforce.</h2><h4>Harmony Endpoint provides comprehensive endpoint protection at the highest security level that is crucial to avoid security breaches and data compromise.</h4><p>The following documentation provides the operations supported by the Harmony Endpoint's External API.</p><p>To use the Harmony Endpoint External API service:</p><ol><li><p>In the <em>Infinity Portal</em>, create a suitable API Key. In the <em>Service</em> field, enter <em>Endpoint</em>.<br>For more information, refer to the <a href=\"https://sc1.checkpoint.com/documents/Infinity_Portal/WebAdminGuides/EN/Infinity-Portal-Admin-Guide/Content/Topics-Infinity-Portal/API-Keys.htm?tocpath=Global%20Settings%7C_____7#API_Keys\">Infinity Portal Administration Guide</a>.<br>Once a key has been created, it may be used indefinitely (unless an expiration date was explicitly set for it).</p>During the key's creation, note the presented <em>Authentication URL</em>. This URL is used to obtain <em>Bearer tokens</em> for the next step</li><li><p>Authenticate using the <em>Infinity Portal's</em> External Authentication Service.<br>The authentication request should be made to the <em>Authentication URL</em> obtained during the previous step.</p><p>Example (<em>Your tenant's authentication URL may differ</em>):</p><p><img src=\"data:image/png;base64,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\"></p><p>Note, image is for reference only. Exact <em>CURL</em> syntax may differ.</p></li><li><p>Include the resulting <em>token</em> in the <em>Authorization</em> header in the form of a <em>Bearer</em> (For example, 'Authorization': 'Bearer {TOKEN}') in every request made to the API service</p></li><li><p>Call the <a href=\"#/Session/LoginCloud\">Cloud Login API</a></p></li><li><p>Include the resulting <em>x-mgmt-api-token</em> in Header <em>x-mgmt-api-token</em> of all subsequent requests</p></li></ol><br><div><p>For your convinience, <em>Harmony Endpoint</em> API SDKs are available here:</p><ul><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-py-sdk\">Python 3.8 and newer</a></li><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-js-ts-sdk\">TypeScript</a></li></ul></div><div><p>In addition, a command-line interface is available <a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-cli\">here</a></p></div><br><div style=\"margin-top:15px;padding-top:30px;padding-bottom:30px\"><h3>Important Notes:</h3><div style=\"margin-left:25px\"><p></p><ul><li style=\"margin-bottom:30px\"><p>When creating an API key, the selected service <b><em>must</em></b> be <em>Endpoint</em> or requests will not be delivered to the service.</p></li><li style=\"margin-bottom:30px\"><p>Operation payload examples should be treated as guidelines and should not be used as-is.</p><p style=\"margin-top:-7px\">Calling a remediation operation, for instance, with the contents of its example will fail.</p></li><li style=\"margin-bottom:30px\"><p>The <em>Harmony Endpoint</em> API service enforces rate-limiting.</p><p style=\"margin-top:-7px\">Please ensure your integration correctly handles <code>HTTP 429 (Too many requests)</code> responses by using appropriate delays and back-off mechanisms.</p></li><li style=\"margin-bottom:30px\"><p>Errors returned by the <em>Harmony Endpoint</em> API service conform, to a large degree, to <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> and convey useful data.</p><p style=\"margin-top:-7px\">It is highly recommended your integration logs the full error as most issues can quickly be pinpointed and rectified by viewing the error contents.</p></li></ul><p></p></div></div><br><div style=\"padding-top:30px;padding-bottom:30px\"><details><summary style=\"font-size:large;font-weight:600;padding-bottom:20px\">Troubleshooting</summary><div style=\"margin-left:25px\"><p>During usage, you may encounter different issues and errors.</p><p>To facilitate resolution of such issues, the <em>Harmony Endpoint API service uses an <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> compliant error structure</em> which conveys information like the type of error that occurred and its source and even potential fixes.<br>This is the first and often last step in diagnosing API related issues.</p><p>The below list is of common errors that may not be obvious from the error message alone.</p><h5>Important notes</h5><ol><li>API errors may be wrapped by a separate object. The content of the errors however is as specified</li><li>Errors that do not follow <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> can be assumed to originate from <em>Infinity Portal</em> which implies a failure in authentication.</li></ol><p></p><p style=\"margin-top:40px\">If you encounter an error that is not listed here and require help, please open a support ticket or request assistance via the e-mail address at the bottom of this documentation page.</p><p style=\"padding-top:10px\">When opening a support ticket, please also provide the following information:</p><ul><li style=\"padding-bottom:8px\">The name and/or address of the API operation</li><li style=\"padding-bottom:8px\">The approximate date and time (including timezone) when you last encountered the issue</li><li style=\"padding-bottom:8px\"><p>The full request (body and headers).</p><p style=\"margin-top:-15px\">For issues pertaining to authentication/login, include your expired <em>Infinity Portal</em> bearer token.</p></li><li style=\"padding-bottom:8px\">The full response returned by the <em>Harmony Endpoint</em> API service</li><li style=\"padding-bottom:8px\">Your use case. For example, \"<em>Retrieving asset information for SIEM integration</em>\" (<b>Optional</b>)</li></ul><p></p><hr style=\"margin-top:25px;margin-bottom:25px\"><div style=\"margin-left:30px\"><details style=\"padding-bottom:15px\"><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"An error has occurred\" }</samp> when authenticating against the <em>Infinity Portal</em></summary><div><h4>Issue:</h4><p>This error usually indicates your authentication request was malformed.</p><h4>Possible Solutions:</h4><p>Make sure your request is a valid JSON, includes header <samp>Content-Type</samp> with a value of <samp>application/json</samp> and looks like <samp>{ \"clientId\": \"{{ciClientId}}\", \"accessKey\": \"{{ciAccessKey}}\" }</samp></p></div></details><details><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"Authentication required\", \"forceLogout\": true }</samp> when invoking Harmony Endpoint API operations</summary><div><h4>Issue:</h4><p>This error indicates that you have attempted to access a resource without a valid Bearer authoriztion token.</p><p>An example could be an attempt to invoke a Harmony Endpoint API operation without providing an <em>Infinity Portal</em> token in the request's <samp>Authorization</samp> header</p><p>Specific cases where this error is raised include:</p><ol><li>A request was made without providing an <em>Infinity Portal</em> bearer token in the <samp>Authorization</samp> header</li><li>A request was directed to to an <em>Infinity Portal</em> gateway other than the one that issued the bearer token</li><li>The provided token is intended for another <em>Infinity Portal</em> application</li><li>The provided token is expired</li><li>The provided token is malformed</li></ol><p></p><h4>Possible Solutions:</h4><p></p><ol><li>Verify the token was created to target the correct application (<em>Endpoint</em>)</li><li>Verify the token has not expired</li><li>Verify the token is being used correctly in the requst (<samp>Authorization: Bearer {{TOKEN}}</samp>)</li></ol><p></p></div></details></div></div></details><br><br></div>  # noqa: E501

    The version of the OpenAPI document: 1.9.221
    Contact: harmony-endpoint-external-api@checkpoint.com
    Generated by: https://openapi-generator.tech
"""

import copy
import logging
import multiprocessing
import sys
import urllib3

from http import client as http_client
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiValueError


JSON_SCHEMA_VALIDATION_KEYWORDS = {
    'multipleOf', 'maximum', 'exclusiveMaximum',
    'minimum', 'exclusiveMinimum', 'maxLength',
    'minLength', 'pattern', 'maxItems', 'minItems',
    'uniqueItems', 'maxProperties', 'minProperties',
}

class Configuration(object):
    """NOTE: This class is auto generated by OpenAPI Generator

    Ref: https://openapi-generator.tech
    Do not edit the class manually.

    :param host: Base url
    :param api_key: Dict to store API key(s).
      Each entry in the dict specifies an API key.
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is the API key secret.
    :param api_key_prefix: Dict to store API prefix (e.g. Bearer)
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is an API key prefix when generating the auth data.
    :param username: Username for HTTP basic authentication
    :param password: Password for HTTP basic authentication
    :param discard_unknown_keys: Boolean value indicating whether to discard
      unknown properties. A server may send a response that includes additional
      properties that are not known by the client in the following scenarios:
      1. The OpenAPI document is incomplete, i.e. it does not match the server
         implementation.
      2. The client was generated using an older version of the OpenAPI document
         and the server has been upgraded since then.
      If a schema in the OpenAPI document defines the additionalProperties attribute,
      then all undeclared properties received by the server are injected into the
      additional properties map. In that case, there are undeclared properties, and
      nothing to discard.
    :param disabled_client_side_validations (string): Comma-separated list of
      JSON schema validation keywords to disable JSON schema structural validation
      rules. The following keywords may be specified: multipleOf, maximum,
      exclusiveMaximum, minimum, exclusiveMinimum, maxLength, minLength, pattern,
      maxItems, minItems.
      By default, the validation is performed for data generated locally by the client
      and data received from the server, independent of any validation performed by
      the server side. If the input data does not satisfy the JSON schema validation
      rules specified in the OpenAPI document, an exception is raised.
      If disabled_client_side_validations is set, structural validation is
      disabled. This can be useful to troubleshoot data validation problem, such as
      when the OpenAPI document validation rules do not match the actual API data
      received by the server.
    :param server_index: Index to servers configuration.
    :param server_variables: Mapping with string values to replace variables in
      templated server configuration. The validation of enums is performed for
      variables with defined enum values before.
    :param server_operation_index: Mapping from operation ID to an index to server
      configuration.
    :param server_operation_variables: Mapping from operation ID to a mapping with
      string values to replace variables in templated server configuration.
      The validation of enums is performed for variables with defined enum values before.

    :Example:

    API Key Authentication Example.
    Given the following security scheme in the OpenAPI specification:
      components:
        securitySchemes:
          cookieAuth:         # name for the security scheme
            type: apiKey
            in: cookie
            name: JSESSIONID  # cookie name

    You can programmatically set the cookie:

conf = chkp_harmony_endpoint_management_sdk.generated.cloud.Configuration(
    api_key={'cookieAuth': 'abc123'}
    api_key_prefix={'cookieAuth': 'JSESSIONID'}
)

    The following cookie will be added to the HTTP request:
       Cookie: JSESSIONID abc123
    """

    _default = None

    def __init__(
        self,
        host=None,
        api_key=None,
        api_key_prefix=None,
        discard_unknown_keys=False,
        disabled_client_side_validations="",
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
        access_token=None,
    ):
        """Constructor
        """
        self._base_path = "https://cloudinfra-gw.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api" if host is None else host
        """Default Base url
        """
        self.server_index = 0 if server_index is None and host is None else server_index
        self.server_operation_index = server_operation_index or {}
        """Default server index
        """
        self.server_variables = server_variables or {}
        self.server_operation_variables = server_operation_variables or {}
        """Default server variables
        """
        self.temp_folder_path = None
        """Temp file folder for downloading files
        """
        # Authentication Settings
        self.api_key = {}
        if api_key:
            self.api_key = api_key
        """dict to store API key(s)
        """
        self.api_key_prefix = {}
        if api_key_prefix:
            self.api_key_prefix = api_key_prefix
        """dict to store API prefix (e.g. Bearer)
        """
        self.refresh_api_key_hook = None
        """function hook to refresh API key if expired
        """
        self.disabled_client_side_validations = disabled_client_side_validations
        self.access_token = None
        """access token for OAuth/Bearer
        """
        self.logger = {}
        """Logging Settings
        """
        self.logger["package_logger"] = logging.getLogger("chkp_harmony_endpoint_management_sdk.generated.cloud")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        self.logger_format = '%(asctime)s %(levelname)s %(message)s'
        """Log format
        """
        self.logger_stream_handler = None
        """Log stream handler
        """
        self.logger_file_handler = None
        """Log file handler
        """
        self.logger_file = None
        """Debug file location
        """
        self.debug = False
        """Debug switch
        """

        self.verify_ssl = True
        """SSL/TLS verification
           Set this to false to skip verifying SSL certificate when calling API
           from https server.
        """
        self.ssl_ca_cert = None
        """Set this to customize the certificate file to verify the peer.
        """
        self.cert_file = None
        """client certificate file
        """
        self.key_file = None
        """client key file
        """
        self.assert_hostname = None
        """Set this to True/False to enable/disable SSL hostname verification.
        """
        self.tls_server_name = None
        """SSL/TLS Server Name Indication (SNI)
           Set this to the SNI value expected by the server.
        """

        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5
        """urllib3 connection pool's maximum number of connections saved
           per pool. urllib3 uses 1 connection as default value, but this is
           not the best value when you are making a lot of possibly parallel
           requests to the same host, which is often the case here.
           cpu_count * 5 is used as default value to increase performance.
        """

        self.proxy = None
        """Proxy URL
        """
        self.proxy_headers = None
        """Proxy headers
        """
        self.safe_chars_for_path_param = ''
        """Safe chars for path_param
        """
        self.retries = None
        """Adding retries to override urllib3 default value 3
        """
        # Enable client side validation
        self.client_side_validation = True

        # Options to pass down to the underlying urllib3 socket
        self.socket_options = None

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k not in ('logger', 'logger_file_handler'):
                setattr(result, k, copy.deepcopy(v, memo))
        # shallow copy of loggers
        result.logger = copy.copy(self.logger)
        # use setters to configure loggers
        result.logger_file = self.logger_file
        result.debug = self.debug
        return result

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == 'disabled_client_side_validations':
            s = set(filter(None, value.split(',')))
            for v in s:
                if v not in JSON_SCHEMA_VALIDATION_KEYWORDS:
                    raise ApiValueError(
                        "Invalid keyword: '{0}''".format(v))
            self._disabled_client_side_validations = s

    @classmethod
    def set_default(cls, default):
        """Set default instance of configuration.

        It stores default configuration, which can be
        returned by get_default_copy method.

        :param default: object of Configuration
        """
        cls._default = copy.deepcopy(default)

    @classmethod
    def get_default_copy(cls):
        """Return new instance of configuration.

        This method returns newly created, based on default constructor,
        object of Configuration class or returns a copy of default
        configuration passed by the set_default method.

        :return: The configuration object.
        """
        if cls._default is not None:
            return copy.deepcopy(cls._default)
        return Configuration()

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        return self.__logger_file

    @logger_file.setter
    def logger_file(self, value):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        self.__logger_file = value
        if self.__logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in self.logger.items():
                logger.addHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self.__debug = value
        if self.__debug:
            # if debug status is True, turn on debug logging
            for _, logger in self.logger.items():
                logger.setLevel(logging.DEBUG)
            # turn on http_client debug
            http_client.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in self.logger.items():
                logger.setLevel(logging.WARNING)
            # turn off http_client debug
            http_client.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(self, identifier, alias=None):
        """Gets API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :param alias: The alternative identifier of apiKey.
        :return: The token for api key authentication.
        """
        if self.refresh_api_key_hook is not None:
            self.refresh_api_key_hook(self)
        key = self.api_key.get(identifier, self.api_key.get(alias) if alias is not None else None)
        if key:
            prefix = self.api_key_prefix.get(identifier)
            if prefix:
                return "%s %s" % (prefix, key)
            else:
                return key

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        username = ""
        if self.username is not None:
            username = self.username
        password = ""
        if self.password is not None:
            password = self.password
        return urllib3.util.make_headers(
            basic_auth=username + ':' + password
        ).get('authorization')

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        auth = {}
        if self.access_token is not None:
            auth['cloudInfraJwt'] = {
                'type': 'bearer',
                'in': 'header',
                'format': 'Infinity Portal Token',
                'key': 'Authorization',
                'value': 'Bearer ' + self.access_token
            }
        if 'apiJwt' in self.api_key:
            auth['apiJwt'] = {
                'type': 'api_key',
                'in': 'header',
                'key': 'x-mgmt-api-token',
                'value': self.get_api_key_with_prefix(
                    'apiJwt',
                ),
            }
        return auth

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 1.9.221\n"\
               "SDK Package Version: 1.0.0".\
               format(env=sys.platform, pyversion=sys.version)

    def get_host_settings(self):
        """Gets an array of host settings

        :return: An array of host settings
        """
        return [
            {
                'url': "https://cloudinfra-gw.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api",
                'description': "Access via the Infinity Portal gateway based in Dublin, Ireland",
            },
            {
                'url': "https://cloudinfra-gw-us.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api",
                'description': "Access via the Infinity Portal gateway based in North Virginia, USA",
            },
            {
                'url': "https://cloudinfra-gw.ap.portal.checkpoint.com/app/endpoint-web-mgmt/harmony/endpoint/api",
                'description': "Access via the Infinity Portal gateway based in Sydney, Australlia",
            }
        ]

    def get_host_from_settings(self, index, variables=None, servers=None):
        """Gets host URL based on the index and variables
        :param index: array index of the host settings
        :param variables: hash of variable and the corresponding value
        :param servers: an array of host settings or None
        :return: URL based on host settings
        """
        if index is None:
            return self._base_path

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                "Invalid index {0} when selecting the host settings. "
                "Must be less than {1}".format(index, len(servers)))

        url = server['url']

        # go through variables and replace placeholders
        for variable_name, variable in server.get('variables', {}).items():
            used_value = variables.get(
                variable_name, variable['default_value'])

            if 'enum_values' in variable \
                    and used_value not in variable['enum_values']:
                raise ValueError(
                    "The variable `{0}` in the host URL has invalid value "
                    "{1}. Must be {2}.".format(
                        variable_name, variables[variable_name],
                        variable['enum_values']))

            url = url.replace("{" + variable_name + "}", used_value)

        return url

    @property
    def host(self):
        """Return generated host."""
        return self.get_host_from_settings(self.server_index, variables=self.server_variables)

    @host.setter
    def host(self, value):
        """Fix base path."""
        self._base_path = value
        self.server_index = None
