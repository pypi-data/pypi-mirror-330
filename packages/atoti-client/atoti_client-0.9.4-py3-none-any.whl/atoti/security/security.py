from __future__ import annotations

from collections.abc import MutableMapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import deprecated

from .._content_client import ContentClient
from .._deprecated_warning_category import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
)
from .._identification import RoleName, UserName
from .._tables_restriction_condition import TablesRestrictionCondition
from .._tables_restrictions import Restrictions
from ._individual_roles import IndividualRoles
from .basic_authentication_security import BasicAuthenticationSecurity
from .kerberos_security import KerberosSecurity
from .ldap_security import LdapSecurity
from .oidc_security import OidcSecurity


@final
class Security:
    """Manage the parts of the security config that can be changed without restarting the :class:`~atoti.Session`.

    Note:
        This feature is not part of the community edition: it needs to be :doc:`unlocked </how_tos/unlock_all_features>`.

    * Users with the :guilabel:`ROLE_ADMIN` are administrators: they have full access to the application.
    * Non-administrator users without the :guilabel:`ROLE_USER` will not be able to access the application.
      See :attr:`individual_roles` for an example.

    """

    def __init__(
        self,
        *,
        basic_credentials: MutableMapping[UserName, str],
        content_client: ContentClient,
    ):
        self._basic_credentials: Final = basic_credentials
        self._content_client: Final = content_client

    @property
    @deprecated(
        "`Session.security.restrictions is deprecated, use `Session.tables.restrictions` instead.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def _restrictions(self) -> MutableMapping[RoleName, TablesRestrictionCondition]:
        return Restrictions(content_client=self._content_client)

    @property
    def individual_roles(self) -> MutableMapping[UserName, AbstractSet[RoleName]]:
        """Mapping from username to roles granted on top of the ones that can be added by authentication providers.

        Example:
            >>> session_config = tt.SessionConfig(security=tt.SecurityConfig())
            >>> session = tt.Session.start(session_config)
            >>> username = "John"
            >>> session.security.basic_authentication.credentials[username] = "X Æ A-12"
            >>> username in session.security.individual_roles
            False
            >>> session.security.individual_roles[username] = {
            ...     "ROLE_USA",
            ...     "ROLE_USER",
            ... }
            >>> sorted(session.security.individual_roles[username])
            ['ROLE_USA', 'ROLE_USER']
            >>> session.security.individual_roles[username] -= {"ROLE_USA"}
            >>> session.security.individual_roles[username]
            frozenset({'ROLE_USER'})
            >>> # Removing all the roles will prevent the user from accessing the application:
            >>> del session.security.individual_roles[username]
            >>> username in session.security.individual_roles
            False

            .. doctest::
                :hide:

                >>> del session

        """
        return IndividualRoles(content_client=self._content_client)

    @property
    @deprecated(
        "`security.basic` is deprecated, use `security.basic_authentication` instead.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def basic(self) -> BasicAuthenticationSecurity:
        """The basic authentication security.

        :meta private:
        """
        return self.basic_authentication

    @property
    def basic_authentication(self) -> BasicAuthenticationSecurity:
        return BasicAuthenticationSecurity(credentials=self._basic_credentials)

    @property
    def kerberos(self) -> KerberosSecurity:
        return KerberosSecurity(content_client=self._content_client)

    @property
    def ldap(self) -> LdapSecurity:
        return LdapSecurity(content_client=self._content_client)

    @property
    def oidc(self) -> OidcSecurity:
        return OidcSecurity(content_client=self._content_client)
