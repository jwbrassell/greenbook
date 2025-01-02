"""
LDAP3 Search Operations Example

This example demonstrates various search operations and filtering techniques using the ldap3 package.
It includes examples of basic and advanced searches, attribute filtering, and result handling.
"""

from ldap3 import Server, Connection, ALL, SUBTREE, LEVEL, BASE
from ldap3.core.exceptions import LDAPException
from ldap3.utils.conv import escape_filter_chars
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LDAPSearcher:
    def __init__(self, host: str, admin_dn: str, admin_password: str):
        """Initialize LDAP connection for searching.

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

    def basic_search(self, search_filter: str, attributes: List[str]) -> List[Dict]:
        """Perform a basic search operation.

        Args:
            search_filter: LDAP search filter
            attributes: List of attributes to retrieve

        Returns:
            List[Dict]: List of search results
        """
        try:
            self.conn.search(
                self.base_dn,
                search_filter,
                attributes=attributes
            )
            
            return [entry.entry_attributes_as_dict for entry in self.conn.entries]
        except LDAPException as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_users(self, criteria: Dict[str, str] = None) -> List[Dict]:
        """Search for users based on criteria.

        Args:
            criteria: Dictionary of search criteria (e.g., {'department': 'IT'})

        Returns:
            List[Dict]: List of matching users
        """
        # Start with base filter
        filter_parts = ['(objectClass=person)']
        
        # Add criteria to filter
        if criteria:
            for attr, value in criteria.items():
                filter_parts.append(f'({attr}={escape_filter_chars(value)})')
        
        # Combine all filters with AND
        search_filter = f'(&{"".join(filter_parts)})'
        
        try:
            self.conn.search(
                self.base_dn,
                search_filter,
                attributes=['cn', 'givenName', 'sn', 'mail', 'department']
            )
            
            return [entry.entry_attributes_as_dict for entry in self.conn.entries]
        except LDAPException as e:
            logger.error(f"User search failed: {e}")
            return []

    def search_groups(self, group_name: Optional[str] = None) -> List[Dict]:
        """Search for groups and their members.

        Args:
            group_name: Optional group name to search for

        Returns:
            List[Dict]: List of matching groups and their members
        """
        filter_parts = ['(objectClass=groupOfNames)']
        if group_name:
            filter_parts.append(f'(cn={escape_filter_chars(group_name)})')
        
        search_filter = f'(&{"".join(filter_parts)})'
        
        try:
            self.conn.search(
                self.base_dn,
                search_filter,
                attributes=['cn', 'member', 'description']
            )
            
            return [entry.entry_attributes_as_dict for entry in self.conn.entries]
        except LDAPException as e:
            logger.error(f"Group search failed: {e}")
            return []

    def search_by_scope(self, base_dn: str, search_filter: str,
                       scope: str = SUBTREE) -> List[Dict]:
        """Search with specific scope.

        Args:
            base_dn: Base DN for search
            search_filter: LDAP search filter
            scope: Search scope (BASE, LEVEL, or SUBTREE)

        Returns:
            List[Dict]: List of search results
        """
        try:
            self.conn.search(
                base_dn,
                search_filter,
                search_scope=scope,
                attributes=['*']
            )
            
            return [entry.entry_attributes_as_dict for entry in self.conn.entries]
        except LDAPException as e:
            logger.error(f"Scoped search failed: {e}")
            return []

    def search_with_paging(self, search_filter: str, page_size: int = 100) -> List[Dict]:
        """Search with paging control.

        Args:
            search_filter: LDAP search filter
            page_size: Number of entries per page

        Returns:
            List[Dict]: Combined list of all search results
        """
        entries = []
        cookie = None
        
        try:
            while True:
                self.conn.search(
                    self.base_dn,
                    search_filter,
                    attributes=['*'],
                    paged_size=page_size,
                    paged_cookie=cookie
                )
                
                entries.extend([entry.entry_attributes_as_dict 
                              for entry in self.conn.entries])
                
                cookie = self.conn.result['controls']['1.2.840.113556.1.4.319'
                                                    ]['value']['cookie']
                if not cookie:
                    break
            
            return entries
        except LDAPException as e:
            logger.error(f"Paged search failed: {e}")
            return entries

    def advanced_search_examples(self) -> None:
        """Demonstrate various advanced search techniques."""
        
        # Example 1: Search with wildcards
        logger.info("Users with email ending in @example.com:")
        results = self.basic_search(
            '(&(objectClass=person)(mail=*@example.com))',
            ['cn', 'mail']
        )
        for result in results:
            print(f"Name: {result['cn']}, Email: {result['mail']}")

        # Example 2: Search with multiple criteria
        logger.info("\nIT department managers:")
        results = self.basic_search(
            '(&(objectClass=person)(department=IT)(title=*Manager*))',
            ['cn', 'title', 'department']
        )
        for result in results:
            print(f"Name: {result['cn']}, Title: {result['title']}")

        # Example 3: OR condition
        logger.info("\nUsers in IT or HR department:")
        results = self.basic_search(
            '(&(objectClass=person)(|(department=IT)(department=HR)))',
            ['cn', 'department']
        )
        for result in results:
            print(f"Name: {result['cn']}, Department: {result['department']}")

        # Example 4: NOT condition
        logger.info("\nUsers not in IT department:")
        results = self.basic_search(
            '(&(objectClass=person)(!(department=IT)))',
            ['cn', 'department']
        )
        for result in results:
            print(f"Name: {result['cn']}, Department: {result['department']}")

    def search_inactive_users(self, days_inactive: int) -> List[Dict]:
        """Search for users who haven't logged in for specified days.

        Args:
            days_inactive: Number of days since last login

        Returns:
            List[Dict]: List of inactive users
        """
        # Convert days to timestamp
        cutoff_date = datetime.now().timestamp() - (days_inactive * 86400)
        
        try:
            self.conn.search(
                self.base_dn,
                f'(&(objectClass=person)(lastLogon<={int(cutoff_date)}))',
                attributes=['cn', 'mail', 'lastLogon']
            )
            
            return [entry.entry_attributes_as_dict for entry in self.conn.entries]
        except LDAPException as e:
            logger.error(f"Inactive user search failed: {e}")
            return []

def main():
    """Example usage of LDAPSearcher."""
    # Connection parameters
    LDAP_HOST = 'ldap://localhost:389'
    ADMIN_DN = 'cn=admin,dc=example,dc=com'
    ADMIN_PASSWORD = 'admin_password'

    with LDAPSearcher(LDAP_HOST, ADMIN_DN, ADMIN_PASSWORD) as searcher:
        # Example 1: Basic user search
        print("\nBasic user search:")
        users = searcher.search_users({'department': 'IT'})
        for user in users:
            print(f"Found user: {user['cn']}")

        # Example 2: Group search
        print("\nGroup search:")
        groups = searcher.search_groups('developers')
        for group in groups:
            print(f"Group: {group['cn']}")
            print(f"Members: {group.get('member', [])}")

        # Example 3: Scoped search
        print("\nScoped search (LEVEL):")
        results = searcher.search_by_scope(
            'ou=users,dc=example,dc=com',
            '(objectClass=person)',
            LEVEL
        )
        for result in results:
            print(f"Found: {result['cn']}")

        # Example 4: Paged search
        print("\nPaged search:")
        all_entries = searcher.search_with_paging('(objectClass=person)', 50)
        print(f"Total entries found: {len(all_entries)}")

        # Example 5: Advanced search examples
        print("\nAdvanced search examples:")
        searcher.advanced_search_examples()

        # Example 6: Search for inactive users
        print("\nInactive users:")
        inactive_users = searcher.search_inactive_users(30)  # 30 days
        for user in inactive_users:
            print(f"Inactive user: {user['cn']}")

if __name__ == '__main__':
    main()
