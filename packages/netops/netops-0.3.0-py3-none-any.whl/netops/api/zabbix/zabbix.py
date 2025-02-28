import sys
import logging
from pyzabbix import ZabbixAPI
from time import sleep

import ipaddress


def init_zapi(zabbix_url, zabbix_user, zabbix_pass):
    """Connects to Zabbix API and returns a ZabbixAPI instance.

    Args:
        zabbix_url (str): Zabbix server URL.
        zabbix_user (str): Username for API authentication.
        zabbix_pass (str): Password for API authentication.

    Returns:
        ZabbixAPI: Connected ZabbixAPI instance.

    Raises:
        ZabbixApiError: If connection or authentication fails.
    """

    # API Token authentication is just able with Zabbix >= 5.4
    # zapi.login(api_token='xxxxx')
    zapi = ZabbixAPI(zabbix_url)    # Connect to Zabbix API using provided credentials
    zapi.login(zabbix_user, zabbix_pass)    # Authenticate with the Zabbix API
    print("Connected to Zabbix API Version %s\n" % zapi.api_version())

    """
    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(logging.DEBUG)
    log = logging.getLogger('pyzabbix')
    log.addHandler(stream)
    log.setLevel(logging.DEBUG)
    """
    
    return zapi


def get_hostid(zapi, host_name):
    """Gets host ID by name from Zabbix API.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        host_name (str): Name of the host.

    Returns:
        str: Host ID (or exits with error if not found).

    Raises:
        ZabbixApiError: On API communication errors.
    """

    print(f"Getting host ID of host {host_name} from Zabbix API...\n")

    hosts_filtered = zapi.host.get(output="extend", filter={"host": host_name}) # Filtering hosts by name

    if hosts_filtered == []:    # Exit if no host found with the provided name
        print(f"ERROR! Host '{host_name}' could not be find on Zabbix.")
        print(f"ERROR! Please check the host name on {zapi.url}\n")
        exit(1)

    for h in hosts_filtered:    # Find the host with matching name
        if h['host'] == host_name:
            h_updated = h
    
    return h_updated['hostid']  # Return host ID


def get_hostname(zapi, zhostid):
    """Gets hostname by ID from Zabbix API.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        zhostid (str): ID of the host.

    Returns:
        str: Hostname (or exits with error if not found).

    Raises:
        ZabbixApiError: On API communication errors.
    """

    print(f"Getting host ID {zhostid} from Zabbix API...\n")

    hosts_filtered = zapi.host.get(output="extend", filter={"hostid": zhostid}) # Retrieve host information

    if hosts_filtered == []:    # Error if no host is found
        print(f"ERROR! Host ID '{zhostid}' could not be find on Zabbix.")
        print(f"ERROR! Please check the host name on {zapi.url}\n")
        exit(1)

    for h in hosts_filtered:    # Iterate through hosts
        if h['hostid'] == zhostid:
            host_name = h['host']   # Store hostname
        
    return host_name


def get_groupname(zapi, zgroupid):
    """Gets group name by ID from Zabbix API.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        zgroupid (str): ID of the host group.

    Returns:
        str: Group name (or exits with error if not found).

    Raises:
        ZabbixApiError: On API communication errors.
    """

    print(f"Getting group ID {zgroupid} from Zabbix API...\n")

    groups_filtered = zapi.hostgroup.get(output="extend", filter={"groupid": zgroupid}) # Retrieve group information
    print(f"Groups got from Zabbix API: {groups_filtered}")
    
    if groups_filtered == []:   # Error if no group is found
        print(f"ERROR! Group ID '{zgroupid}' could not be find on Zabbix.")
        print(f"ERROR! Please check the group name on {zapi.url}\n")
        exit(1)

    for g in groups_filtered:   # Iterate through groups
        if g['groupid'] == zgroupid:
            group_name = g['name']  # Store group name
    
    print("Group name match: ", group_name)
    
    return group_name


def get_groupid(zapi, group_name):
    """Gets group ID by name from Zabbix API.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        group_name (str): Name of the host group.

    Returns:
        str: Group ID (or exits with error if not found).

    Raises:
        ZabbixApiError: On API communication errors.
    """

    groups_filtered = zapi.hostgroup.get(output="extend", filter={"name": group_name})  # Retrieve group information

    if groups_filtered == []:   # Error if no group is found
        print(f"ERROR! Group '{group_name}' could not be find on Zabbix.")
        print(f"ERROR! Please check the group names on {zapi.url}\n")
        exit(1)

    for g in groups_filtered:
        if g['name'] == group_name:     # Check for matching group name
            groupid = g['groupid']      # Store group ID
    
    return groupid
        

def get_hostinterfaceid(zapi, host_name):
    """Gets first interface ID of a Zabbix host.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        host_name (str): Name of the host.

    Returns:
        str: ID of the first interface (or exits with error if not found).

    Raises:
        ZabbixApiError: On API communication errors.
    """

    zhostid = get_hostid(zapi, host_name)
    print(f"Getting host interface of host {host_name} from Zabbix API...\n")

    interfaces_filtered = zapi.hostinterface.get(output="extend", filter={"hostids": zhostid})  # Retrieve interfaces

    if interfaces_filtered == []:   # Error if no interface is found
        print(f"ERROR! Host interfaces of host '{host_name}' could not be find on Zabbix.")
        print(f"ERROR! Please check the host name and its interfaces on {zapi.url}")
        exit(1)

    for i in interfaces_filtered:
        if i['hostid'] == zhostid:  # Check for matching host ID
            iid_updated = i['interfaceid']  # Store interface ID
        
    return iid_updated # Return interface ID


def get_templateid(zapi, ztemplatename):
    """Gets template ID by name from Zabbix API.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        ztemplatename (str): Name of the template.

    Returns:
        str: Template ID (or None if not found).

    Raises:
        Exception: On API errors or template not found.
    """

    try:    
        templates = zapi.template.get(filter={"host": ztemplatename}, output=["templateid"])    # Search for templates with matching name
        if templates:
            return templates[0]['templateid']   # Return ID of the first template
        else:
            raise Exception(f"Template '{ztemplatename}' não encontrado.")
    except Exception as e:
        print(e)
        return None


def update_host_name(zapi, host_name, new_name):
    """Updates the visible name of a Zabbix host.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        host_name (str): Current name of the host to update.
        new_name (str): New visible name for the host.

    Raises:
        Exception: On API errors or host update failures.
    """

    zhostid = get_hostid(zapi, host_name)   # Retrieve host ID first

    try:
        zapi.host.update(hostid=zhostid, name=new_name) # Update host name

        print(f"Visible Name of host '{host_name}' changed to '{new_name}'\n")
        print("")
        sleep(5)
    except Exception as e:
        print(e)
        exit(1)

    return


def create_host_name(zapi, host_name, new_name):
    """Creates a new Zabbix host with group association.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        host_name (str): Desired hostname for the new host.
        new_name (str): Visible name for the new host.
        group_id (str, optional): Host group ID (defaults to "1").

    Raises:
        Exception: On API errors or host creation failures (existing name).
    """

    zapi.host.create(   # Attempt to create the host
        host=host_name,
        name=new_name,
        groups=[{"groupid": "1"}]  # Group ID to which the host belongs
    )
    print(f"Host '{host_name}' does not exist. Creating it with name '{new_name}'\n")
    print("")
    print(f"Host '{host_name}' created with name '{new_name}'\n")
    sleep(5)


def update_hostinterface(zapi, host_name, interface_value):
    """Updates IP/DNS of the host's first interface.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        host_name (str): Name of the host with the interface.
        interface_value (str): New IP address or DNS name.

    Raises:
        Exception: On API errors, interface retrieval issues, or update failures.
        ValueError: If `interface_value` is not a valid IP address.
    """

    zhostinterfaceid = get_hostinterfaceid(zapi, host_name) # Retrieve interface ID

    try:    # Update interface based on IP or DNS type
        ipaddress.ip_address(interface_value)   # Validate as IP address
        is_ip = True
    except ValueError:
        is_ip = False

    try:    
        if is_ip:
            zapi.hostinterface.update(  # Update interface IP
                interfaceid=zhostinterfaceid, 
                ip=interface_value
            )
            print(f"The IP address of host '{host_name}' has been changed to '{interface_value}'\n")
            print("")
        else:
            zapi.hostinterface.update(  # Update interface DNS
                interfaceid=zhostinterfaceid, 
                dns=interface_value
            )
            print(f"DNS of host '{host_name}' has been changed to  '{interface_value}'\n")
            print("")
        sleep(5)
    except Exception as e:
        print(e)
        exit(1)

    return


def create_hostinterface(zapi, host_name, interface_value):
    """Creates a new interface (IP or DNS) for a host.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        host_name (str): Name of the host for the new interface.
        interface_value (str): IP address or DNS name of the interface.

    Raises:
        Exception: On API errors, host retrieval issues, or creation failures.
        ValueError: If `interface_value` is not a valid IP address.
    """

    host_id = get_hostid(zapi, host_name)   # Retrieve host ID

    try:
        ipaddress.ip_address(interface_value)   # Validate as IP address
        is_ip = True
    except ValueError:
        is_ip = False

    try:    # Create interface based on IP or DNS type
        if is_ip:
            zapi.hostinterface.create(
                hostid=host_id,
                dns='', # Set empty for IP interface
                ip=interface_value,
                port="161",
                main=1,
                useip=1,
                type=2,
                details={
                    "version": "2", 
                    "bulk": "1", 
                    "community": "{$SNMP_COMMUNITY}"    # Placeholder for actual community
                }
            )
            print(f"A new IP interface with value '{interface_value}' has been created for host '{host_name}'\n")
        else:
            zapi.hostinterface.create(
                hostid=host_id,
                dns=interface_value,
                ip='',  # Set empty for DNS interface
                port="161",
                main=1,
                useip=0,
                type=2,
                details={
                    "version": "2", 
                    "bulk": "1", 
                    "community": "{$SNMP_COMMUNITY}"    # Placeholder for actual community
                }
            )

            print(f"A new DNS interface with value '{interface_value}' has been created for host '{host_name}'\n")
            sleep(5)
    except Exception as e:
        print(e)
        exit(1)


def remove_hostgroup_from_host(zapi, zhostname, zgroupname):
    """Removes a host from a specified host group.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        hostname (str): Name of the host to remove.
        group_name (str): Name of the group to remove from.

    Raises:
        Exception: On API errors or retrieval/removal issues.
    """
    
    zhostid = get_hostid(zapi, zhostname)   # Retrieve the host ID
    zgroupid = get_groupid(zapi, zgroupname)    # Retrieve the group ID 
    
    try:
        zapi.hostgroup.massremove(  # Remove the host from the specified group
            groupids=[zgroupid],
            hostids= [zhostid]
        )
        print(f"Host '{zhostname}' removed from hostgroup name '{zgroupname}' ID '{zgroupid}'\n")

    except Exception as e:
        print(e)
    
    return


def remove_all_groups_from_host(zapi, zhostname):
    """Removes all host groups except 'generic_group' from the specified host. The respective group ('generic_group') needs to be created on Zabbix.

    Args:
        zapi (ZabbixAPI): An active ZabbixAPI instance.
        zhostname (str): The name of the host to remove groups from.

    Raises:
        Exception: If an error occurs during API communication or group operations.
    """

    zhostid = get_hostid(zapi, zhostname)
    try:
        generic_group_id = get_groupid(zapi, 'generic_group')

        group_ids_to_keep = [{"groupid": generic_group_id}] if generic_group_id else [] # associate 'generic_group' with host groups

        groups = zapi.host.get(hostids=zhostid, selectGroups="extend")  # Get all groups associated with the host
        
        zapi.host.update(   ## Update the host with the list of group IDs to keep
            hostid=zhostid,
            groups=[{"groupid": generic_group_id}]
        )

        for group in groups[0]["groups"]:   # Remove all non-'generic_group' groups from the host
            if group["name"] != "generic_group":
                zapi.hostgroup.massremove(
                    groupids=[group["groupid"]], hostids=[zhostid]
                )

        zapi.host.update(   # Update the host with the list of group IDs to keep
            hostid=zhostid,
            groups=group_ids_to_keep
        )

        print(f"All groups have been removed from host '{zhostname}'.\n")
    except Exception as e:
        print(f"Error removing groups from host '{zhostname}': {e}\n")

    print("")
    sleep(5)


def add_hostgroup_to_host(zapi, zhostname, zgroupname):
    """Adds the host 'zhostname' to the host group 'zgroupname'.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        zhostname (str): Name of the host to add.
        zgroupname (str): Name of the host group to add the host to.

    Raises:
        Exception: On API errors or if host or group is not found.
    """
    
    zhostid = get_hostid(zapi, zhostname)   # Retrieve the host ID
    zgroupid = get_groupid(zapi, zgroupname)    # Retrieve the group ID 

    try:    # Attempt to add the host to the group
        zapi.hostgroup.massadd(
            groups=[{"groupid": zgroupid}],
            hosts= [{"hostid": zhostid}]
        )
        print(f"Host '{zhostname}' added to hostgroup name '{zgroupname}' ID '{zgroupid}'\n")
        sleep(5)
    except Exception as e:
        print(e)


def add_template_to_host(zapi, zhostname, zgroupname, ztemplatename):
    """Associates template 'ztemplatename' with host 'zhostname' in group 'zgroupname'.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        zhostname (str): Name of the host.
        zgroupname (str): Name of the host group.
        ztemplatename (str): Name of the template.

    Raises:
        Exception: On API errors or if host, group, or template is not found.
    """
    
    zhostid = get_hostid(zapi, zhostname)   # Retrieve host ID
    zgroupid = get_groupid(zapi, zgroupname)    # Retrieve group ID
    ztemplateid = get_templateid(zapi, ztemplatename)   # Retrieve template ID

    try:    # Attempt to add the template to host
        zapi.host.massadd(
            hosts=[{"hostid": zhostid}], templates=[{"templateid": ztemplateid}]
        )
        print(f"Template '{ztemplatename}' adicionado ao host '{zhostname}' no grupo '{zgroupname}' (ID: {zgroupid})\n")
        sleep(5)
    except Exception as e:
        print(e)


def remove_all_templates_from_host(zapi, zhostname):
    """Removes all templates associated with a host.

    Args:
        zapi (ZabbixAPI): Active ZabbixAPI instance.
        zhostname (str): Name of the host.

    Raises:
        Exception: On API errors or if host is not found.
    """

    zhostid = get_hostid(zapi, zhostname)   # Retrieve host ID

    try:
        templates = zapi.template.get(hostids=zhostid)  # Get current templates associated with the host
        template_ids = [{"templateid": template["templateid"]} for template in templates]   # Extract template IDs from the retrieved information
        zapi.host.update(hostid=zhostid, templates=[])  # Update host with an empty templates list to remove all
        print(f"All templates have been removed from host '{zhostname}'.\n")
    except Exception as e:
        print(f"Error removing templates from host '{zhostname}': {e}\n")
    print("")
    sleep(5)
