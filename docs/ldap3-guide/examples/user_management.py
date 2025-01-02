"""
LDAP3 User Management Example

This example demonstrates common user management operations using the ldap3 package.
It includes functions for creating, modifying, and deleting users, as well as
managing group memberships.
"""

from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPException, LDAPOperationResult
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LDAPUserManager:
    def __init__(self, host: str, admin_dn: str, admin_password: str):
        """Initialize LDAP connection with admin credentials.

        Args:
            host: LDAP server hostname/IP
            admin_dn: Admin distinguished name
            admin_password: Admin password
        """
        self.server = Server(host, get_info=ALL)
        self.admin_dn = admin_dn
        self.admin_password = admin_password
        self.base_dn = ','.join(admin_dn.split(',')[1:])  # Extract base DN from admin DN
        
    def __enter__(self):
        """Context manager entry point."""
        self.conn = Connection(
            self.server,
            self.admin_dn,
            self.admin_password,
            auto_bind=True
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.conn.unbind()

    def create_user(self, username: str, attributes: Dict) -> bool:
        """Create a new user entry.

        Args:
            username: User's username
            attributes: Dictionary of user attributes

        Returns:
            bool: True if successful, False otherwise
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        
        # Default object classes for user entries
        object_class = ['top', 'person', 'organizationalPerson', 'inetOrgPerson']
        
        try:
            self.conn.add(user_dn, object_class, attributes)
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully created user: {username}")
                return True
            else:
                logger.error(f"Failed to create user: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error creating user: {e}")
            return False

    def delete_user(self, username: str) -> bool:
        """Delete a user entry.

        Args:
            username: Username to delete

        Returns:
            bool: True if successful, False otherwise
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        
        try:
            self.conn.delete(user_dn)
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully deleted user: {username}")
                return True
            else:
                logger.error(f"Failed to delete user: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error deleting user: {e}")
            return False

    def modify_user(self, username: str, modifications: Dict) -> bool:
        """Modify user attributes.

        Args:
            username: Username to modify
            modifications: Dictionary of modifications

        Returns:
            bool: True if successful, False otherwise
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        
        try:
            self.conn.modify(user_dn, modifications)
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully modified user: {username}")
                return True
            else:
                logger.error(f"Failed to modify user: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error modifying user: {e}")
            return False

    def add_to_group(self, username: str, group: str) -> bool:
        """Add user to a group.

        Args:
            username: Username to add
            group: Group name

        Returns:
            bool: True if successful, False otherwise
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        group_dn = f"cn={group},ou=groups,{self.base_dn}"
        
        try:
            # Add user to group's member attribute
            self.conn.modify(group_dn,
                           {'member': [(MODIFY_ADD, [user_dn])]})
            
            # Add group to user's memberOf attribute
            self.conn.modify(user_dn,
                           {'memberOf': [(MODIFY_ADD, [group_dn])]})
            
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully added {username} to group {group}")
                return True
            else:
                logger.error(f"Failed to add to group: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error adding to group: {e}")
            return False

    def remove_from_group(self, username: str, group: str) -> bool:
        """Remove user from a group.

        Args:
            username: Username to remove
            group: Group name

        Returns:
            bool: True if successful, False otherwise
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        group_dn = f"cn={group},ou=groups,{self.base_dn}"
        
        try:
            # Remove user from group's member attribute
            self.conn.modify(group_dn,
                           {'member': [(MODIFY_DELETE, [user_dn])]})
            
            # Remove group from user's memberOf attribute
            self.conn.modify(user_dn,
                           {'memberOf': [(MODIFY_DELETE, [group_dn])]})
            
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully removed {username} from group {group}")
                return True
            else:
                logger.error(f"Failed to remove from group: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error removing from group: {e}")
            return False

    def get_user_groups(self, username: str) -> List[str]:
        """Get list of groups user belongs to.

        Args:
            username: Username to check

        Returns:
            List[str]: List of group names
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        
        try:
            self.conn.search(user_dn,
                           '(objectClass=*)',
                           attributes=['memberOf'])
            
            if not self.conn.entries:
                logger.error(f"User not found: {username}")
                return []
                
            groups = []
            if 'memberOf' in self.conn.entries[0]:
                for group_dn in self.conn.entries[0].memberOf:
                    groups.append(group_dn.split(',')[0].split('=')[1])
            
            return groups
        except LDAPException as e:
            logger.error(f"Error getting user groups: {e}")
            return []

    def change_password(self, username: str, new_password: str, old_password: Optional[str] = None) -> bool:
        """Change user's password.

        Args:
            username: Username whose password to change
            new_password: New password
            old_password: Old password (optional, for non-admin password changes)

        Returns:
            bool: True if successful, False otherwise
        """
        user_dn = f"cn={username},ou=users,{self.base_dn}"
        
        try:
            if old_password:
                # User changing their own password
                self.conn.extend.standard.modify_password(user_dn,
                                                        old_password,
                                                        new_password)
            else:
                # Admin changing user's password
                self.conn.modify(user_dn,
                               {'userPassword': [(MODIFY_REPLACE, [new_password])]})
            
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully changed password for user: {username}")
                return True
            else:
                logger.error(f"Failed to change password: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error changing password: {e}")
            return False

def main():
    """Example usage of LDAPUserManager."""
    # Connection parameters
    LDAP_HOST = 'ldap://localhost:389'
    ADMIN_DN = 'cn=admin,dc=example,dc=com'
    ADMIN_PASSWORD = 'admin_password'

    # Create a new user
    new_user = {
        'givenName': 'John',
        'sn': 'Doe',
        'mail': 'john.doe@example.com',
        'userPassword': 'initial_password'
    }

    with LDAPUserManager(LDAP_HOST, ADMIN_DN, ADMIN_PASSWORD) as ldap_mgr:
        # Create user
        ldap_mgr.create_user('jdoe', new_user)

        # Modify user attributes
        modifications = {
            'mail': [(MODIFY_REPLACE, ['john.doe.new@example.com'])],
            'telephoneNumber': [(MODIFY_ADD, ['+1234567890'])]
        }
        ldap_mgr.modify_user('jdoe', modifications)

        # Add to groups
        ldap_mgr.add_to_group('jdoe', 'developers')
        ldap_mgr.add_to_group('jdoe', 'project-a')

        # Get user's groups
        groups = ldap_mgr.get_user_groups('jdoe')
        print(f"User's groups: {groups}")

        # Change password
        ldap_mgr.change_password('jdoe', 'new_password')

        # Remove from group
        ldap_mgr.remove_from_group('jdoe', 'project-a')

if __name__ == '__main__':
    main()
