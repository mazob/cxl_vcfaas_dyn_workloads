import argparse
import logging
import os
import json
import pathlib
import requests
import threading
import time
import signal
import lib.logger as logger
import lib.iam as iam
import lib.vcfass as vcfass
import lib.cloud_director as cloud_director
import lib.tags as tags

from types import SimpleNamespace
from urllib.parse import urlparse
from datetime import datetime, timedelta

tag_update_pause = 60   # How long between updates in seconds
resolution_window = 2   # Round up in minutes for task execution times, eg, 15 means tasks executed every 15 minutes

# configure logging
logger.config(os.path.basename(__file__))
log = logging.getLogger(__name__)

class ExitCommand(Exception):
    pass

def signal_handler(signal, frame):
    raise ExitCommand()

class Environment:

    # Class to handle global environment variables

    def __init__(self):
        # Get environment variables
        log.info('Retrieving Environment....')
        if 'ibmcloud_api_key' in os.environ:
            self.ibmcloud_api_key = os.environ['ibmcloud_api_key']
        else:
            raise Exception('Error: ibmcloud_api_key environment variable missing.')

        if 'ibmcloud_region' in os.environ:
            self.ibmcloud_region = os.environ['ibmcloud_region']
            if self.ibmcloud_region not in tags.region_timezones.keys():
                raise Exception(f'Error: ibmcloud_region {self.ibmcloud_region} has no valid timezone.')
        else:
            raise Exception('Error: ibmcloud_region environment variable missing.')

        if 'ibmcloud_vcfaas_site' in os.environ:
            self.ibmcloud_vcfaas_site = os.environ['ibmcloud_vcfaas_site']
        else:
            raise Exception('Error: ibmcloud_vcfaas_site environment variable missing.')
        
        # Get IBM Cloud Session Token
        ibm_iam_access_token = iam.request_ibm_iam_access_token(
            ibm_api_key=self.ibmcloud_api_key
        )

        # Get director site
        director_sites = vcfass.list_director_sites(
            ibm_iam_access_token=ibm_iam_access_token, region=self.ibmcloud_region
        )['director_sites']

        director_site = [d for d in director_sites if d.get('name') == self.ibmcloud_vcfaas_site][0]
        if not director_site:
            raise Exception(f'ERROR: Site not found: {self.ibmcloud_vcfaas_site}')

        # Get Director URL for the Site
        # Note: We assume we have at least 1 VDC which is always the case for multi-tenant sites

        vdcs = vcfass.list_vcfaas_vdcs(region = self.ibmcloud_region,ibm_iam_access_token=ibm_iam_access_token)['vdcs']
        vdc =  [v for v in vdcs if v['director_site']['id'] == director_site["id"]][0]
        self.director_url = urlparse(vdc['director_site']['url']).scheme + "://" + urlparse(vdc['director_site']['url']).netloc
        org = vdc['org_name']

        # Get VMware Access Token
        self.vmware_access_token = vcfass.get_vmware_access_token(
                                        ibm_iam_access_token = ibm_iam_access_token, 
                                        url = self.director_url,
                                        org = org)
        
    def dump(self):
        log.info(f'ibmcloud_region: {self.ibmcloud_region}')
        log.info(f'ibmcloud_vcfaas_site: {self.ibmcloud_vcfaas_site}')
        log.info(f'director_url: {self.director_url}')
        log.info(f'ibmcloud_api_key: <<Secret>>')
        log.info(f'ibm_api_key: <<Secret>>')
        log.info(f'vmware_access_token: <<Secret>>')

def vm_tag_update(ns, vm_tags_lock, env_lock):

    # Configuration update thread to update the Virtual Machine Metadata

    while True:
        log.info(f'----- Refreshing Virtual Machine Tags -------')

        vm_tags = []

        # Query all Virtual Machines

        try:
            log.info(f'Query all  Virtual Machines')
            filter = ""
            query_vms =  cloud_director.query_vm(director_url = ns.env.director_url, 
                                                vmware_access_token = ns.env.vmware_access_token, 
                                                filter = filter)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                log.error(e)
                log.info('Rehydrating tokens')
                with env_lock:
                    ns.env = Environment()
            else:
                log.error(f'Failed to query Virtual Machines')
                log.error(e)
            continue

        except Exception as e:
            log.error(f"Failed to query Virtual Machines")
            log.error(e)
            continue

        # Get metadata for all Relevant Virtual Machines

        vm_metadata = []
        log.info(f'Query Virtual Machines Metadata')
        for vm in query_vms:

            if vm["isVAppTemplate"]:
                log.debug(f'Skipped {vm["name"]} - VM is a VAPPTemplate')
                continue

            if vm["isInMaintenanceMode"]:
                log.debug(f'Skipped {vm["name"]} - VM in maintenance mode')
                continue

            if vm["isExpired"]:
                log.debug(f'Skipped {vm["name"]} - VM has expired')
                continue       

            try:
                filter = ""
                metadata = cloud_director.get_vm_metadata(href = vm["href"], vmware_access_token = ns.env.vmware_access_token)

                for metadata_entry in metadata["metadataEntry"]:
                    tag = tags.metadata_to_tag(metadata_entry, vm)

                    if len(tag) > 0:
                        vm_metadata.append(tag)

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    log.error(e)
                    log.info('Rehydrating tokens')
                    with env_lock:
                        ns.env = Environment()
                else:
                    log.error(f'Failed to query Virtual Machine Metadata')
                    log.error(e)
                continue

            except Exception as e:
                log.error(f"Failed to query Virtual Machine Metadata")
                log.error(e)
                continue

        with vm_tags_lock:
            ns.vm_tags = vm_metadata

        time.sleep(tag_update_pause)

    # os.kill(os.getpid(), signal.SIGUSR1)

def round_up(time: datetime, resolution):
    """
    Round up the time in minutes to the resolution
    """

    new_minute = ((time.minute // resolution) + 1 ) * resolution
    minute_delta = new_minute - time.minute
    new_time = time + timedelta(minutes = minute_delta)
    return new_time.replace(second=0, microsecond=0)

def round_down(time: datetime, resolution):
    """
    Round down the time in minutes to the resolution
    """

    new_minute = ((time.minute // resolution)) * resolution
    minute_delta = time.minute - new_minute
    new_time = time - timedelta(minutes = minute_delta)
    return new_time.replace(second=0, microsecond=0)

def main() -> int:

    
    # print('Starting Bugged Version')
    # print(datetime.now())
    # time.sleep(30)
    # print('  >>> crashed')
    # exit(1)
    

    # Check vars
    if resolution_window > 60:
        log.error('ERROR - Resolution window must be between 0-60')
        exit()
    elif (60 % resolution_window) != 0:
        log.error('ERROR - Resolution window must be a factor of 60')
        exit()

    # Register signal handler
    signal.signal(signal.SIGUSR1, signal_handler)

    # Initialise environment
    ns = SimpleNamespace()
    ns.env = Environment()
    ns.env.dump()

    # Initialise the Virtual Machine Metadata tags
    ns.vm_tags = []

    # Create locks 
    vm_tags_lock = threading.Lock()
    env_lock = threading.Lock()

    # Spawn the VDC Update Thread
    vm_tag_update_thread = threading.Thread(target=vm_tag_update, args=(ns, vm_tags_lock, env_lock))
    vm_tag_update_thread.start()

    # Main loop
    try:
        actions = {}
        while True:
            log.info(f'----- Start main processing loop -------')

            actions = []
            now = round_down(tags.get_now(ns.env.ibmcloud_region), resolution_window)

            # Build current actions list
            with vm_tags_lock:
                for tag in ns.vm_tags:
                    next = tags.next_exec(tag["value"], now)
                    delta = next - now
                    if (next != now):
                        if (now + timedelta(minutes = resolution_window)) >= next:
                            actions.append(tag)

            # Sleep to the end of the cycle
            now = tags.get_now(ns.env.ibmcloud_region)
            sleep_time = round_up(now, resolution_window) - now
            log.info(f'Number of Actions registered after next sleep - {len(actions)}')
            log.info(f'Sleeping for {sleep_time.seconds} seconds')
            time.sleep(sleep_time.seconds)

            # Rehydrate access tokens just in case
            log.info(f'Preparing to execute actions...')
            with env_lock:
                ns.env = Environment()

            # Run through actions list
            log.info(f'Executing {len(actions)} actions')
            for action in actions:
                try:
                    log.info(f'Processing Actions:')
                    log.info(f'    Name: {action["name"]}')
                    log.info(f'    Key: {action["key"]}')
                    log.info(f'    Value: {action["value"]}')
                    log.info(f'    href: {action["vm_href"]}')

                    #Get current status
                    filter = f'name=={action["name"]}'
                    query_vms =  cloud_director.query_vm(director_url = ns.env.director_url, 
                                                        vmware_access_token = ns.env.vmware_access_token, 
                                                        filter = filter)
                    status = query_vms[0]["status"]
            
                    if action["key"] == 'ibm.manage.up':
                        if status == 'POWERED_ON':
                            log.info(f'WARNING: Virtual Machine: {action["name"]} was already powered on')
                        else:
                            log.info(f'Powering on Virtual Machine: {action["name"]}')
                            task = cloud_director.powerOn(action["vm_href"], ns.env.vmware_access_token)
                    elif action["key"]== 'ibm.manage.down':
                        if status == 'POWERED_OFF':
                            log.info(f'WARNING: Virtual Machine: {action["name"]} was already powered off')
                        else:
                            log.info(f'Powering off Virtual Machine: {action["name"]}')
                            task = cloud_director.powerOff(action["vm_href"], ns.env.vmware_access_token)
                except Exception as e:
                    log.error(f'Failed to execute {action["key"]} on {action["vm_href"]}')
                    log.error(e)
                    continue

    except ExitCommand:
        pass

if __name__ == "__main__":
    exit(main())