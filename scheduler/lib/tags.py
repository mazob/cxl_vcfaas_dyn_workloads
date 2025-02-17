import os
import json

import dateutil.tz
from croniter import croniter
from datetime import datetime

import logging


log = logging.getLogger(__name__)

valid_tags = ['ibm.manage.up', 'ibm.manage.down']

region_timezones = {'eu-de': 'Europe/Berlin',
                    'us-south': 'America/Chicago',
                    'us-east': 'America/New_York',
                    'ca-tor': 'America/St_Johns',
                    'jp-tok': 'Asia/Tokyo'}

def is_tag(tag: str) -> bool:
    """
    Returns true if the tag is a registered tag.

    """

    return tag in valid_tags


def is_valid_tag(tag_content: str) -> bool:

    """
    Returns true if the contents of a tag is a valid croniter string

    """

    return croniter.is_valid(tag_content)

def is_valid_region(region: str) -> bool:

    """
    Returns true if the region is valid can be converted to a timezone

    """

    if region in region_timezones.keys():
        return True
    else:
        return False

def is_valid_cron(tag_content: str) -> bool:

    """
    Returns true if the contents of a tag is a valid croniter string

    """

    return croniter.is_valid(tag_content)

def get_now(region: str) -> datetime:
    """
    Returns current time for the region within a window

    """

    region_timezone = region_timezones[region]
    tz = dateutil.tz.gettz(region_timezone)
    return datetime.now(tz)

def next_exec(tag_content: str, now: datetime) -> int:

    """
    Returns the time of the next execution

    """

    return croniter(tag_content, now).get_next(datetime)

def metadata_to_tag(metadata: dict, vm: dict) -> dict:

    """
    Convert a director virtual machine metadata into a tag structure
    """

    tag = {}
    if is_tag(metadata["key"]):
        if not is_valid_cron(metadata["typedValue"]["value"]):
            log.error(f'ERROR: Tag: {metadata["key"]} Value: {metadata["typedValue"]["value"]} for VM {vm["name"]} is Invalid !!')
        else:
            log.info(f'Found Tag - VM: {vm["name"]}, Name: {metadata["key"]}, Value: {metadata["typedValue"]["value"]}')
            tag["key"] = metadata["key"]
            tag["value"] = metadata["typedValue"]["value"]
            tag["vm_href"] = vm["href"]
            tag["name"] = vm["name"]

    return tag
