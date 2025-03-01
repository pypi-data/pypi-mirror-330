from typing import List, Optional

from square_commons.api_utils import make_request_json_output

from square_authentication_helper.pydantic_models import TokenType


class SquareAuthenticationHelper:
    def __init__(
        self,
        param_int_square_authentication_port: int = 10011,
        param_str_square_authentication_ip: str = "localhost",
        param_str_square_authentication_protocol: str = "http",
    ):
        try:
            self.global_str_square_authentication_url_base = (
                f"{param_str_square_authentication_protocol}://"
                f"{param_str_square_authentication_ip}:{param_int_square_authentication_port}"
            )
        except Exception:
            raise

    def _make_request(self, method, endpoint, data=None, params=None, headers=None):
        try:
            return make_request_json_output(
                method=method,
                base_url=self.global_str_square_authentication_url_base,
                endpoint=endpoint,
                data=data,
                params=params,
                headers=headers,
            )

        except Exception:
            raise

    def register_username_v0(
        self,
        username: str,
        password: str,
        app_id: Optional[int] = None,
    ):
        try:
            endpoint = "register_username/v0"
            data = {
                "username": username,
                "password": password,
                "app_id": app_id,
            }
            return self._make_request(method="POST", endpoint=endpoint, data=data)
        except Exception:
            raise

    def login_username_v0(
        self,
        username: str,
        password: str,
        app_id: int,
        assign_app_id_if_missing: bool = False,
    ):
        try:
            endpoint = "login_username/v0"
            data = {
                "username": username,
                "password": password,
                "app_id": app_id,
                "assign_app_id_if_missing": assign_app_id_if_missing,
            }
            return self._make_request(method="POST", endpoint=endpoint, data=data)
        except Exception:
            raise

    def generate_access_token_v0(
        self,
        refresh_token: str,
    ):
        try:
            endpoint = "generate_access_token/v0"
            headers = {
                "refresh_token": refresh_token,
            }
            return self._make_request(method="GET", endpoint=endpoint, headers=headers)
        except Exception:
            raise

    def logout_v0(
        self,
        refresh_token: str,
    ):
        try:
            endpoint = "logout/v0"
            headers = {
                "refresh_token": refresh_token,
            }
            return self._make_request(
                method="DELETE", endpoint=endpoint, headers=headers
            )
        except Exception:
            raise

    def logout_apps_v0(
        self,
        access_token: str,
        app_ids: List[int],
    ):
        try:
            endpoint = "logout/apps/v0"
            headers = {
                "access_token": access_token,
            }
            body = {
                "app_ids": app_ids,
            }
            return self._make_request(
                method="DELETE", endpoint=endpoint, headers=headers, data=body
            )
        except Exception:
            raise

    def logout_all_v0(
        self,
        access_token: str,
    ):
        try:
            endpoint = "logout/all/v0"
            headers = {
                "access_token": access_token,
            }
            return self._make_request(
                method="DELETE", endpoint=endpoint, headers=headers
            )
        except Exception:
            raise

    def get_user_details_v0(
        self,
        access_token: str,
    ):
        try:
            endpoint = "get_user_details/v0"
            headers = {
                "access_token": access_token,
            }
            return self._make_request(
                method="GET",
                endpoint=endpoint,
                headers=headers,
            )
        except Exception:
            raise

    def update_user_app_ids_v0(
        self,
        access_token: str,
        app_ids_to_add: List[int],
        app_ids_to_remove: List[int],
    ):
        try:
            endpoint = "update_user_app_ids/v0"
            headers = {
                "access_token": access_token,
            }
            payload = {
                "app_ids_to_add": app_ids_to_add,
                "app_ids_to_remove": app_ids_to_remove,
            }
            return self._make_request(
                method="PATCH", endpoint=endpoint, headers=headers, data=payload
            )
        except Exception:
            raise

    def update_username_v0(
        self,
        new_username: str,
        access_token: str,
    ):
        try:
            endpoint = "update_username/v0"
            params = {
                "new_username": new_username,
            }
            headers = {
                "access_token": access_token,
            }
            return self._make_request(
                method="PATCH", endpoint=endpoint, params=params, headers=headers
            )
        except Exception:
            raise

    def delete_user_v0(
        self,
        password: str,
        access_token: str,
    ):
        try:
            endpoint = "delete_user/v0"
            data = {
                "password": password,
            }
            headers = {
                "access_token": access_token,
            }
            return self._make_request(
                method="DELETE", endpoint=endpoint, data=data, headers=headers
            )
        except Exception:
            raise

    def update_password_v0(
        self,
        old_password: str,
        new_password: str,
        access_token: str,
    ):
        try:
            endpoint = "update_password/v0"
            data = {
                "old_password": old_password,
                "new_password": new_password,
            }
            headers = {
                "access_token": access_token,
            }
            return self._make_request(
                method="PATCH", endpoint=endpoint, data=data, headers=headers
            )
        except Exception:
            raise

    def validate_and_get_payload_from_token_v0(self, token: str, token_type: TokenType):
        try:
            endpoint = "validate_and_get_payload_from_token/v0"
            params = {"token_type": token_type.value}
            headers = {
                "token": token,
            }
            return self._make_request(
                method="GET", endpoint=endpoint, headers=headers, params=params
            )
        except Exception:
            raise
