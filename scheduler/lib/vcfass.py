"""Module with IBM Cloud VMware Cloud Foundation (VCF) as a Service API calls.

https://cloud.ibm.com/apidocs/vmware-service#list-director-sites
"""


import logging
from typing import Any

from lib.requests_session import requests_session

log = logging.getLogger(__name__)


def list_director_sites(ibm_iam_access_token: str, region: str) -> dict[str, Any]:
    """List Cloud Director site instances.

    List all VMware Cloud Director site instances the user can access
    in the cloud account.

    Args:
        ibm_iam_access_token: IBM IAM access token.
        region: VCF as a Service Director region, e.g., "eu-fr2".

    Returns:
        Dictionary with VMware Cloud Director site instances.
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """
    s = requests_session()

    base_url = f"https://api.{region}.vmware.cloud.ibm.com"

    endpoint_url = "/".join([base_url, "v1", "director_sites"])

    headers = {"authorization": f"Bearer {ibm_iam_access_token}"}

    log.debug("Request VCFaaS Director sites.")
    r = s.get(url=endpoint_url, headers=headers)
    r.raise_for_status()
    log.debug(f'Got {len(r.json()["director_sites"])} VCFaaS Director sites.')

    return r.json()

def get_vmware_access_token(ibm_iam_access_token: str, url: str, org: str) -> str:
    """Retreive a VMWare Cloud Director session token represent in the X-VMWARE-VCLOUD-ACCESS-TOKEN header.

    Args:
        ibm_iam_access_token : An IBM IAM Session key
        url: Director site base URL, eg, https://dirw002.eu-de.vmware.cloud.ibm.com
        org: The organization the Director Site is a memeber of

    Returns:
        A VMWare VCD Access Token to be used in future API calls to VCD
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

   # request retry mechanism
    s = requests_session()

    endpoint_url = "/".join([url, "cloudapi", "1.0.0", "sessions"])

    headers = {"Authorization": f"Bearer {ibm_iam_access_token}; org={org}",
               "Accept": "application/*;version=36.2"}

    log.debug("Requesting VMWare Access Token")
    r = s.post(url=endpoint_url, headers=headers)
    r.raise_for_status()
    return r.headers["X-VMWARE-VCLOUD-ACCESS-TOKEN"]


def list_vcfaas_vdcs(ibm_iam_access_token: str, region: str) -> dict[str, Any]:
    """Retreive all VDC's for a specific region

    Args:
        ibm_iam_access_token: IBM IAM access token.
        region: VCF as a Service Director region, e.g., "eu-fr2".

    Returns:
        A VMWare VCD Access Token to be used in future API calls to VCD
    
    Raises:
        requests.RequestException: all Requests package exceptions
            can be raised due to, e.g., connection or authorization errors.
    """

   # request retry mechanism
    s = requests_session()

    base_url = f"https://api.{region}.vmware.cloud.ibm.com"

    endpoint_url = "/".join([base_url, "v1", "vdcs"])

    headers = {"authorization": f"Bearer {ibm_iam_access_token}",
               "Content-Type": "application/json"}
    
    log.debug("Retrieving list of VDC")
    r = s.get(url=endpoint_url, headers=headers)
    r.raise_for_status()
    return r.json()