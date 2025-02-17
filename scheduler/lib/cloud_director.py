import logging
import time

from typing import Any, Optional
from lib.requests_session import requests_session

log = logging.getLogger(__name__)
pageSize = 128

status = {-1: "FAILED_CREATION",
               1: "UNRESOLVED",
               2: "RESOLVED",
               3: "DEPLOYED",
               4: "POWERED_ON",
               5: "WAITING_FOR_INPUT",
               6: "UNKNOWN",
               7: "UNRECOGNIZED",
               8: "POWERED_OFF",
               9: "INCONSISTENT_STATE",
               10: "MIXED",
               11: "DESCRIPTOR_PENDING",
               12: "COPYING_CONTENTS",
               13: "DISK_CONTENT_PENDING",
               14: "QUARANTINED",
               15: "QUARANTINED_EXPIRED",
               16: "REJECTED",
               17: "TRANSFER_TIMEOUT",
               18: "VAPP_UNDEPLOYED",
               19: "VAPP_PARTIALLY_DEPLOYED",
               20: "PARTIALLY_POWERED_OFF",
               21: "PARTIALLY_SUSPENDED",
}

def query_vm(director_url: str, vmware_access_token: str, filter: str) -> dict[str, Any]:
    """List all VM filtered by the a filter

    Args:
        director_url: base director url, eg.: https://fradir01.vmware-solutions.cloud.ibm.com
        vmware_access_token: A VMWare VCD Session token.
        filter: A VCD Query filter, for example, name==virtual_machine_1

    Returns:
       A list of Virtual Machine records
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

    # request retry mechanism
    s = requests_session()

    endpoint_url = "/".join([director_url, "api", "query"])

    headers = {
        "Authorization": f"Bearer {vmware_access_token}",
        "Accept": "application/*+json;version=38.1"
    }

    params: dict[str, int | str] = {
        "filter": filter,
        "type": "vm",
        "format": "records",
        "pageSize": pageSize
    }
    
    log.debug(f'Query Virtual Machines with filter: {filter}')

    page_number = 0
    record = []
    more_pages = True

    while(more_pages):
        page_number = page_number + 1
        log.debug(f"Getting page {page_number}")
        params["page"] = page_number

        r = s.get(url=endpoint_url, headers=headers, params=params)
        r.raise_for_status()

        total = r.json()["total"]            
        record = record + r.json()["record"]
        more_pages = page_number*pageSize < total

    return record

def get_vapp_vm(vmware_access_token: str, href: str) -> dict[str, Any]:
    """Get the JSON Record of a VM or VAPP referenced by the provided href

    Args:
        director_url: base director url, eg.: https://fradir01.vmware-solutions.cloud.ibm.com
        vmware_access_token: A VMWare VCD Session token.
        href: THe href of the resource, eg, https://dirw002.eu-de.vmware.cloud.ibm.com/api/vApp/vm-0a782687-a2c2-44df-86f0-fce60e075d7c

    Returns:
        A VM or VAPP Record
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

    # request retry mechanism
    s = requests_session()

    headers = {
        "Authorization": f"Bearer {vmware_access_token}",
        "Accept": "application/*+json;version=38.1"
    }

    log.debug(f"Retrieving VAPP or VM")

    r = s.get(url=href, headers=headers)
    r.raise_for_status()

    return r.json()


def get_vm_metadata(vmware_access_token: str, href: str) -> dict[str, Any]:
    """Get the JSON Record of a VM or VAPP referenced by the provided href/metadata

    Args:
        director_url: base director url, eg.: https://fradir01.vmware-solutions.cloud.ibm.com
        vmware_access_token: A VMWare VCD Session token.
        href: THe href of the resource, eg, https://dirw002.eu-de.vmware.cloud.ibm.com/api/vApp/vm-0a782687-a2c2-44df-86f0-fce60e075d7c

    Returns:
        A metadata record
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

    # request retry mechanism
    s = requests_session()

    endpoint_url = "/".join([href, "metadata"])

    headers = {
        "Authorization": f"Bearer {vmware_access_token}",
        "Accept": "application/*+json;version=38.1"
    }

    log.debug(f'Retrieving metadata for {href}')

    r = s.get(url=endpoint_url, headers=headers)
    r.raise_for_status()

    return r.json()

def powerOff(href: str, vmware_access_token: str) -> dict[str, Any]:
    """Perform an Power Off operation on a VM or VAPP

    Args:
        href: Resource reference, eg, https://dirw002.eu-de.vmware.cloud.ibm.com/api/vApp/vm-0a782687-a2c2-44df-86f0-fce60e075d7c
        vmware_access_token: A VMWare VCD Session token.

    Returns:
        A task object
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

    # request retry mechanism
    s = requests_session()

    endpoint_url = "/".join([href, "power", "action", "powerOff"])

    headers = {
        "Authorization": f"Bearer {vmware_access_token}",
        "Accept": "application/*+json;version=38.0",
    }

    log.debug(f'Power Off: {href}')
    r = s.post(url=endpoint_url, headers=headers)
    r.raise_for_status()

    return r.json()

def powerOn(href: str, vmware_access_token: str) -> dict[str, Any]:
    """Perform an Power On operation on a VM or VAPP

    Args:
        href: Resource reference, eg, https://dirw002.eu-de.vmware.cloud.ibm.com/api/vApp/vm-0a782687-a2c2-44df-86f0-fce60e075d7c
        vmware_access_token: A VMWare VCD Session token.

    Returns:
        A task object
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

    # request retry mechanism
    s = requests_session()

    endpoint_url = "/".join([href, "power", "action", "powerOn"])

    headers = {
        "Authorization": f"Bearer {vmware_access_token}",
        "Accept": "application/*+json;version=38.0",
    }

    log.debug(f'Power On: {href}')
    r = s.post(url=endpoint_url, headers=headers)
    r.raise_for_status()

    return r.json()