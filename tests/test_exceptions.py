# tests/test_exceptions.py
"""
Layer 1 — Exception hierarchy tests.
"""
import builtins
import pytest
from cipher_gateway.exceptions import (
    CipherGatewayError,
    NotStartedError,
    AuthenticationError,
    AccountNotFoundError,
    AccountLoginFailedError,
    AccountTimeoutError,
    OrderError,
    GatewayConnectionError,
    SubscriptionError,
    GatewayResponseError,
)


class TestExceptionHierarchy:

    def test_all_inherit_from_base(self):
        for exc_class in [
            NotStartedError,
            AuthenticationError,
            AccountNotFoundError,
            AccountLoginFailedError,
            AccountTimeoutError,
            OrderError,
            GatewayConnectionError,
            SubscriptionError,
            GatewayResponseError,
        ]:
            assert issubclass(exc_class, CipherGatewayError), \
                f"{exc_class.__name__} must inherit from CipherGatewayError"

    def test_base_inherits_from_exception(self):
        assert issubclass(CipherGatewayError, Exception)

    def test_catch_all_works(self):
        for exc_class in [AuthenticationError, AccountLoginFailedError,
                          GatewayConnectionError, OrderError]:
            with pytest.raises(CipherGatewayError):
                raise exc_class("test")

    def test_gateway_connection_error_does_not_shadow_builtin(self):
        # The SDK must NOT export a class named 'ConnectionError'
        # which would shadow builtins.ConnectionError
        assert GatewayConnectionError is not builtins.ConnectionError
        assert GatewayConnectionError.__name__ == 'GatewayConnectionError'

    def test_builtin_connection_error_still_works(self):
        # After importing from SDK, builtins.ConnectionError is intact
        with pytest.raises(builtins.ConnectionError):
            raise builtins.ConnectionError("system network error")


class TestGatewayResponseError:

    def test_message_and_defaults(self):
        e = GatewayResponseError("bad gateway")
        assert str(e) == "bad gateway"
        assert e.status_code == 0
        assert e.raw == ""

    def test_with_status_and_raw(self):
        e = GatewayResponseError("server error", status_code=500, raw="Internal Server Error")
        assert e.status_code == 500
        assert e.raw == "Internal Server Error"

    def test_is_catchable_as_base(self):
        with pytest.raises(CipherGatewayError) as exc_info:
            raise GatewayResponseError("oops", status_code=422)
        assert exc_info.value.status_code == 422
