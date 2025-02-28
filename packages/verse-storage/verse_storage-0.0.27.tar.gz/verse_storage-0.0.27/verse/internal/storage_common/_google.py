import json


def get_credentials(
    service_account_info,
    service_account_file,
    access_token,
):
    from google.oauth2 import service_account

    if service_account_info is not None:
        service_account_info = (
            json.loads(service_account_info)
            if isinstance(service_account_info, str)
            else service_account_info
        )
        return service_account.Credentials.from_service_account_info(
            service_account_info
        )
    elif service_account_file is not None:
        return service_account.Credentials.from_service_account_file(
            service_account_file
        )
    elif access_token is not None:
        from google.auth.credentials import Credentials

        return Credentials(access_token)
    return None
