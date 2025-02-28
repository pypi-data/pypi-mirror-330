import requests
import json

import ipaddress

from time import sleep
from typing import Any, Dict, List

from .netbox_manager import NetboxManager
from ...utils.paths import PIPELINE_DESCRIPTION


def get_sot_filter_parameters():
    """
    Retrieves filter parameters from the pipeline description file.

    Returns:
        dict: Filter parameters extracted from the pipeline description.
    """

    with open(PIPELINE_DESCRIPTION) as f:
        data = json.load(f)

    return data['filter_params']    # Return the filter parameters extracted from the JSON data

filter_params = get_sot_filter_parameters() # Retrieving filter parameters

netbox_manager = NetboxManager(filter_params=filter_params) # Initializing NetboxManager with filter parameters

# Retrieving NetBox URL, filter parameters, session, and API
nb_url = netbox_manager.nb_url  
filter_parameters = netbox_manager.filter_parameters
session = netbox_manager.session
nb_api = netbox_manager.get_netbox_api()


def get_inventory():
    """
    Retrieves inventory data using NetboxManager.

    Returns:
        dict: Inventory data obtained from Netbox.
    """

    return netbox_manager.get_inventory()


def get_circuits(url: str = f"{nb_url}/api/circuits/circuits/?limits=0", params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Retrieves circuit information from Netbox.

    Args:
        url (str, optional): The URL to retrieve circuit data from.
        params (Dict[str, Any], optional): Additional parameters for the API request.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing circuit information.
    """

    circuits: List[Dict[str, Any]] = []

    """
    for param, filter in params.items():
        while url:
            r = session.get(url, params={param: filter})
            if not r.status_code == 200:
                raise ValueError(
                    f"Failed to get data from NetBox instance {nb_url}"
                )

            resp = r.json()
            circuits.extend(resp.get("results"))

            url = resp.get("next")
    """
    
    while url:  # Loop while there is a valid URL to fetch data from
        if params:
            r = session.get(url, params=params) # Perform a GET request with the parameters
        else:
            r = session.get(url)    # Perform a GET request without parameters
        
        if not r.status_code == 200:
            raise ValueError(
                f"Failed to get data from NetBox instance {nb_url}"
            )

        resp = r.json()
        circuits.extend(resp.get("results"))    # Add the results to the circuits list

        url = resp.get("next")

    return circuits # Return the complete list of circuits


def get_circuit_terminations(params: Dict[str, Any] = None):
    """
    Retrieves circuit terminations from Netbox based on specified parameters.

    Args:
        params (Dict[str, Any], optional): Additional parameters for the API request.

    Returns:
        Dict[str, Any]: Dictionary containing circuit terminations.
    """

    if params:
        circuits = get_circuits(params=params)  # Fetch circuits data with provided parameters
    else:
        circuits = get_circuits()   # Fetch circuits data without any parameters
        
    terminations = {}
    for circuit in circuits:    # Fetch termination information for termination A of the circuit
        termination_a = get_resources(
            url=f"{nb_url}/api/circuits/circuit-terminations/", params={"id": circuit["termination_a"]["id"]})
        
        termination_z = get_resources(  # Fetch termination information for termination Z of the circuit
            url=f"{nb_url}/api/circuits/circuit-terminations/", params={"id": circuit["termination_z"]["id"]})
        
        c_name = circuit["display"] # Get the display name of the circuit
        terminations[c_name] = [termination_a[0], termination_z[0]]

    return terminations # Return the dictionary containing circuit terminations


def get_device_by_name(device_name):
    """
	TODO: write docstrings
	"""

    devices = nb_api.dcim.devices.filter(
        name=device_name)
    device = {}
    for d in devices:
        device = d
    return device


def get_resources(url: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Retrieves resources from Netbox based on specified URL and parameters.

    Args:
        url (str): The URL to retrieve resources from.
        params (Dict[str, Any]): Additional parameters for the API request.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing resource information.
    """

    resources: List[Dict[str, Any]] = []     # Initialize an empty list to store resources

    while url:  
        # Send a GET request to the specified URL with optional parameters
        r = session.get(url, params=params)

        if not r.status_code == 200:
            raise ValueError(
                f"Failed to get data from NetBox instance {nb_url}"
            )

        resp = r.json()
        resources.extend(resp.get("results"))   # Extend the resources list with the results from the response

        url = resp.get("next")  # Update the URL for the next page of results

    return resources


def get_device_by_name(device_name):
    """
    Retrieves a device by its name from NetBox.

    Args:
        device_name (str): The name of the device to retrieve.

    Returns:
        Dict[str, Any]: A dictionary containing information about the device.
    """

    devices = nb_api.dcim.devices.filter(   # Filter devices by name
        name=device_name)
    device = {}

    for d in devices:
        device = d  # Assign the current device to the 'device' dictionary

    return device   # Return the device information


def get_prefix_ipv4_client(role_name, tenant_name, family_number=4):
    """
    Retrieves IPv4 prefixes assigned to a client based on role and tenant.

    Args:
        role_name (str): The role name of the prefixes.
        tenant_name (str): The name of the tenant.
        family_number (int, optional): The IP family number. Defaults to 4.

    Returns:
        List[str]: A list of IPv4 prefixes assigned to the client.
    """

    roles = nb_api.ipam.prefixes.filter(
        role=role_name, tenant=tenant_name, family=family_number)
    
    prefixes = []
    for role in roles:
        prefix = role["prefix"] # Extract the prefix information
        prefixes.append(prefix) # Append the prefix to the list
        
    return prefixes # Return the list of prefixes


def get_interface_by_name_device(interface_name, device_name):
    """
    Retrieves an interface by its name and associated device from NetBox.

    Args:
        interface_name (str): The name of the interface to retrieve.
        device_name (str): The name of the device associated with the interface.

    Returns:
        Dict[str, Any]: A dictionary containing information about the interface.
    """

    interfaces = nb_api.dcim.interfaces.filter(
        name=interface_name, device=device_name)
    interface = {}

    for i in interfaces:
        interface = i   # Update the interface dictionary with the current interface

    return interface    # Return the interface dictionary


def get_interface_by_label_device(if_label, device_name):
    """
    Retrieves an interface by its label and associated device from NetBox.

    Args:
        if_label (str): The label of the interface to retrieve.
        device_name (str): The name of the device associated with the interface.

    Returns:
        str: A string representation of the retrieved interface.
    """

    interfaces = nb_api.dcim.interfaces.filter(
        label=if_label, 
        device=device_name
    )

    for i in interfaces:  
        interface = i   # Update the interface variable with the current interface

    return str(interface)   # Return a string representation of the interface


def get_interface_child_by_parent_device(interface_name, device_name):
    """
	TODO: write docstrings
    Warning: Juniper Only
	"""

    interfaces = nb_api.dcim.interfaces.filter( device=device_name )

    for i in interfaces:
        if str(interface_name) in str(i) and '.' in str(i):
            interface = i   # Update the interface variable with the current interface

    return str(interface)   # Return a string representation of the interface


def get_interface_parent_by_child_device(interface_name, device_name):
    """
	TODO: write docstrings
    Warning: Juniper Only
	"""

    interfaces = nb_api.dcim.interfaces.filter( device=device_name )

    for i in interfaces:
        phy_int = str(interface_name).split('.')[0] # Extract the physical interface name
        if phy_int in str(i) and '.' not in str(i): # Check if the physical interface name is in the current interface object and if it's not a subinterface
            interface = i

    return str(interface)   # Return a string representation of the interface

    
def get_interfaces_unused_device(device_name):
    """
	TODO: write docstrings
    Warning: Juniper Only
	"""

    interfaces = nb_api.dcim.interfaces.filter( device=device_name )
    unused_ints = []

    for i in interfaces:
        if '.' not in i['name'] and i['label'] == '':    # Check if the interface name does not contain a dot (indicating it's not a subinterface) and if it has no label
            unused_ints.append(str(i))

    return unused_ints  # Return the list of unused interfaces


def get_interface_all_ips_by_device(interface_name, device_name):
    """
    Retrieves all IP addresses assigned to an interface of a device from NetBox.

    Args:
        interface_name (str): The name of the interface.
        device_name (str): The name of the device.

    Returns:
        Dict[str, str]: A dictionary mapping IP address types to IP addresses.
    """

    ips = {}

    for ip_address in nb_api.ipam.ip_addresses.all():

        for key in dict(ip_address).keys(): # Iterate through keys of the IP address object
            if key == "assigned_object" and ip_address["assigned_object"]:
                if ip_address["assigned_object"]["name"] == interface_name and ip_address["assigned_object"]["device"]["name"] == device_name:  # Check if the IP address is assigned to the specified interface 
                    ip_obj = ipaddress.ip_interface(ip_address["address"])
                    ip_version = 'ipv4' if ip_obj.version == 4 else 'ipv6'  # Determine IP version (IPv4 or IPv6)
                    ip_type = ''

                    for attr in dir(ip_obj):    # Iterate through attributes of the IP interface object
                        if attr.startswith('is_') and getattr(ip_obj, attr):     # Check if the attribute indicates a specific IP type
                            ip_type += '_' + attr[3:]   # Append IP type to the ip_type variable

                    ip_key = f'{ip_version}{ip_type}'   # Create a key for the IP address dictionary based on IP version and type
                    ips[ip_key] = str(ip_obj)

    return ips  # Return the dictionary containing IP addresses


def get_interface_ips_by_interface_name(interface_name, device_name):
    """
    Retrieves IP addresses assigned to a specific interface of a device from NetBox.

    Args:
        interface_name (str): The name of the interface.
        device_name (str): The name of the device.

    Returns:
        Dict[str, str]: A dictionary mapping IP address families to IP addresses.
    """

    ips = {}
    for ip_address in nb_api.ipam.ip_addresses.all():
        for key in dict(ip_address).keys(): # Iterate through keys of the IP address object
            if key == "assigned_object" and ip_address["assigned_object"]:  # Check if the IP address is assigned to an object
                if ip_address["assigned_object"]["name"] == interface_name and ip_address["assigned_object"]["device"]["name"] == device_name:
                    ips[ip_address["family"]["label"]] = ip_address["address"]  

    return ips  # Return the dictionary containing IP addresses


def get_config_context_data(device_name):
    """
    Retrieves configuration context data of a device from NetBox.

    Args:
        device_name (str): The name of the device.

    Returns:
        Dict[str, Any]: Configuration context data of the device.
    """

    # Retrieve configuration context data of a device from NetBox
    return nb_api.dcim.devices.filter( name=device_name )["config_context"]


def get_custom_script_result(result_url, nb_token=netbox_manager.nb_token):
    """
    Retrieves the result of a custom script execution from NetBox.

    Args:
        result_url (str): The URL of the result.
        nb_token (str, optional): NetBox API token. Defaults to netbox_manager.nb_token.

    Returns:
        Tuple[Dict[str, Any], str]: A tuple containing the result JSON and the status.
    """

    headers = {'Authorization': f"Token {nb_token}" }                    
    r = requests.get(result_url, headers=headers)                       
    status = r.json()['status']['value']    # Extract status value from the JSON response

    return r.json(), status # Return the JSON response and status value
    

def post_custom_script(data, script_urn=None, nb_url=nb_url, nb_token=netbox_manager.nb_token):
    """
    Executes a custom script in NetBox.

    Args:
        data (Union[Dict[str, Any], str]): The data to be sent in the request body.
        script_urn (str, optional): The URN of the script. Defaults to None.
        nb_url (str, optional): The URL of the NetBox instance. Defaults to nb_url.
        nb_token (str, optional): NetBox API token. Defaults to netbox_manager.nb_token.

    Raises:
        Exception: If the POST request to NetBox fails.
    """
    
    headers = {
        'Content-type': 'application/json', 
        'Authorization': f'Token {nb_token}', 
        'Accept': 'application/json; indent=4'
    }

    if type(data) == dict:
        data = json.dumps(data)
    
    response = requests.post(    # Send a POST request to the specified URL with headers and data
        nb_url+script_urn,
        headers=headers,
        data=data
    )

    if response.status_code == 200:
        print(f"SUCCESSFULLY made the POST to Netbox Custom Script: {script_urn.split('/')[-2]}")
        print(f"Response MESSAGE: ")
        print(json.dumps(response.json(), indent=4))

        result_url = response.json()['result']['url']   # Extract the result URL from the response JSON
        print(f"Result URL: {result_url}")
        status='pending'

        while status == 'pending':  # Loop until the script execution status changes from 'pending'
            rqr, status = get_custom_script_result(result_url, nb_token) # rqr = Result Query Response
            print("Waiting for next query result...")
            sleep(10)

        if status == 'completed':
            print('Script run was SUCCESSFULL!')
            print('Successfull response: ')
            print(json.dumps(rqr, indent=4))
            exit(0)
        else:
            print('Script run FAILED')
            print(f'FAILED status: {status}')
            print('FAILED response: ')
            print(json.dumps(rqr, indent=4))
            exit(1)

    else:
        # Print error message and response details if the POST request failed
        print(f"POST to Netbox Custom Script {script_urn.split('/')[-1]} FAILED")
        print(f"Response STATUS CODE: {response.status_code}")
        print(f"Response MESSAGE: {response.text}")
        exit(1)
    return

filter_params = get_sot_filter_parameters()