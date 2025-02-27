"""Utilities for describing capabilities.

Each known capability is assigned a base class for request and response.
The actual request and response types in a integration implementation
can either use the base classes directly or create subclasses, however,
those bases are enforced to be used.
"""

import inspect
import typing as t
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError

from connector.generated import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    AppInfoRequest,
    AppInfoResponse,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    AuthCredential,
    BasicCredential,
    CapabilitySchema,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    ErrorCode,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    GetAuthorizationUrlRequest,
    GetAuthorizationUrlResponse,
    GetLastActivityRequest,
    GetLastActivityResponse,
    HandleAuthorizationCallbackRequest,
    HandleAuthorizationCallbackResponse,
    HandleClientCredentialsRequest,
    HandleClientCredentialsResponse,
    JWTCredential,
    ListAccountsRequest,
    ListAccountsResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListExpensesRequest,
    ListExpensesResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    Page,
    RefreshAccessTokenRequest,
    RefreshAccessTokenResponse,
    StandardCapabilityName,
    TokenCredential,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
    UpdateAccountRequest,
    UpdateAccountResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
)
from connector.oai.errors import ConnectorError

BaseModelType = t.TypeVar("BaseModelType", bound=BaseModel)


class Request(t.Protocol):
    """
    A generic request to any capability.

    Useful as a type for calling request helpers on, e.g. get_token_auth, get_settings.

    Will match all AuthenticatedRequest capability inputs.
    """

    auth: t.Any
    """
    The connector.generated.AuthCredential attached to this request.
    """

    credentials: t.Any

    request: t.Any
    """
    The payload of this request. The type depends on the request type.
    """

    page: t.Any
    """
    Page data. May be None
    """

    include_raw_data: bool | None = None

    settings: t.Any
    """
    User-configured settings for the integration.
    """


class AuthRequest(t.Protocol):
    """
    A request being used as part of an authentication flow.

    These requests must have settings, but they don't have credentials.
    """

    request: t.Any
    """
    The payload of this request
    """

    page: t.Any
    """
    Page data. May be None
    """

    include_raw_data: bool | None = None

    settings: t.Any
    """
    User-configured settings for the integration.
    """


CredentialType = t.TypeVar(
    "CredentialType",
    OAuthCredential,
    OAuthClientCredential,
    BasicCredential,
    TokenCredential,
    JWTCredential,
)


def get_credential(
    request: Request, credential_id: str, credential_type: type[CredentialType]
) -> CredentialType:
    """
    Return the particular credential from the request.
    Similarly to get_settings, the credential is identified by the credential_id and the root credentials model.
    eg. OAuthCredential, OAuthClientCredential, BasicCredential, TokenCredential, JWTCredential
    """
    if request.credentials and isinstance(request.credentials, list):
        for credential in request.credentials:
            if credential.id == credential_id:
                # Find the credential from the request
                if credential.oauth and isinstance(credential.oauth, credential_type):
                    return credential.oauth
                elif credential.oauth_client_credentials and isinstance(
                    credential.oauth_client_credentials, credential_type
                ):
                    return credential.oauth_client_credentials
                elif credential.basic and isinstance(credential.basic, credential_type):
                    return credential.basic
                elif credential.token and isinstance(credential.token, credential_type):
                    return credential.token
                elif credential.jwt and isinstance(credential.jwt, credential_type):
                    return credential.jwt

                raise ConnectorError(
                    message=f"Credential '{credential_id}' found but is not of type {credential_type}.",
                    error_code=ErrorCode.BAD_REQUEST,
                )

    raise ConnectorError(
        message=f"Credential '{credential_id}' not provided in credentials.",
        error_code=ErrorCode.BAD_REQUEST,
    )


def get_oauth(request: Request) -> OAuthCredential | OAuthClientCredential:
    """
    Either get the (valid) request.auth as an OAuth credential, or throw an error.
    """
    if request.auth and request.auth.oauth and isinstance(request.auth.oauth, OAuthCredential):
        return request.auth.oauth
    if (
        request.auth
        and request.auth.oauth_client_credentials
        and isinstance(request.auth.oauth_client_credentials, OAuthClientCredential)
    ):
        return request.auth.oauth_client_credentials

    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_oauth_1(request: Request) -> OAuth1Credential:
    """
    Either get the (valid) request.auth as an OAuth1 credential, or throw an error.
    """
    if request.auth and request.auth.oauth1 and isinstance(request.auth.oauth1, OAuth1Credential):
        return request.auth.oauth1
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_basic_auth(request: Request) -> BasicCredential:
    """
    Either get the (valid) request.auth as a basic credential, or throw an error.
    """
    if request.auth and request.auth.basic and isinstance(request.auth.basic, BasicCredential):
        return request.auth.basic
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_token_auth(request: Request) -> TokenCredential:
    """
    Either get the (valid) request.auth as a token credential, or throw an error.
    """
    if request.auth and request.auth.token and isinstance(request.auth.token, TokenCredential):
        return request.auth.token
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_jwt_auth(request: Request) -> JWTCredential:
    """
    Either get the (valid) request.auth as a JWT credential, or throw an error.
    """
    if request.auth and request.auth.jwt and isinstance(request.auth.jwt, JWTCredential):
        return request.auth.jwt
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_page(request: Request) -> Page:
    """
    Get request.page or a blank one if it isn't set.
    """
    if request.page:
        return request.page
    return Page()


SettingsType = t.TypeVar("SettingsType", bound=BaseModel)


def get_settings(
    request: Request | AuthRequest | AppInfoRequest, model: type[SettingsType]
) -> SettingsType:
    """
    Get a validated Settings type from request.settings.
    """
    try:
        return model.model_validate(request.settings or {})
    except ValidationError as err:
        raise ConnectorError(
            message="Invalid request settings", error_code=ErrorCode.BAD_REQUEST
        ) from err


def extra_data(extra: dict[str, t.Any]) -> dict[str, str]:
    """
    Generate a str:str dict out of arbitrary data for a response.raw_data.
    """
    ret: dict[str, str] = {}
    for key, value in extra.items():
        if value:
            ret[key] = str(value)
    return ret


T = t.TypeVar("T")


class Response(t.Protocol):
    response: t.Any
    raw_data: t.Any | None


_Request = t.TypeVar("_Request", bound=Request, contravariant=True)


class CapabilityCallableProto(t.Protocol, t.Generic[_Request]):
    def __call__(self, args: _Request) -> Response | t.Awaitable[Response]:
        ...

    __name__: str


class CustomRequest(BaseModel, t.Generic[BaseModelType]):
    """
    Generic Request type, extendable for customized capability inputs.

    Example:

    class MyAppCreateAccount(CreateAccount):
      birthday: str

    def create_account(args: CustomRequest[MyAppCreateAccount]) -> CreateAccountResponse:
       ...
    """

    auth: AuthCredential
    credentials: t.Any = None
    page: Page | None = None
    include_raw_data: bool | None = None
    settings: t.Any

    request: BaseModelType


class CustomResponse(BaseModel, t.Generic[BaseModelType]):
    page: Page | None = None
    raw_data: t.Any | None = None

    response: BaseModelType


class Empty(BaseModel):
    pass


def generate_capability_schema(
    impl: (CapabilityCallableProto[t.Any]),
    capability_description: str | None = None,
    full_schema: bool = False,
) -> CapabilitySchema:
    request_annotation, response_annotation = get_capability_annotations(impl)
    request_type = _request_payload_type(request_annotation)
    response_type = _response_payload_type(response_annotation)

    # Old behavior: use Empty for list types when full_schema is False
    if not full_schema:
        request_type = Empty if _is_list(request_type) else request_type
        response_type = Empty if _is_list(response_type) else response_type
        return CapabilitySchema(
            argument=request_type.model_json_schema(),
            output=response_type.model_json_schema(),
            description=capability_description,
        )

    # Get the full payload type
    request_type = _full_payload_type(request_annotation)
    response_type = _full_payload_type(response_annotation)

    # New behavior: handle full schema generation for both simple and list types
    base_request_type = request_type.__args__[0] if _is_list(request_type) else request_type
    base_response_type = response_type.__args__[0] if _is_list(response_type) else response_type

    base_request_schema = base_request_type.model_json_schema(
        ref_template="#/components/schemas/{model}"
    )
    base_response_schema = base_response_type.model_json_schema(
        ref_template="#/components/schemas/{model}"
    )

    request_schema = (
        {
            "type": "array",
            "items": base_request_schema,
            "title": f"Array of {getattr(base_request_type, '__name__', 'Items')}",
        }
        if _is_list(request_type)
        else base_request_schema
    )

    response_schema = (
        {
            "type": "array",
            "items": base_response_schema,
            "title": f"Array of {getattr(base_response_type, '__name__', 'Items')}",
        }
        if _is_list(response_type)
        else base_response_schema
    )

    return CapabilitySchema(
        argument=request_schema,
        output=response_schema,
        description=capability_description,
    )


def get_capability_annotations(
    impl: CapabilityCallableProto[t.Any],
) -> tuple[t.Any, t.Any]:
    """Extract argument and return type annotations."""
    annotations = inspect.get_annotations(impl)
    try:
        response_annotation = annotations["return"]
        request_annotation_name = (set(annotations.keys()) - {"return"}).pop()
    except KeyError:
        raise TypeError(
            f"The capability function {impl.__name__} must have both request and return annotations."
        ) from None

    request_annotation = annotations[request_annotation_name]

    return request_annotation, response_annotation


def _full_payload_type(model: type[BaseModelType]) -> type[BaseModelType]:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model


def _request_payload_type(model: type[BaseModel]) -> t.Any:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model.model_fields["request"].annotation


def _response_payload_type(model: type[BaseModel]) -> t.Any:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model.model_fields["response"].annotation


def _pluck_generic_parameter(type_annotation: t.Any) -> t.Any:
    if type(type_annotation) in (type(list[t.Any]), type(dict[t.Any, t.Any])):
        value_type = type_annotation.__args__[-1]
        return value_type
    return type_annotation


def _is_list(type_annotation: t.Any) -> bool:
    """This function is compatible with both list and typing.List
    (which is used in the generated models)"""
    if origin := getattr(type_annotation, "__origin__", None):
        return origin is list
    return type_annotation is list


def validate_capability(
    capability_name: StandardCapabilityName,
    impl: (CapabilityCallableProto[t.Any]),
) -> None:
    """Make sure capability implementation is valid.

    Capability is marked as valid when:
        * is fully annotated, i.e., both argument and return value are
        type-hinted
        * type of accepted argument matches the expected one, i.e., is
        exactly the same class or a subclass
        * type of returned value matches the expected one, same
        mechanism as for argument
    """
    actual_request, actual_response = get_capability_annotations(impl)
    config = CAPABILITY_CONFIGS[capability_name]
    if actual_response != config.output.model and not config.output.may_be_customized:
        raise TypeError(
            f"The function {impl.__name__} for capability {capability_name} must return {config.output.model.__name__}. "
            f"Actual response model: {actual_response.__name__}"
        ) from None

    actual_request_model = _pluck_generic_parameter(_request_payload_type(actual_request))
    expected_request_model = _pluck_generic_parameter(_request_payload_type(config.input.model))

    is_same_class = actual_request_model == expected_request_model
    is_subclass = issubclass(actual_request_model, expected_request_model)
    is_subclass_allowed = config.input.may_be_customized
    if not is_same_class and not (is_subclass and is_subclass_allowed):
        raise TypeError(
            f"The function {impl.__name__} for capability {capability_name} must accept {expected_request_model.__name__} "
            f"or its subclass. Actual request model: {actual_request_model.__name__}"
        ) from None


def capability_requires_authentication(capability: CapabilityCallableProto[t.Any]) -> bool:
    """Check if the capability requires authentication on the request."""
    expected_request, _ = get_capability_annotations(capability)

    # TODO: Later on when "auth" is phased out, we can add the .is_required() check back here
    if "auth" in expected_request.model_fields or "credentials" in expected_request.model_fields:
        return True
    return False


@dataclass
class Message:
    model: type[BaseModel]
    may_be_customized: bool = False


@dataclass
class CapabilityConfig:
    input: Message
    output: Message


CAPABILITY_CONFIGS: dict[StandardCapabilityName, CapabilityConfig] = {
    StandardCapabilityName.APP_INFO: CapabilityConfig(
        input=Message(AppInfoRequest),
        output=Message(AppInfoResponse),
    ),
    StandardCapabilityName.GET_AUTHORIZATION_URL: CapabilityConfig(
        input=Message(GetAuthorizationUrlRequest),
        output=Message(GetAuthorizationUrlResponse),
    ),
    StandardCapabilityName.GET_LAST_ACTIVITY: CapabilityConfig(
        input=Message(GetLastActivityRequest),
        output=Message(GetLastActivityResponse),
    ),
    StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK: CapabilityConfig(
        input=Message(HandleAuthorizationCallbackRequest),
        output=Message(HandleAuthorizationCallbackResponse),
    ),
    StandardCapabilityName.HANDLE_CLIENT_CREDENTIALS_REQUEST: CapabilityConfig(
        input=Message(HandleClientCredentialsRequest),
        output=Message(HandleClientCredentialsResponse),
    ),
    StandardCapabilityName.LIST_ACCOUNTS: CapabilityConfig(
        input=Message(ListAccountsRequest),
        output=Message(ListAccountsResponse),
    ),
    StandardCapabilityName.LIST_RESOURCES: CapabilityConfig(
        input=Message(ListResourcesRequest),
        output=Message(ListResourcesResponse),
    ),
    StandardCapabilityName.LIST_ENTITLEMENTS: CapabilityConfig(
        input=Message(ListEntitlementsRequest),
        output=Message(ListEntitlementsResponse),
    ),
    StandardCapabilityName.LIST_EXPENSES: CapabilityConfig(
        input=Message(ListExpensesRequest),
        output=Message(ListExpensesResponse),
    ),
    StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: CapabilityConfig(
        input=Message(FindEntitlementAssociationsRequest),
        output=Message(FindEntitlementAssociationsResponse),
    ),
    StandardCapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA: CapabilityConfig(
        input=Message(ListCustomAttributesSchemaRequest),
        output=Message(ListCustomAttributesSchemaResponse),
    ),
    StandardCapabilityName.REFRESH_ACCESS_TOKEN: CapabilityConfig(
        input=Message(RefreshAccessTokenRequest),
        output=Message(RefreshAccessTokenResponse),
    ),
    StandardCapabilityName.CREATE_ACCOUNT: CapabilityConfig(
        input=Message(CreateAccountRequest),
        output=Message(CreateAccountResponse),
    ),
    StandardCapabilityName.DELETE_ACCOUNT: CapabilityConfig(
        input=Message(DeleteAccountRequest),
        output=Message(DeleteAccountResponse),
    ),
    StandardCapabilityName.ACTIVATE_ACCOUNT: CapabilityConfig(
        input=Message(ActivateAccountRequest),
        output=Message(ActivateAccountResponse),
    ),
    StandardCapabilityName.DEACTIVATE_ACCOUNT: CapabilityConfig(
        input=Message(DeactivateAccountRequest),
        output=Message(DeactivateAccountResponse),
    ),
    StandardCapabilityName.ASSIGN_ENTITLEMENT: CapabilityConfig(
        input=Message(AssignEntitlementRequest),
        output=Message(AssignEntitlementResponse),
    ),
    StandardCapabilityName.UNASSIGN_ENTITLEMENT: CapabilityConfig(
        input=Message(UnassignEntitlementRequest),
        output=Message(UnassignEntitlementResponse),
    ),
    StandardCapabilityName.UPDATE_ACCOUNT: CapabilityConfig(
        input=Message(UpdateAccountRequest, may_be_customized=True),
        output=Message(UpdateAccountResponse, may_be_customized=True),
    ),
    StandardCapabilityName.VALIDATE_CREDENTIALS: CapabilityConfig(
        input=Message(ValidateCredentialsRequest),
        output=Message(ValidateCredentialsResponse),
    ),
}
