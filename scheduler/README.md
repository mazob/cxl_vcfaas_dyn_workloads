# VCFAAS Virtual Machine Scheduler

## Description

The VCFaaS Virtual Machine Scheduler will allow for scheduled start and stop of Virtual Machine resources to better manage resource consumption. For example a customer may require:

- Shut down testing resources over the weekend.
- Shut down testing resources between 8pm and 6am each week night.

## Requirements

### Python

- Version 3.8 +
- pip install -r requirements.txt

### Environment Variables

The following environment variables are required to run the scheduler.

- **ibmcloud_api_key**: IBM Cloud API Key
- **ibmcloud_region**: IBM Cloud Region (eg en-de)
- **ibmcloud_vcfaas_site**: The Director Site to target (eg IBM VCFaaS Multitenant - FRA)

### Execution

The scheduler is a long running process and as such will run as a background task. This task should be managed by a watchdog to ensure its continued availability. TAG Updates are made dynamically meaning the process needs never be stopped.

For example:

```
python vmscheduler.py

2024-09-01 09:19:08 - INFO     - __main__ -  39 - Retrieving Environment....
2024-09-01 09:19:08 - DEBUG    - lib.iam -  41 - Request IBM Cloud IAM access token.
2024-09-01 09:19:08 - DEBUG    - urllib3.connectionpool - 1014 - Starting new HTTPS connection (1): iam.cloud.ibm.com:443
2024-09-01 09:19:09 - DEBUG    - urllib3.connectionpool - 473 - https://iam.cloud.ibm.com:443 "POST /identity/token HTTP/1.1" 200 1132
2024-09-01 09:19:09 - DEBUG    - lib.iam -  44 - Got IBM Cloud IAM access token: eyJraWQ(...)
2024-09-01 09:19:09 - DEBUG    - lib.vcfass -  40 - Request VCFaaS Director sites.
2024-09-01 09:19:09 - DEBUG    - urllib3.connectionpool - 1014 - Starting new HTTPS connection (1): api.eu-de.vmware.cloud.ibm.com:443
2024-09-01 09:19:11 - DEBUG    - urllib3.connectionpool - 473 - https://api.eu-de.vmware.cloud.ibm.com:443 "GET /v1/director_sites HTTP/1.1" 200 2159
2024-09-01 09:19:11 - DEBUG    - lib.vcfass -  43 - Got 1 VCFaaS Director sites.
2024-09-01 09:19:11 - DEBUG    - lib.vcfass - 102 - Retrieving list of VDC

```

Cron Format testing may be checked with the cron_test utility. For example:

```
python test_cron.py '*/3 * * * *' us-south
region valid
cron string valid
Current time in region us-south : 2024-08-31 18:34:14.771798-05:00
Next execution time - 2024-08-31 18:36:00-05:00
```

## TAG Population

Tagging is done at the Virtual Machine level and is realized through the use of *Virtual Machine Metadata* configured through the VMware Cloud Director console.

Current tags are as follows:

- ibm.manage.up: Start a virtual machine
- ibm.manage.down: Stop a virtual machine

Tag values indicate a series of time events described in the crontab format. A reasonable reference for this can be found here -> [https://crontab.guru](https://crontab.guru)
