from typing import Final, final

from .._content_client import ContentClient
from .default_roles import DefaultRoles


@final
class KerberosSecurity:
    """Manage Kerberos security on the session.

    Note:
        This requires :attr:`atoti.SecurityConfig.sso` to be an instance of :class:`~atoti.KerberosConfig`.

    See Also:
        :attr:`~atoti.security.Security.ldap` for a similar usage example.
    """

    def __init__(self, *, content_client: ContentClient) -> None:
        self._content_client: Final = content_client

    @property
    def default_roles(self) -> DefaultRoles:
        return DefaultRoles(
            authentication_type="KERBEROS", content_client=self._content_client
        )
