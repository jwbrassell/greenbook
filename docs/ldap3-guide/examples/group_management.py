"""
LDAP3 Group Management Example

This example demonstrates group management operations using the ldap3 package.
It includes functions for creating, modifying, and deleting groups, as well as
managing group memberships and nested groups.
"""

from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPException, LDAPOperationResult
import logging
from typing import List, Dict, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LDAPGroupManager:
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

    def create_group(self, group_name: str, description: str = None) -> bool:
        """Create a new group.

        Args:
            group_name: Name of the group
            description: Optional group description

        Returns:
            bool: True if successful, False otherwise
        """
        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"
        
        # Default attributes for group
        attributes = {
            'objectClass': ['top', 'groupOfNames', 'group'],
            'cn': [group_name],
            # Add a dummy member as groupOfNames requires at least one member
            'member': ['cn=dummy,ou=users,{self.base_dn}']
        }
        
        if description:
            attributes['description'] = description

        try:
            self.conn.add(group_dn, attributes=attributes)
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully created group: {group_name}")
                return True
            else:
                logger.error(f"Failed to create group: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error creating group: {e}")
            return False

    def delete_group(self, group_name: str) -> bool:
        """Delete a group.

        Args:
            group_name: Name of the group to delete

        Returns:
            bool: True if successful, False otherwise
        """
        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"

        try:
            self.conn.delete(group_dn)
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully deleted group: {group_name}")
                return True
            else:
                logger.error(f"Failed to delete group: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error deleting group: {e}")
            return False

    def add_member(self, group_name: str, member_dn: str) -> bool:
        """Add a member to a group.

        Args:
            group_name: Name of the group
            member_dn: DN of the member to add

        Returns:
            bool: True if successful, False otherwise
        """
        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"

        try:
            self.conn.modify(group_dn,
                           {'member': [(MODIFY_ADD, [member_dn])]})
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully added member to group: {group_name}")
                return True
            else:
                logger.error(f"Failed to add member: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error adding member: {e}")
            return False

    def remove_member(self, group_name: str, member_dn: str) -> bool:
        """Remove a member from a group.

        Args:
            group_name: Name of the group
            member_dn: DN of the member to remove

        Returns:
            bool: True if successful, False otherwise
        """
        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"

        try:
            self.conn.modify(group_dn,
                           {'member': [(MODIFY_DELETE, [member_dn])]})
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully removed member from group: {group_name}")
                return True
            else:
                logger.error(f"Failed to remove member: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error removing member: {e}")
            return False

    def get_group_members(self, group_name: str) -> List[str]:
        """Get all members of a group.

        Args:
            group_name: Name of the group

        Returns:
            List[str]: List of member DNs
        """
        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"

        try:
            self.conn.search(group_dn,
                           '(objectClass=*)',
                           attributes=['member'])
            
            if not self.conn.entries:
                logger.error(f"Group not found: {group_name}")
                return []
                
            if 'member' in self.conn.entries[0]:
                return list(self.conn.entries[0].member)
            return []
        except LDAPException as e:
            logger.error(f"Error getting group members: {e}")
            return []

    def get_nested_members(self, group_name: str, processed_groups: Set[str] = None) -> Set[str]:
        """Get all members of a group, including members of nested groups.

        Args:
            group_name: Name of the group
            processed_groups: Set of already processed groups (for recursion)

        Returns:
            Set[str]: Set of all member DNs
        """
        if processed_groups is None:
            processed_groups = set()

        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"
        if group_dn in processed_groups:
            return set()

        processed_groups.add(group_dn)
        members = set()

        try:
            self.conn.search(group_dn,
                           '(objectClass=*)',
                           attributes=['member'])
            
            if not self.conn.entries:
                return members

            for member_dn in self.conn.entries[0].member:
                members.add(member_dn)
                # If member is a group, get its members recursively
                if 'ou=groups' in member_dn:
                    nested_group = member_dn.split(',')[0].split('=')[1]
                    members.update(self.get_nested_members(nested_group, processed_groups))

            return members
        except LDAPException as e:
            logger.error(f"Error getting nested members: {e}")
            return members

    def modify_group(self, group_name: str, modifications: Dict) -> bool:
        """Modify group attributes.

        Args:
            group_name: Name of the group
            modifications: Dictionary of modifications

        Returns:
            bool: True if successful, False otherwise
        """
        group_dn = f"cn={group_name},ou=groups,{self.base_dn}"

        try:
            self.conn.modify(group_dn, modifications)
            if self.conn.result['result'] == 0:
                logger.info(f"Successfully modified group: {group_name}")
                return True
            else:
                logger.error(f"Failed to modify group: {self.conn.result['description']}")
                return False
        except LDAPException as e:
            logger.error(f"Error modifying group: {e}")
            return False

def main():
    """Example usage of LDAPGroupManager."""
    # Connection parameters
    LDAP_HOST = 'ldap://localhost:389'
    ADMIN_DN = 'cn=admin,dc=example,dc=com'
    ADMIN_PASSWORD = 'admin_password'

    with LDAPGroupManager(LDAP_HOST, ADMIN_DN, ADMIN_PASSWORD) as group_mgr:
        # Create groups
        group_mgr.create_group('developers', 'Development team')
        group_mgr.create_group('project-a', 'Project A team')
        group_mgr.create_group('admins', 'System administrators')

        # Add members
        user1_dn = 'cn=john,ou=users,dc=example,dc=com'
        user2_dn = 'cn=jane,ou=users,dc=example,dc=com'
        
        group_mgr.add_member('developers', user1_dn)
        group_mgr.add_member('developers', user2_dn)
        group_mgr.add_member('project-a', user1_dn)

        # Create nested group structure
        group_mgr.add_member('admins', 'cn=developers,ou=groups,dc=example,dc=com')

        # Get group members
        dev_members = group_mgr.get_group_members('developers')
        print(f"Developer group members: {dev_members}")

        # Get nested members
        admin_members = group_mgr.get_nested_members('admins')
        print(f"Admin group members (including nested): {admin_members}")

        # Modify group
        modifications = {
            'description': [(MODIFY_REPLACE, ['Updated development team'])]
        }
        group_mgr.modify_group('developers', modifications)

        # Remove member
        group_mgr.remove_member('project-a', user1_dn)

if __name__ == '__main__':
    main()
