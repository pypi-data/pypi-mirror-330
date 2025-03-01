# square_authentication_helper

## about

helper to access the authentication layer for my personal server.

## installation

```shell
pip install square_authentication_helper
```

## usage

[reference python file](./example.py)

## env

- python>=3.12.0

## changelog

### v2.3.0

- add logout_apps_v0 and logout_all_v0.

### v2.2.0

- add validate_and_get_payload_from_token_v0.

### v2.1.0

- login_username_v0 now uses post method and has new optional flag assign_app_id_if_missing that defaults to false.
- use make_request_json_output to call api endpoints.

### v2.0.0

- add functions for
    - update_username_v0
    - update_password_v0
    - delete_user_v0
- move data in password related endpoints to request body from params.
- new optional param, app_id in register_username_v0.
- generate_access_token_v0 now only needs refresh token.
- logout_v0 now only needs refresh token.
- update_user_app_ids_v0 now only updates ids for self (user). added access token as input param and removed user_id.
- get_user_app_ids_v0 is now get_user_details_v0 with access token as the only input param.

### v1.0.0

- initial implementation.

## Feedback is appreciated. Thank you!
