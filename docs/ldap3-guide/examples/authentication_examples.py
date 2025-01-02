"""
LDAP3 Authentication Examples

This example demonstrates various authentication methods and scenarios using the ldap3 package.
It includes examples of different authentication mechanisms, SSL/TLS configuration,
and connection pooling.
"""

from ldap3 import Server, Connection, ALL, SASL, NTLM, Tls, SUBTREE
from ldap3 import SIMPLE, SYNC, ASYNC, REUSABLE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from ldap3.utils.log import set_library_log_detail_level, EXTENDED
import ssl
import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LDAPAuthenticator:
    def __init__(self, host: str, base_dn: str, use_ssl: bool = False,
                 ca_certs_file: Optional[str] = None):
        """Initialize LDAP authenticator.

        Args:
            host: LDAP server hostname/IP
            base_dn: Base DN for LDAP operations
            use_ssl: Whether to use SSL/TLS
            ca_certs_file: Path to CA certificates file for SSL/TLS
        """
        self.host = host
        self.base_dn = base_dn
        
        # Configure TLS if needed
        if use_ssl:
            self.tls = Tls(
                validate=ssl.CERT_REQUIRED if ca_certs_file else ssl.CERT_NONE,
                ca_certs_file=ca_certs_file,
                version=ssl.PROTOCOL_TLSv1_2
            )
        else:
            self.tls = None
            
        # Create server instance
        self.server = Server(
            host,
            use_ssl=use_ssl,
            tls=self.tls,
            get_info=ALL
        )

    def simple_bind(self, user_dn: str, password: str) -> bool:
        """Perform simple bind authentication.

        Args:
            user_dn: User's distinguished name
            password: User's password

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            with Connection(
                self.server,
                user=user_dn,
                password=password,
                authentication=SIMPLE,
                read_only=True
            ) as conn:
                return conn.bind()
        except LDAPBindError as e:
            logger.error(f"Bind failed: {e}")
            return False
        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

    def sasl_digest_md5(self, username: str, password: str,
                       realm: str, authorization_id: str = '') -> bool:
        """Perform SASL DIGEST-MD5 authentication.

        Args:
            username: Username
            password: Password
            realm: SASL realm
            authorization_id: Optional authorization ID

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            with Connection(
                self.server,
                authentication=SASL,
                sasl_mechanism='DIGEST-MD5',
                sasl_credentials=(username, password, realm, authorization_id)
            ) as conn:
                return conn.bind()
        except LDAPException as e:
            logger.error(f"SASL DIGEST-MD5 authentication failed: {e}")
            return False

    def ntlm_authenticate(self, domain: str, username: str, password: str) -> bool:
        """Perform NTLM authentication.

        Args:
            domain: Windows domain
            username: Username
            password: Password

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            with Connection(
                self.server,
                user=f"{domain}\\{username}",
                password=password,
                authentication=NTLM
            ) as conn:
                return conn.bind()
        except LDAPException as e:
            logger.error(f"NTLM authentication failed: {e}")
            return False

    def authenticate_with_starttls(self, user_dn: str, password: str) -> bool:
        """Authenticate using StartTLS.

        Args:
            user_dn: User's distinguished name
            password: Password

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            conn = Connection(
                self.server,
                user=user_dn,
                password=password
            )
            
            if conn.start_tls():
                return conn.bind()
            return False
        except LDAPException as e:
            logger.error(f"StartTLS authentication failed: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.unbind()

    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials by searching for user and binding.

        Args:
            username: Username to validate
            password: Password to validate

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        # First bind as admin to search for user
        try:
            with Connection(
                self.server,
                authentication=SIMPLE,
                read_only=True
            ) as conn:
                # Search for user
                conn.search(
                    self.base_dn,
                    f'(&(objectClass=person)(uid={username}))',
                    attributes=['dn']
                )
                
                if not conn.entries:
                    logger.error(f"User not found: {username}")
                    return False
                
                user_dn = conn.entries[0].entry_dn
                
                # Try binding with user credentials
                return self.simple_bind(user_dn, password)
        except LDAPException as e:
            logger.error(f"Credential validation failed: {e}")
            return False

    def check_group_membership(self, username: str, group_dn: str) -> bool:
        """Check if user is member of specified group.

        Args:
            username: Username to check
            group_dn: Group DN to check membership

        Returns:
            bool: True if user is member of group, False otherwise
        """
        try:
            with Connection(
                self.server,
                authentication=SIMPLE,
                read_only=True
            ) as conn:
                # Search for user's groups
                conn.search(
                    self.base_dn,
                    f'(&(objectClass=person)(uid={username})(memberOf={group_dn}))',
                    attributes=['dn']
                )
                
                return len(conn.entries) > 0
        except LDAPException as e:
            logger.error(f"Group membership check failed: {e}")
            return False

def main():
    """Example usage of LDAPAuthenticator."""
    # Enable detailed logging
    set_library_log_detail_level(EXTENDED)

    # Connection parameters
    LDAP_HOST = 'ldap://localhost:389'
    BASE_DN = 'dc=example,dc=com'
    CA_CERT_FILE = '/path/to/ca_cert.pem'  # Optional

    # Initialize authenticator
    auth = LDAPAuthenticator(
        LDAP_HOST,
        BASE_DN,
        use_ssl=True,
        ca_certs_file=CA_CERT_FILE
    )

    # Example 1: Simple bind
    user_dn = 'cn=john,ou=users,dc=example,dc=com'
    if auth.simple_bind(user_dn, 'password123'):
        print("Simple bind successful")

    # Example 2: SASL DIGEST-MD5
    if auth.sasl_digest_md5('john', 'password123', 'example.com'):
        print("SASL DIGEST-MD5 authentication successful")

    # Example 3: NTLM
    if auth.ntlm_authenticate('EXAMPLE', 'john', 'password123'):
        print("NTLM authentication successful")

    # Example 4: StartTLS
    if auth.authenticate_with_starttls(user_dn, 'password123'):
        print("StartTLS authentication successful")

    # Example 5: Validate credentials
    if auth.validate_credentials('john', 'password123'):
        print("Credentials validated successfully")

    # Example 6: Check group membership
    group_dn = 'cn=developers,ou=groups,dc=example,dc=com'
    if auth.check_group_membership('john', group_dn):
        print("User is member of developers group")

def test_authentication_scenarios():
    """Test various authentication scenarios."""
    auth = LDAPAuthenticator('ldap://localhost:389', 'dc=example,dc=com')

    # Test cases
    test_cases = [
        {
            'name': 'Valid credentials',
            'username': 'valid_user',
            'password': 'correct_password',
            'expected': True
        },
        {
            'name': 'Invalid password',
            'username': 'valid_user',
            'password': 'wrong_password',
            'expected': False
        },
        {
            'name': 'Non-existent user',
            'username': 'nonexistent_user',
            'password': 'any_password',
            'expected': False
        },
        {
            'name': 'Empty password',
            'username': 'valid_user',
            'password': '',
            'expected': False
        }
    ]

    # Run tests
    for test in test_cases:
        result = auth.validate_credentials(test['username'], test['password'])
        status = 'PASS' if result == test['expected'] else 'FAIL'
        print(f"Test: {test['name']} - {status}")

if __name__ == '__main__':
    main()
    # Uncomment to run test scenarios
    # test_authentication_scenarios()
