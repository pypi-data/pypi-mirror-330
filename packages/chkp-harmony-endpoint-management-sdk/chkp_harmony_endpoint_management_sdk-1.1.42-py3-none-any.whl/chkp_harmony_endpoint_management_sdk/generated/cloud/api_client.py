# coding: utf-8
"""
    Harmony Endpoint Management API

    <style>details{user-select:none}details>summary span.icon{width:24px;height:24px;transition:all .3s;margin-left:auto}details>ol>li{padding-bottom:20px}summary{cursor:pointer}summary::-webkit-details-marker{display:none}</style><h2>Today more than ever, endpoint security plays a critical role in enabling your remote workforce.</h2><h4>Harmony Endpoint provides comprehensive endpoint protection at the highest security level that is crucial to avoid security breaches and data compromise.</h4><p>The following documentation provides the operations supported by the Harmony Endpoint's External API.</p><p>To use the Harmony Endpoint External API service:</p><ol><li><p>In the <em>Infinity Portal</em>, create a suitable API Key. In the <em>Service</em> field, enter <em>Endpoint</em>.<br>For more information, refer to the <a href=\"https://sc1.checkpoint.com/documents/Infinity_Portal/WebAdminGuides/EN/Infinity-Portal-Admin-Guide/Content/Topics-Infinity-Portal/API-Keys.htm?tocpath=Global%20Settings%7C_____7#API_Keys\">Infinity Portal Administration Guide</a>.<br>Once a key has been created, it may be used indefinitely (unless an expiration date was explicitly set for it).</p>During the key's creation, note the presented <em>Authentication URL</em>. This URL is used to obtain <em>Bearer tokens</em> for the next step</li><li><p>Authenticate using the <em>Infinity Portal's</em> External Authentication Service.<br>The authentication request should be made to the <em>Authentication URL</em> obtained during the previous step.</p><p>Example (<em>Your tenant's authentication URL may differ</em>):</p><p><img src=\"data:image/png;base64,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\"></p><p>Note, image is for reference only. Exact <em>CURL</em> syntax may differ.</p></li><li><p>Include the resulting <em>token</em> in the <em>Authorization</em> header in the form of a <em>Bearer</em> (For example, 'Authorization': 'Bearer {TOKEN}') in every request made to the API service</p></li><li><p>Call the <a href=\"#/Session/LoginCloud\">Cloud Login API</a></p></li><li><p>Include the resulting <em>x-mgmt-api-token</em> in Header <em>x-mgmt-api-token</em> of all subsequent requests</p></li></ol><br><div><p>For your convinience, <em>Harmony Endpoint</em> API SDKs are available here:</p><ul><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-py-sdk\">Python 3.8 and newer</a></li><li><a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-js-ts-sdk\">TypeScript</a></li></ul></div><div><p>In addition, a command-line interface is available <a href=\"https://github.com/CheckPointSW/harmony-endpoint-management-cli\">here</a></p></div><br><div style=\"margin-top:15px;padding-top:30px;padding-bottom:30px\"><h3>Important Notes:</h3><div style=\"margin-left:25px\"><p></p><ul><li style=\"margin-bottom:30px\"><p>When creating an API key, the selected service <b><em>must</em></b> be <em>Endpoint</em> or requests will not be delivered to the service.</p></li><li style=\"margin-bottom:30px\"><p>Operation payload examples should be treated as guidelines and should not be used as-is.</p><p style=\"margin-top:-7px\">Calling a remediation operation, for instance, with the contents of its example will fail.</p></li><li style=\"margin-bottom:30px\"><p>The <em>Harmony Endpoint</em> API service enforces rate-limiting.</p><p style=\"margin-top:-7px\">Please ensure your integration correctly handles <code>HTTP 429 (Too many requests)</code> responses by using appropriate delays and back-off mechanisms.</p></li><li style=\"margin-bottom:30px\"><p>Errors returned by the <em>Harmony Endpoint</em> API service conform, to a large degree, to <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> and convey useful data.</p><p style=\"margin-top:-7px\">It is highly recommended your integration logs the full error as most issues can quickly be pinpointed and rectified by viewing the error contents.</p></li></ul><p></p></div></div><br><div style=\"padding-top:30px;padding-bottom:30px\"><details><summary style=\"font-size:large;font-weight:600;padding-bottom:20px\">Troubleshooting</summary><div style=\"margin-left:25px\"><p>During usage, you may encounter different issues and errors.</p><p>To facilitate resolution of such issues, the <em>Harmony Endpoint API service uses an <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> compliant error structure</em> which conveys information like the type of error that occurred and its source and even potential fixes.<br>This is the first and often last step in diagnosing API related issues.</p><p>The below list is of common errors that may not be obvious from the error message alone.</p><h5>Important notes</h5><ol><li>API errors may be wrapped by a separate object. The content of the errors however is as specified</li><li>Errors that do not follow <a href=\"https://www.rfc-editor.org/rfc/rfc7807\">RFC7807</a> can be assumed to originate from <em>Infinity Portal</em> which implies a failure in authentication.</li></ol><p></p><p style=\"margin-top:40px\">If you encounter an error that is not listed here and require help, please open a support ticket or request assistance via the e-mail address at the bottom of this documentation page.</p><p style=\"padding-top:10px\">When opening a support ticket, please also provide the following information:</p><ul><li style=\"padding-bottom:8px\">The name and/or address of the API operation</li><li style=\"padding-bottom:8px\">The approximate date and time (including timezone) when you last encountered the issue</li><li style=\"padding-bottom:8px\"><p>The full request (body and headers).</p><p style=\"margin-top:-15px\">For issues pertaining to authentication/login, include your expired <em>Infinity Portal</em> bearer token.</p></li><li style=\"padding-bottom:8px\">The full response returned by the <em>Harmony Endpoint</em> API service</li><li style=\"padding-bottom:8px\">Your use case. For example, \"<em>Retrieving asset information for SIEM integration</em>\" (<b>Optional</b>)</li></ul><p></p><hr style=\"margin-top:25px;margin-bottom:25px\"><div style=\"margin-left:30px\"><details style=\"padding-bottom:15px\"><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"An error has occurred\" }</samp> when authenticating against the <em>Infinity Portal</em></summary><div><h4>Issue:</h4><p>This error usually indicates your authentication request was malformed.</p><h4>Possible Solutions:</h4><p>Make sure your request is a valid JSON, includes header <samp>Content-Type</samp> with a value of <samp>application/json</samp> and looks like <samp>{ \"clientId\": \"{{ciClientId}}\", \"accessKey\": \"{{ciAccessKey}}\" }</samp></p></div></details><details><summary style=\"font-size:medium;font-weight:400\">You receive a message like <samp>{ \"success\": false, \"message\": \"Authentication required\", \"forceLogout\": true }</samp> when invoking Harmony Endpoint API operations</summary><div><h4>Issue:</h4><p>This error indicates that you have attempted to access a resource without a valid Bearer authoriztion token.</p><p>An example could be an attempt to invoke a Harmony Endpoint API operation without providing an <em>Infinity Portal</em> token in the request's <samp>Authorization</samp> header</p><p>Specific cases where this error is raised include:</p><ol><li>A request was made without providing an <em>Infinity Portal</em> bearer token in the <samp>Authorization</samp> header</li><li>A request was directed to to an <em>Infinity Portal</em> gateway other than the one that issued the bearer token</li><li>The provided token is intended for another <em>Infinity Portal</em> application</li><li>The provided token is expired</li><li>The provided token is malformed</li></ol><p></p><h4>Possible Solutions:</h4><p></p><ol><li>Verify the token was created to target the correct application (<em>Endpoint</em>)</li><li>Verify the token has not expired</li><li>Verify the token is being used correctly in the requst (<samp>Authorization: Bearer {{TOKEN}}</samp>)</li></ol><p></p></div></details></div></div></details><br><br></div>  # noqa: E501

    The version of the OpenAPI document: 1.9.221
    Contact: harmony-endpoint-external-api@checkpoint.com
    Generated by: https://openapi-generator.tech
"""

from dataclasses import dataclass
from decimal import Decimal
import enum
import email
import json
import os
import io
import atexit
from multiprocessing.pool import ThreadPool
import re
import tempfile
import typing
import typing_extensions
import urllib3
from urllib3._collections import HTTPHeaderDict
from urllib.parse import urlparse, quote
from urllib3.fields import RequestField as RequestFieldBase

import frozendict

from chkp_harmony_endpoint_management_sdk.generated.cloud import rest
from chkp_harmony_endpoint_management_sdk.generated.cloud.configuration import Configuration
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiTypeError, ApiValueError
from chkp_harmony_endpoint_management_sdk.generated.cloud.schemas import (
    NoneClass,
    BoolClass,
    Schema,
    FileIO,
    BinarySchema,
    date,
    datetime,
    none_type,
    Unset,
    unset,
)


class RequestField(RequestFieldBase):
    def __eq__(self, other):
        if not isinstance(other, RequestField):
            return False
        return self.__dict__ == other.__dict__


class JSONEncoder(json.JSONEncoder):
    compact_separators = (',', ':')

    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, Decimal):
            if obj.as_tuple().exponent >= 0:
                return int(obj)
            return float(obj)
        elif isinstance(obj, NoneClass):
            return None
        elif isinstance(obj, BoolClass):
            return bool(obj)
        elif isinstance(obj, (dict, frozendict.frozendict)):
            return {key: self.default(val) for key, val in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.default(item) for item in obj]
        raise ApiValueError('Unable to prepare type {} for serialization'.format(obj.__class__.__name__))


class ParameterInType(enum.Enum):
    QUERY = 'query'
    HEADER = 'header'
    PATH = 'path'
    COOKIE = 'cookie'


class ParameterStyle(enum.Enum):
    MATRIX = 'matrix'
    LABEL = 'label'
    FORM = 'form'
    SIMPLE = 'simple'
    SPACE_DELIMITED = 'spaceDelimited'
    PIPE_DELIMITED = 'pipeDelimited'
    DEEP_OBJECT = 'deepObject'


class PrefixSeparatorIterator:
    # A class to store prefixes and separators for rfc6570 expansions

    def __init__(self, prefix: str, separator: str):
        self.prefix = prefix
        self.separator = separator
        self.first = True
        if separator in {'.', '|', '%20'}:
            item_separator = separator
        else:
            item_separator = ','
        self.item_separator = item_separator

    def __iter__(self):
        return self

    def __next__(self):
        if self.first:
            self.first = False
            return self.prefix
        return self.separator


class ParameterSerializerBase:
    @classmethod
    def _get_default_explode(cls, style: ParameterStyle) -> bool:
        return False

    @staticmethod
    def __ref6570_item_value(in_data: typing.Any, percent_encode: bool):
        """
        Get representation if str/float/int/None/items in list/ values in dict
        None is returned if an item is undefined, use cases are value=
        - None
        - []
        - {}
        - [None, None None]
        - {'a': None, 'b': None}
        """
        if type(in_data) in {str, float, int}:
            if percent_encode:
                return quote(str(in_data))
            return str(in_data)
        elif isinstance(in_data, none_type):
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        elif isinstance(in_data, list) and not in_data:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        elif isinstance(in_data, dict) and not in_data:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        raise ApiValueError('Unable to generate a ref6570 item representation of {}'.format(in_data))

    @staticmethod
    def _to_dict(name: str, value: str):
        return {name: value}

    @classmethod
    def __ref6570_str_float_int_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_value = cls.__ref6570_item_value(in_data, percent_encode)
        if item_value is None or (item_value == '' and prefix_separator_iterator.separator == ';'):
            return next(prefix_separator_iterator) + var_name_piece
        value_pair_equals = '=' if named_parameter_expansion else ''
        return next(prefix_separator_iterator) + var_name_piece + value_pair_equals + item_value

    @classmethod
    def __ref6570_list_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_values = [cls.__ref6570_item_value(v, percent_encode) for v in in_data]
        item_values = [v for v in item_values if v is not None]
        if not item_values:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        value_pair_equals = '=' if named_parameter_expansion else ''
        if not explode:
            return (
                next(prefix_separator_iterator) +
                var_name_piece +
                value_pair_equals +
                prefix_separator_iterator.item_separator.join(item_values)
            )
        # exploded
        return next(prefix_separator_iterator) + next(prefix_separator_iterator).join(
            [var_name_piece + value_pair_equals + val for val in item_values]
        )

    @classmethod
    def __ref6570_dict_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        in_data_transformed = {key: cls.__ref6570_item_value(val, percent_encode) for key, val in in_data.items()}
        in_data_transformed = {key: val for key, val in in_data_transformed.items() if val is not None}
        if not in_data_transformed:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        value_pair_equals = '=' if named_parameter_expansion else ''
        if not explode:
            return (
                next(prefix_separator_iterator) +
                var_name_piece + value_pair_equals +
                prefix_separator_iterator.item_separator.join(
                    prefix_separator_iterator.item_separator.join(
                        item_pair
                    ) for item_pair in in_data_transformed.items()
                )
            )
        # exploded
        return next(prefix_separator_iterator) + next(prefix_separator_iterator).join(
            [key + '=' + val for key, val in in_data_transformed.items()]
        )

    @classmethod
    def _ref6570_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator
    ) -> str:
        """
        Separator is for separate variables like dict with explode true, not for array item separation
        """
        named_parameter_expansion = prefix_separator_iterator.separator in {'&', ';'}
        var_name_piece = variable_name if named_parameter_expansion else ''
        if type(in_data) in {str, float, int}:
            return cls.__ref6570_str_float_int_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, none_type):
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        elif isinstance(in_data, list):
            return cls.__ref6570_list_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, dict):
            return cls.__ref6570_dict_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        # bool, bytes, etc
        raise ApiValueError('Unable to generate a ref6570 representation of {}'.format(in_data))


class StyleFormSerializer(ParameterSerializerBase):
    @classmethod
    def _get_default_explode(cls, style: ParameterStyle) -> bool:
        if style is ParameterStyle.FORM:
            return True
        return super()._get_default_explode(style)

    def _serialize_form(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        name: str,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator] = None
    ) -> str:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = PrefixSeparatorIterator('', '&')
        return self._ref6570_expansion(
            variable_name=name,
            in_data=in_data,
            explode=explode,
            percent_encode=percent_encode,
            prefix_separator_iterator=prefix_separator_iterator
        )


class StyleSimpleSerializer(ParameterSerializerBase):

    def _serialize_simple(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        name: str,
        explode: bool,
        percent_encode: bool
    ) -> str:
        prefix_separator_iterator = PrefixSeparatorIterator('', ',')
        return self._ref6570_expansion(
            variable_name=name,
            in_data=in_data,
            explode=explode,
            percent_encode=percent_encode,
            prefix_separator_iterator=prefix_separator_iterator
        )


class JSONDetector:
    """
    Works for:
    application/json
    application/json; charset=UTF-8
    application/json-patch+json
    application/geo+json
    """
    __json_content_type_pattern = re.compile("application/[^+]*[+]?(json);?.*")

    @classmethod
    def _content_type_is_json(cls, content_type: str) -> bool:
        if cls.__json_content_type_pattern.match(content_type):
            return True
        return False


@dataclass
class ParameterBase(JSONDetector):
    name: str
    in_type: ParameterInType
    required: bool
    style: typing.Optional[ParameterStyle]
    explode: typing.Optional[bool]
    allow_reserved: typing.Optional[bool]
    schema: typing.Optional[typing.Type[Schema]]
    content: typing.Optional[typing.Dict[str, typing.Type[Schema]]]

    __style_to_in_type = {
        ParameterStyle.MATRIX: {ParameterInType.PATH},
        ParameterStyle.LABEL: {ParameterInType.PATH},
        ParameterStyle.FORM: {ParameterInType.QUERY, ParameterInType.COOKIE},
        ParameterStyle.SIMPLE: {ParameterInType.PATH, ParameterInType.HEADER},
        ParameterStyle.SPACE_DELIMITED: {ParameterInType.QUERY},
        ParameterStyle.PIPE_DELIMITED: {ParameterInType.QUERY},
        ParameterStyle.DEEP_OBJECT: {ParameterInType.QUERY},
    }
    __in_type_to_default_style = {
        ParameterInType.QUERY: ParameterStyle.FORM,
        ParameterInType.PATH: ParameterStyle.SIMPLE,
        ParameterInType.HEADER: ParameterStyle.SIMPLE,
        ParameterInType.COOKIE: ParameterStyle.FORM,
    }
    __disallowed_header_names = {'Accept', 'Content-Type', 'Authorization'}
    _json_encoder = JSONEncoder()

    @classmethod
    def __verify_style_to_in_type(cls, style: typing.Optional[ParameterStyle], in_type: ParameterInType):
        if style is None:
            return
        in_type_set = cls.__style_to_in_type[style]
        if in_type not in in_type_set:
            raise ValueError(
                'Invalid style and in_type combination. For style={} only in_type={} are allowed'.format(
                    style, in_type_set
                )
            )

    def __init__(
        self,
        name: str,
        in_type: ParameterInType,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        if schema is None and content is None:
            raise ValueError('Value missing; Pass in either schema or content')
        if schema and content:
            raise ValueError('Too many values provided. Both schema and content were provided. Only one may be input')
        if name in self.__disallowed_header_names and in_type is ParameterInType.HEADER:
            raise ValueError('Invalid name, name may not be one of {}'.format(self.__disallowed_header_names))
        self.__verify_style_to_in_type(style, in_type)
        if content is None and style is None:
            style = self.__in_type_to_default_style[in_type]
        if content is not None and in_type in self.__in_type_to_default_style and len(content) != 1:
            raise ValueError('Invalid content length, content length must equal 1')
        self.in_type = in_type
        self.name = name
        self.required = required
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = content

    def _serialize_json(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        eliminate_whitespace: bool = False
    ) -> str:
        if eliminate_whitespace:
            return json.dumps(in_data, separators=self._json_encoder.compact_separators)
        return json.dumps(in_data)


class PathParameter(ParameterBase, StyleSimpleSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        super().__init__(
            name,
            in_type=ParameterInType.PATH,
            required=required,
            style=style,
            explode=explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def __serialize_label(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list]
    ) -> typing.Dict[str, str]:
        prefix_separator_iterator = PrefixSeparatorIterator('.', '.')
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_matrix(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list]
    ) -> typing.Dict[str, str]:
        prefix_separator_iterator = PrefixSeparatorIterator(';', ';')
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_simple(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
    ) -> typing.Dict[str, str]:
        value = self._serialize_simple(
            in_data=in_data,
            name=self.name,
            explode=self.explode,
            percent_encode=True
        )
        return self._to_dict(self.name, value)

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            simple -> path
                path:
                    returns path_params: dict
            label -> path
                returns path_params
            matrix -> path
                returns path_params
            """
            if self.style:
                if self.style is ParameterStyle.SIMPLE:
                    return self.__serialize_simple(cast_in_data)
                elif self.style is ParameterStyle.LABEL:
                    return self.__serialize_label(cast_in_data)
                elif self.style is ParameterStyle.MATRIX:
                    return self.__serialize_matrix(cast_in_data)
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self._to_dict(self.name, value)
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class QueryParameter(ParameterBase, StyleFormSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: typing.Optional[bool] = None,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        used_style = ParameterStyle.FORM if style is None else style
        used_explode = self._get_default_explode(used_style) if explode is None else explode

        super().__init__(
            name,
            in_type=ParameterInType.QUERY,
            required=required,
            style=used_style,
            explode=used_explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def __serialize_space_delimited(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_pipe_delimited(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_form(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._serialize_form(
            in_data,
            name=self.name,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def get_prefix_separator_iterator(self) -> typing.Optional[PrefixSeparatorIterator]:
        if self.style is ParameterStyle.FORM:
            return PrefixSeparatorIterator('?', '&')
        elif self.style is ParameterStyle.SPACE_DELIMITED:
            return PrefixSeparatorIterator('', '%20')
        elif self.style is ParameterStyle.PIPE_DELIMITED:
            return PrefixSeparatorIterator('', '|')

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator] = None
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            form -> query
                query:
                    - GET/HEAD/DELETE: could use fields
                    - PUT/POST: must use urlencode to send parameters
                    returns fields: tuple
            spaceDelimited -> query
                returns fields
            pipeDelimited -> query
                returns fields
            deepObject -> query, https://github.com/OAI/OpenAPI-Specification/issues/1706
                returns fields
            """
            if self.style:
                # TODO update query ones to omit setting values when [] {} or None is input
                if self.style is ParameterStyle.FORM:
                    return self.__serialize_form(cast_in_data, prefix_separator_iterator)
                elif self.style is ParameterStyle.SPACE_DELIMITED:
                    return self.__serialize_space_delimited(cast_in_data, prefix_separator_iterator)
                elif self.style is ParameterStyle.PIPE_DELIMITED:
                    return self.__serialize_pipe_delimited(cast_in_data, prefix_separator_iterator)
        # self.content will be length one
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data, eliminate_whitespace=True)
                return self._to_dict(
                    self.name,
                    next(prefix_separator_iterator) + self.name + '=' + quote(value)
                )
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class CookieParameter(ParameterBase, StyleFormSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: typing.Optional[bool] = None,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        used_style = ParameterStyle.FORM if style is None and content is None and schema else style
        used_explode = self._get_default_explode(used_style) if explode is None else explode

        super().__init__(
            name,
            in_type=ParameterInType.COOKIE,
            required=required,
            style=used_style,
            explode=used_explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            form -> cookie
                returns fields: tuple
            """
            if self.style:
                """
                TODO add escaping of comma, space, equals
                or turn encoding on
                """
                value = self._serialize_form(
                    cast_in_data,
                    explode=self.explode,
                    name=self.name,
                    percent_encode=False,
                    prefix_separator_iterator=PrefixSeparatorIterator('', '&')
                )
                return self._to_dict(self.name, value)
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self._to_dict(self.name, value)
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class HeaderParameter(ParameterBase, StyleSimpleSerializer):
    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        super().__init__(
            name,
            in_type=ParameterInType.HEADER,
            required=required,
            style=style,
            explode=explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    @staticmethod
    def __to_headers(in_data: typing.Tuple[typing.Tuple[str, str], ...]) -> HTTPHeaderDict:
        data = tuple(t for t in in_data if t)
        headers = HTTPHeaderDict()
        if not data:
            return headers
        headers.extend(data)
        return headers

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> HTTPHeaderDict:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            simple -> header
                headers: PoolManager needs a mapping, tuple is close
                    returns headers: dict
            """
            if self.style:
                value = self._serialize_simple(cast_in_data, self.name, self.explode, False)
                return self.__to_headers(((self.name, value),))
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self.__to_headers(((self.name, value),))
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class Encoding:
    def __init__(
        self,
        content_type: str,
        headers: typing.Optional[typing.Dict[str, HeaderParameter]] = None,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: bool = False,
    ):
        self.content_type = content_type
        self.headers = headers
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved


@dataclass
class MediaType:
    """
    Used to store request and response body schema information
    encoding:
        A map between a property name and its encoding information.
        The key, being the property name, MUST exist in the schema as a property.
        The encoding object SHALL only apply to requestBody objects when the media type is
        multipart or application/x-www-form-urlencoded.
    """
    schema: typing.Optional[typing.Type[Schema]] = None
    encoding: typing.Optional[typing.Dict[str, Encoding]] = None


@dataclass
class ApiResponse:
    response: urllib3.HTTPResponse
    body: typing.Union[Unset, Schema] = unset
    headers: typing.Union[Unset, typing.Dict[str, Schema]] = unset

    def __init__(
        self,
        response: urllib3.HTTPResponse,
        body: typing.Union[Unset, Schema] = unset,
        headers: typing.Union[Unset, typing.Dict[str, Schema]] = unset
    ):
        """
        pycharm needs this to prevent 'Unexpected argument' warnings
        """
        self.response = response
        self.body = body
        self.headers = headers


@dataclass
class ApiResponseWithoutDeserialization(ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[Unset, typing.Type[Schema]] = unset
    headers: typing.Union[Unset, typing.List[HeaderParameter]] = unset


class OpenApiResponse(JSONDetector):
    __filename_content_disposition_pattern = re.compile('filename="(.+?)"')

    def __init__(
        self,
        response_cls: typing.Type[ApiResponse] = ApiResponse,
        content: typing.Optional[typing.Dict[str, MediaType]] = None,
        headers: typing.Optional[typing.List[HeaderParameter]] = None,
    ):
        self.headers = headers
        if content is not None and len(content) == 0:
            raise ValueError('Invalid value for content, the content dict must have >= 1 entry')
        self.content = content
        self.response_cls = response_cls

    @staticmethod
    def __deserialize_json(response: urllib3.HTTPResponse) -> typing.Any:
        # python must be >= 3.9 so we can pass in bytes into json.loads
        return json.loads(response.data)

    @staticmethod
    def __file_name_from_response_url(response_url: typing.Optional[str]) -> typing.Optional[str]:
        if response_url is None:
            return None
        url_path = urlparse(response_url).path
        if url_path:
            path_basename = os.path.basename(url_path)
            if path_basename:
                _filename, ext = os.path.splitext(path_basename)
                if ext:
                    return path_basename
        return None

    @classmethod
    def __file_name_from_content_disposition(cls, content_disposition: typing.Optional[str]) -> typing.Optional[str]:
        if content_disposition is None:
            return None
        match = cls.__filename_content_disposition_pattern.search(content_disposition)
        if not match:
            return None
        return match.group(1)

    def __deserialize_application_octet_stream(
        self, response: urllib3.HTTPResponse
    ) -> typing.Union[bytes, io.BufferedReader]:
        """
        urllib3 use cases:
        1. when preload_content=True (stream=False) then supports_chunked_reads is False and bytes are returned
        2. when preload_content=False (stream=True) then supports_chunked_reads is True and
            a file will be written and returned
        """
        if response.supports_chunked_reads():
            file_name = (
                self.__file_name_from_content_disposition(response.headers.get('content-disposition'))
                or self.__file_name_from_response_url(response.geturl())
            )

            if file_name is None:
                _fd, path = tempfile.mkstemp()
            else:
                path = os.path.join(tempfile.gettempdir(), file_name)

            with open(path, 'wb') as new_file:
                chunk_size = 1024
                while True:
                    data = response.read(chunk_size)
                    if not data:
                        break
                    new_file.write(data)
            # release_conn is needed for streaming connections only
            response.release_conn()
            new_file = open(path, 'rb')
            return new_file
        else:
            return response.data

    @staticmethod
    def __deserialize_multipart_form_data(
        response: urllib3.HTTPResponse
    ) -> typing.Dict[str, typing.Any]:
        msg = email.message_from_bytes(response.data)
        return {
            part.get_param("name", header="Content-Disposition"): part.get_payload(
                decode=True
            ).decode(part.get_content_charset())
            if part.get_content_charset()
            else part.get_payload()
            for part in msg.get_payload()
        }

    def deserialize(self, response: urllib3.HTTPResponse, configuration: Configuration) -> ApiResponse:
        content_type = response.getheader('content-type')
        deserialized_body = unset
        streamed = response.supports_chunked_reads()

        deserialized_headers = unset
        if self.headers is not None:
            # TODO add header deserialiation here
            pass

        if self.content is not None:
            if content_type not in self.content:
                raise ApiValueError(
                    f"Invalid content_type returned. Content_type='{content_type}' was returned "
                    f"when only {str(set(self.content))} are defined for status_code={str(response.status)}"
                )
            body_schema = self.content[content_type].schema
            if body_schema is None:
                # some specs do not define response content media type schemas
                return self.response_cls(
                    response=response,
                    headers=deserialized_headers,
                    body=unset
                )

            if self._content_type_is_json(content_type):
                body_data = self.__deserialize_json(response)
            elif content_type == 'application/octet-stream':
                body_data = self.__deserialize_application_octet_stream(response)
            elif content_type.startswith('multipart/form-data'):
                body_data = self.__deserialize_multipart_form_data(response)
                content_type = 'multipart/form-data'
            else:
                raise NotImplementedError('Deserialization of {} has not yet been implemented'.format(content_type))
            deserialized_body = body_schema.from_openapi_data_oapg(
                body_data, _configuration=configuration)
        elif streamed:
            response.release_conn()

        return self.response_cls(
            response=response,
            headers=deserialized_headers,
            body=deserialized_body
        )


class ApiClient:
    """Generic API client for OpenAPI client library builds.

    OpenAPI generic API client. This client handles the client-
    server communication, and is invariant across implementations. Specifics of
    the methods and models for each application are generated from the OpenAPI
    templates.

    NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech
    Do not edit the class manually.

    :param configuration: .Configuration object for this client
    :param header_name: a header to pass when making calls to the API.
    :param header_value: a header value to pass when making calls to
        the API.
    :param cookie: a cookie to include in the header when making calls
        to the API
    :param pool_threads: The number of threads to use for async requests
        to the API. More threads means more concurrent API requests.
    """

    _pool = None

    def __init__(
        self,
        configuration: typing.Optional[Configuration] = None,
        header_name: typing.Optional[str] = None,
        header_value: typing.Optional[str] = None,
        cookie: typing.Optional[str] = None,
        pool_threads: int = 1
    ):
        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration
        self.pool_threads = pool_threads

        self.rest_client = rest.RESTClientObject(configuration)
        self.default_headers = HTTPHeaderDict()
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        # Set default User-Agent.
        self.user_agent = 'OpenAPI-Generator/1.0.0/python'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._pool:
            self._pool.close()
            self._pool.join()
            self._pool = None
            if hasattr(atexit, 'unregister'):
                atexit.unregister(self.close)

    @property
    def pool(self):
        """Create thread pool on first request
         avoids instantiating unused threadpool for blocking clients.
        """
        if self._pool is None:
            atexit.register(self.close)
            self._pool = ThreadPool(self.pool_threads)
        return self._pool

    @property
    def user_agent(self):
        """User agent for this API client"""
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        self.default_headers[header_name] = header_value

    def __call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
    ) -> urllib3.HTTPResponse:

        # header parameters
        used_headers = HTTPHeaderDict(self.default_headers)
        if self.cookie:
            headers['Cookie'] = self.cookie

        # auth setting
        self.update_params_for_auth(used_headers,
                                    auth_settings, resource_path, method, body)

        # must happen after cookie setting and auth setting in case user is overriding those
        if headers:
            used_headers.update(headers)

        # request url
        if host is None:
            url = self.configuration.host + resource_path
        else:
            # use server/host defined in path or operation instead
            url = host + resource_path

        # perform request and return response
        response = self.request(
            method,
            url,
            headers=used_headers,
            fields=fields,
            body=body,
            stream=stream,
            timeout=timeout,
        )
        return response

    def call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        async_req: typing.Optional[bool] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
    ) -> urllib3.HTTPResponse:
        """Makes the HTTP request (synchronous) and returns deserialized data.

        To make an async_req request, set the async_req parameter.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param headers: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param fields: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings: Auth Settings names for the request.
        :param async_req: execute request asynchronously
        :type async_req: bool, optional TODO remove, unused
        :param stream: if True, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Also when True, if the openapi spec describes a file download,
                                 the data will be written to a local filesystme file and the BinarySchema
                                 instance will also inherit from FileSchema and FileIO
                                 Default is False.
        :type stream: bool, optional
        :param timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param host: api endpoint host
        :return:
            If async_req parameter is True,
            the request will be called asynchronously.
            The method will return the request thread.
            If parameter async_req is False or missing,
            then the method will return the response directly.
        """

        if not async_req:
            return self.__call_api(
                resource_path,
                method,
                headers,
                body,
                fields,
                auth_settings,
                stream,
                timeout,
                host,
            )

        return self.pool.apply_async(
            self.__call_api,
            (
                resource_path,
                method,
                headers,
                body,
                json,
                fields,
                auth_settings,
                stream,
                timeout,
                host,
            )
        )

    def request(
        self,
        method: str,
        url: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> urllib3.HTTPResponse:
        """Makes the HTTP request using RESTClient."""
        if method == "GET":
            return self.rest_client.GET(url,
                                        stream=stream,
                                        timeout=timeout,
                                        headers=headers)
        elif method == "HEAD":
            return self.rest_client.HEAD(url,
                                         stream=stream,
                                         timeout=timeout,
                                         headers=headers)
        elif method == "OPTIONS":
            return self.rest_client.OPTIONS(url,
                                            headers=headers,
                                            fields=fields,
                                            stream=stream,
                                            timeout=timeout,
                                            body=body)
        elif method == "POST":
            return self.rest_client.POST(url,
                                         headers=headers,
                                         fields=fields,
                                         stream=stream,
                                         timeout=timeout,
                                         body=body)
        elif method == "PUT":
            return self.rest_client.PUT(url,
                                        headers=headers,
                                        fields=fields,
                                        stream=stream,
                                        timeout=timeout,
                                        body=body)
        elif method == "PATCH":
            return self.rest_client.PATCH(url,
                                          headers=headers,
                                          fields=fields,
                                          stream=stream,
                                          timeout=timeout,
                                          body=body)
        elif method == "DELETE":
            return self.rest_client.DELETE(url,
                                           headers=headers,
                                           stream=stream,
                                           timeout=timeout,
                                           body=body)
        else:
            raise ApiValueError(
                "http method must be `GET`, `HEAD`, `OPTIONS`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )

    def update_params_for_auth(self, headers, auth_settings,
                               resource_path, method, body):
        """Updates header and query params based on authentication setting.

        :param headers: Header parameters dict to be updated.
        :param auth_settings: Authentication setting identifiers list.
        :param resource_path: A string representation of the HTTP request resource path.
        :param method: A string representation of the HTTP request method.
        :param body: A object representing the body of the HTTP request.
            The object type is the return value of _encoder.default().
        """
        if not auth_settings:
            return

        for auth in auth_settings:
            auth_setting = self.configuration.auth_settings().get(auth)
            if not auth_setting:
                continue
            if auth_setting['in'] == 'cookie':
                headers.add('Cookie', auth_setting['value'])
            elif auth_setting['in'] == 'header':
                if auth_setting['type'] != 'http-signature':
                    headers.add(auth_setting['key'], auth_setting['value'])
            elif auth_setting['in'] == 'query':
                """ TODO implement auth in query
                need to pass in prefix_separator_iterator
                and need to output resource_path with query params added
                """
                raise ApiValueError("Auth in query not yet implemented")
            else:
                raise ApiValueError(
                    'Authentication token must be in `query` or `header`'
                )


class Api:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client: typing.Optional[ApiClient] = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    @staticmethod
    def _verify_typed_dict_inputs_oapg(cls: typing.Type[typing_extensions.TypedDict], data: typing.Dict[str, typing.Any]):
        """
        Ensures that:
        - required keys are present
        - additional properties are not input
        - value stored under required keys do not have the value unset
        Note: detailed value checking is done in schema classes
        """
        missing_required_keys = []
        required_keys_with_unset_values = []
        for required_key in cls.__required_keys__:
            if required_key not in data:
                missing_required_keys.append(required_key)
                continue
            value = data[required_key]
            if value is unset:
                required_keys_with_unset_values.append(required_key)
        if missing_required_keys:
            raise ApiTypeError(
                '{} missing {} required arguments: {}'.format(
                    cls.__name__, len(missing_required_keys), missing_required_keys
                 )
             )
        if required_keys_with_unset_values:
            raise ApiValueError(
                '{} contains invalid unset values for {} required keys: {}'.format(
                    cls.__name__, len(required_keys_with_unset_values), required_keys_with_unset_values
                )
            )

        disallowed_additional_keys = []
        for key in data:
            if key in cls.__required_keys__ or key in cls.__optional_keys__:
                continue
            disallowed_additional_keys.append(key)
        if disallowed_additional_keys:
            raise ApiTypeError(
                '{} got {} unexpected keyword arguments: {}'.format(
                    cls.__name__, len(disallowed_additional_keys), disallowed_additional_keys
                )
            )

    def _get_host_oapg(
        self,
        operation_id: str,
        servers: typing.Tuple[typing.Dict[str, str], ...] = tuple(),
        host_index: typing.Optional[int] = None
    ) -> typing.Optional[str]:
        configuration = self.api_client.configuration
        try:
            if host_index is None:
                index = configuration.server_operation_index.get(
                    operation_id, configuration.server_index
                )
            else:
                index = host_index
            server_variables = configuration.server_operation_variables.get(
                operation_id, configuration.server_variables
            )
            host = configuration.get_host_from_settings(
                index, variables=server_variables, servers=servers
            )
        except IndexError:
            if servers:
                raise ApiValueError(
                    "Invalid host index. Must be 0 <= index < %s" %
                    len(servers)
                )
            host = None
        return host


class SerializedRequestBody(typing_extensions.TypedDict, total=False):
    body: typing.Union[str, bytes]
    fields: typing.Tuple[typing.Union[RequestField, typing.Tuple[str, str]], ...]


class RequestBody(StyleFormSerializer, JSONDetector):
    """
    A request body parameter
    content: content_type to MediaType Schema info
    """
    __json_encoder = JSONEncoder()

    def __init__(
        self,
        content: typing.Dict[str, MediaType],
        required: bool = False,
    ):
        self.required = required
        if len(content) == 0:
            raise ValueError('Invalid value for content, the content dict must have >= 1 entry')
        self.content = content

    def __serialize_json(
        self,
        in_data: typing.Any
    ) -> typing.Dict[str, bytes]:
        in_data = self.__json_encoder.default(in_data)
        json_str = json.dumps(in_data, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        return dict(body=json_str)

    @staticmethod
    def __serialize_text_plain(in_data: typing.Any) -> typing.Dict[str, str]:
        if isinstance(in_data, frozendict.frozendict):
            raise ValueError('Unable to serialize type frozendict.frozendict to text/plain')
        elif isinstance(in_data, tuple):
            raise ValueError('Unable to serialize type tuple to text/plain')
        elif isinstance(in_data, NoneClass):
            raise ValueError('Unable to serialize type NoneClass to text/plain')
        elif isinstance(in_data, BoolClass):
            raise ValueError('Unable to serialize type BoolClass to text/plain')
        return dict(body=str(in_data))

    def __multipart_json_item(self, key: str, value: Schema) -> RequestField:
        json_value = self.__json_encoder.default(value)
        request_field = RequestField(name=key, data=json.dumps(json_value))
        request_field.make_multipart(content_type='application/json')
        return request_field

    def __multipart_form_item(self, key: str, value: Schema) -> RequestField:
        if isinstance(value, str):
            request_field = RequestField(name=key, data=str(value))
            request_field.make_multipart(content_type='text/plain')
        elif isinstance(value, bytes):
            request_field = RequestField(name=key, data=value)
            request_field.make_multipart(content_type='application/octet-stream')
        elif isinstance(value, FileIO):
            # TODO use content.encoding to limit allowed content types if they are present
            request_field = RequestField.from_tuples(key, (os.path.basename(value.name), value.read()))
            value.close()
        else:
            request_field = self.__multipart_json_item(key=key, value=value)
        return request_field

    def __serialize_multipart_form_data(
        self, in_data: Schema
    ) -> typing.Dict[str, typing.Tuple[RequestField, ...]]:
        if not isinstance(in_data, frozendict.frozendict):
            raise ValueError(f'Unable to serialize {in_data} to multipart/form-data because it is not a dict of data')
        """
        In a multipart/form-data request body, each schema property, or each element of a schema array property,
        takes a section in the payload with an internal header as defined by RFC7578. The serialization strategy
        for each property of a multipart/form-data request body can be specified in an associated Encoding Object.

        When passing in multipart types, boundaries MAY be used to separate sections of the content being
        transferred – thus, the following default Content-Types are defined for multipart:

        If the (object) property is a primitive, or an array of primitive values, the default Content-Type is text/plain
        If the property is complex, or an array of complex values, the default Content-Type is application/json
            Question: how is the array of primitives encoded?
        If the property is a type: string with a contentEncoding, the default Content-Type is application/octet-stream
        """
        fields = []
        for key, value in in_data.items():
            if isinstance(value, tuple):
                if value:
                    # values use explode = True, so the code makes a RequestField for each item with name=key
                    for item in value:
                        request_field = self.__multipart_form_item(key=key, value=item)
                        fields.append(request_field)
                else:
                    # send an empty array as json because exploding will not send it
                    request_field = self.__multipart_json_item(key=key, value=value)
                    fields.append(request_field)
            else:
                request_field = self.__multipart_form_item(key=key, value=value)
                fields.append(request_field)

        return dict(fields=tuple(fields))

    def __serialize_application_octet_stream(self, in_data: BinarySchema) -> typing.Dict[str, bytes]:
        if isinstance(in_data, bytes):
            return dict(body=in_data)
        # FileIO type
        result = dict(body=in_data.read())
        in_data.close()
        return result

    def __serialize_application_x_www_form_data(
        self, in_data: typing.Any
    ) -> SerializedRequestBody:
        """
        POST submission of form data in body
        """
        if not isinstance(in_data, frozendict.frozendict):
            raise ValueError(
                f'Unable to serialize {in_data} to application/x-www-form-urlencoded because it is not a dict of data')
        cast_in_data = self.__json_encoder.default(in_data)
        value = self._serialize_form(cast_in_data, name='', explode=True, percent_encode=True)
        return dict(body=value)

    def serialize(
        self, in_data: typing.Any, content_type: str
    ) -> SerializedRequestBody:
        """
        If a str is returned then the result will be assigned to data when making the request
        If a tuple is returned then the result will be used as fields input in encode_multipart_formdata
        Return a tuple of

        The key of the return dict is
        - body for application/json
        - encode_multipart and fields for multipart/form-data
        """
        media_type = self.content[content_type]
        if isinstance(in_data, media_type.schema):
            cast_in_data = in_data
        elif isinstance(in_data, (dict, frozendict.frozendict)) and in_data:
            cast_in_data = media_type.schema(**in_data)
        else:
            cast_in_data = media_type.schema(in_data)
        # TODO check for and use encoding if it exists
        # and content_type is multipart or application/x-www-form-urlencoded
        if self._content_type_is_json(content_type):
            return self.__serialize_json(cast_in_data)
        elif content_type == 'text/plain':
            return self.__serialize_text_plain(cast_in_data)
        elif content_type == 'multipart/form-data':
            return self.__serialize_multipart_form_data(cast_in_data)
        elif content_type == 'application/x-www-form-urlencoded':
            return self.__serialize_application_x_www_form_data(cast_in_data)
        elif content_type == 'application/octet-stream':
            return self.__serialize_application_octet_stream(cast_in_data)
        raise NotImplementedError('Serialization has not yet been implemented for {}'.format(content_type))