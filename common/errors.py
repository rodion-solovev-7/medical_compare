import fastapi_jsonrpc as jsonrpc


class AuthError(jsonrpc.BaseError):
    CODE = 7000
    MESSAGE = 'Auth error'


class AccountNotFound(jsonrpc.BaseError):
    CODE = 6000
    MESSAGE = 'Account not found'
