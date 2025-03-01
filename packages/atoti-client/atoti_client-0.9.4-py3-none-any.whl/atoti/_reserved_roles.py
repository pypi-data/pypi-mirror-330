from collections.abc import Collection

from ._identification import RoleName

ROLE_ADMIN: RoleName = "ROLE_ADMIN"
ROLE_USER: RoleName = "ROLE_USER"

_RESERVED_ROLES: Collection[RoleName] = (ROLE_ADMIN, ROLE_USER)


def check_no_reserved_roles(role_names: Collection[RoleName]) -> None:
    for role_name in role_names:
        if role_name in _RESERVED_ROLES:
            raise ValueError(f"Role `{role_name}` is reserved, use another role.")
