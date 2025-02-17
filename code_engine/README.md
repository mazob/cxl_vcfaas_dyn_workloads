# Running VCFAAS Virtual Machine Scheduler on IBM Cloud Code engine

The VCFaaS Virtual Machine Scheduler will allow for scheduled start and stop of Virtual Machine resources to better manage resource consumption. The solution uses CRON logic where each VM running scheduler is TAGged with two metadata entries (`ibm.manager.up` and `ibm.manager.down`). The scheduler is a long running process and as such will run as a background task. This task should be managed by a watchdog to ensure its continued availability. TAG updates are made dynamically meaning the process needs never be stopped.

IBM Cloud® Code Engine is a fully managed, serverless platform that runs your containerized workloads, including web apps, micro-services, event-driven functions, or batch jobs. Code Engine even builds container images for you from your source code. In this example, we use [the scheduler python code](../scheduler/README.md) and we let the IBM Cloud® Code Engine to build a job which runs as a daemon.

## How to build the environment with IBM Cloud CLI

Create an API key for your account and change the other values to match your existing VCFAAS deployment and other IBM Cloud account settings.

Then modify the following environmental variables settings and export them in your shell before running the scripts:

```bash
export ibmcloud_api_key="***omitted***"
export ibmcloud_region="us-south"
export ibmcloud_vcfaas_site="IBM VCFaaS Multitenant - DAL"

export ibmcloud_resource_group="Default"

export ce_jobname="vcd-scheduler"
```

Three simple utility scripts (based on IBM Cloud CLI commands) located in this folder have been created for setting up the environment.

```bash
code-engine-create.sh
code-engine-stop.sh
code-engine-start.sh
code-engine-delete.sh
```

Note. Run the scripts from their own folder `code_engine`.

`code-engine-create.sh` will create a Code Engine project, build the job from the source code and creates a jobrun for it.

`code-engine-stop.sh` will delete the job and `code-engine-start.sh` will (re)build the job from the source code and creates a jobrun for it.

`code-engine-delete.sh` will delete the job and the project.


An example to create a VCFaaS Virtual Machine Scheduler Code Engine project:

```bash
% ./code-engine-create.sh 
################################################################################
Login to IBMCloud with CLI...
################################################################################

API endpoint: https://cloud.ibm.com
Authenticating...
OK

Targeted account IBM - IC4VS - Architecture (72cbd8dc47ae35c60c925005d212fdbc) <-> 1318041

Targeted resource group Default

Targeted region us-south

                  
API endpoint:     https://cloud.ibm.com
Region:           us-south
User:             sami.kuronen@fi.ibm.com
Account:          IBM - IC4VS - Architecture (72cbd8dc47ae35c60c925005d212fdbc) <-> 1318041
Resource group:   Default
################################################################################
Creating CE a project...
################################################################################

Creating project 'vcd-scheduler-project'...
ID for project 'vcd-scheduler-project' is '2053d54a-0f5a-4e24-bcf4-394df3c87e21'.
Waiting for project 'vcd-scheduler-project' to be active...
Now selecting project 'vcd-scheduler-project'.
OK
################################################################################
Creating CE a secret...
################################################################################

Creating generic secret 'ibmcloud-apikey-to-access-vcfaas'...
OK
################################################################################
Creating CE a job...
################################################################################

Creating job 'vcd-scheduler'...
Packaging files to upload from source path '../scheduler'...
Submitting build run 'vcd-scheduler-run-240906-103451345'...
Creating image 'private.us.icr.io/ce--72cbd-1li7ha093ghr/job-vcd-scheduler'...
Waiting for build run to complete...
Build run status: 'Running'
Build run completed successfully.
Run 'ibmcloud ce buildrun get -n vcd-scheduler-run-240906-103451345' to check the build run status.
OK                                                
################################################################################
Getting the CE job details...
################################################################################

Getting job 'vcd-scheduler'...
OK

Name:          vcd-scheduler  
ID:            6714fe65-348c-4e94-a3fa-8ae61bfb446c  
Project Name:  vcd-scheduler-project  
Project ID:    2053d54a-0f5a-4e24-bcf4-394df3c87e21  
Age:           63s  
Created:       2024-09-06T10:34:56+03:00  

Environment Variables:    
  Type                   Name                              Value  
  Secret full reference  ibmcloud-apikey-to-access-vcfaas    
  Literal                CE_API_BASE_URL                   https://api.us-south.codeengine.cloud.ibm.com  
  Literal                CE_PROJECT_ID                     2053d54a-0f5a-4e24-bcf4-394df3c87e21  
  Literal                CE_REGION                         us-south  
  Literal                ibmcloud_region                   us-south  
  Literal                ibmcloud_vcfaas_site              IBM VCFaaS Multitenant - DAL  
Image:                  private.us.icr.io/ce--72cbd-1li7ha093ghr/job-vcd-scheduler  
Resource Allocation:      
  CPU:     1  
  Memory:  4G  
Registry Secrets:         
  ce-auto-icr-private-us-south  

Runtime:              
  Mode:           daemon  
  Array Indices:  0  

Build Information:    
  Build Run Name:     vcd-scheduler-run-240906-103451345  
  Build Type:         local  
  Build Strategy:     buildpacks-medium  
  Timeout:            600  
  Source:             ../scheduler  
                      
  Build Run Summary:  Succeeded  
  Build Run Status:   Succeeded  
  Build Run Reason:   All Steps have completed executing  
  Run 'ibmcloud ce buildrun get -n vcd-scheduler-run-240906-103451345' for details.  
################################################################################
Submit a CE jobrun...
################################################################################

Getting job 'vcd-scheduler'...
Submitting job run 'vcd-scheduler-run'...
Run 'ibmcloud ce jobrun get -n vcd-scheduler-run' to check the job run status.
OK
################################################################################
Waiting for the container to start...
################################################################################

Starting


################################################################################
Getting the CE jobrun details...
################################################################################

Getting jobrun 'vcd-scheduler-run'...
Getting instances of jobrun 'vcd-scheduler-run'...
Getting events of jobrun 'vcd-scheduler-run'...
For troubleshooting information visit: https://cloud.ibm.com/docs/codeengine?topic=codeengine-troubleshoot-job.
Run 'ibmcloud ce jobrun events -n vcd-scheduler-run' to get the system events of the job run instances.
Run 'ibmcloud ce jobrun logs -f -n vcd-scheduler-run' to follow the logs of the job run instances.
OK

Name:          vcd-scheduler-run  
ID:            2623979f-1a38-4dd0-b817-74ca63729197  
Project Name:  vcd-scheduler-project  
Project ID:    2053d54a-0f5a-4e24-bcf4-394df3c87e21  
Age:           4s  
Created:       2024-09-06T10:36:04+03:00  

Job Ref:                vcd-scheduler  
Environment Variables:    
  Type                   Name                              Value  
  Secret full reference  ibmcloud-apikey-to-access-vcfaas    
  Literal                CE_API_BASE_URL                   https://api.us-south.codeengine.cloud.ibm.com  
  Literal                CE_PROJECT_ID                     2053d54a-0f5a-4e24-bcf4-394df3c87e21  
  Literal                CE_REGION                         us-south  
  Literal                ibmcloud_region                   us-south  
  Literal                ibmcloud_vcfaas_site              IBM VCFaaS Multitenant - DAL  
Image:                  private.us.icr.io/ce--72cbd-1li7ha093ghr/job-vcd-scheduler  
Resource Allocation:      
  CPU:                1  
  Ephemeral Storage:  400M  
  Memory:             4G  
Registry Secrets:         
  ce-auto-icr-private-us-south  

Runtime:      
  Mode:           daemon  
  Array Indices:  0  

Status:       
  Instance Statuses:    
    Running:  1  
  Conditions:         
    Type     Status  Last Probe  Last Transition  
    Pending  True    4s          4s  
             True    1s          1s  
    Running  True    1s          1s  

Events:       
  Type    Reason   Age              Source                Messages  
  Normal  Updated  2s (x7 over 5s)  batch-job-controller  Updated JobRun "vcd-scheduler-run"  

Instances:    
  Name                   Running  Status   Restarts  Age  
  vcd-scheduler-run-0-0  1/1      Running  0         5s  
################################################################################
Follow STDIN log details...
################################################################################

Getting logs for all instances of job run 'vcd-scheduler-run'...
Getting jobrun 'vcd-scheduler-run'...
Getting instances of jobrun 'vcd-scheduler-run'...
OK

vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:08 - INFO     - __main__ -  39 - Retrieving Environment....
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  86 - ibmcloud_region: us-south
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  87 - ibmcloud_vcfaas_site: IBM VCFaaS Multitenant - DAL
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  88 - director_url: https://dirw082.us-south.vmware.cloud.ibm.com
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  89 - ibmcloud_api_key: <<Secret>>
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  90 - ibm_api_key: <<Secret>>
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  91 - vmware_access_token: <<Secret>>
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ -  98 - ----- Refreshing Virtual Machine Tags -------
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ - 239 - ----- Start main processing loop -------
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ - 105 - Query all  Virtual Machines
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ - 256 - Number of Actions registered after next sleep - 0
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ - 257 - Sleeping for 107 seconds
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - __main__ - 130 - Query Virtual Machines Metadata
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - lib.tags -  90 - Found Tag - VM: test-cron-1, Name: ibm.manage.down, Value: 05 * * * *
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:36:12 - INFO     - lib.tags -  90 - Found Tag - VM: test-cron-1, Name: ibm.manage.up, Value: 00 * * * *
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:12 - INFO     - __main__ -  98 - ----- Refreshing Virtual Machine Tags -------
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:12 - INFO     - __main__ - 105 - Query all  Virtual Machines
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:13 - INFO     - __main__ - 130 - Query Virtual Machines Metadata
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:13 - INFO     - lib.tags -  90 - Found Tag - VM: test-cron-1, Name: ibm.manage.down, Value: 05 * * * *
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:13 - INFO     - lib.tags -  90 - Found Tag - VM: test-cron-1, Name: ibm.manage.up, Value: 00 * * * *
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:59 - INFO     - __main__ - 261 - Preparing to execute actions...
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:37:59 - INFO     - __main__ -  39 - Retrieving Environment....
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:04 - INFO     - __main__ - 266 - Executing 0 actions
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:04 - INFO     - __main__ - 239 - ----- Start main processing loop -------
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:04 - INFO     - __main__ - 256 - Number of Actions registered after next sleep - 0
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:04 - INFO     - __main__ - 257 - Sleeping for 115 seconds
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:13 - INFO     - __main__ -  98 - ----- Refreshing Virtual Machine Tags -------
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:13 - INFO     - __main__ - 105 - Query all  Virtual Machines
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:14 - INFO     - __main__ - 130 - Query Virtual Machines Metadata
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:14 - INFO     - lib.tags -  90 - Found Tag - VM: test-cron-1, Name: ibm.manage.down, Value: 05 * * * *
vcd-scheduler-run-0-0/vcd-scheduler: 2024-09-06 07:38:14 - INFO     - lib.tags -  90 - Found Tag - VM: test-cron-1, Name: ibm.manage.up, Value: 00 * * * *
```

The script will end by showing a continuos log of the scheduler. You can press ctrl + C to exit the log view. You can always return to logs with command `ibmcloud ce jobrun logs -f -n "$ce_jobname-run"`.

The job has been created as a daemon job, see [more in IBM Cloud Docs](https://cloud.ibm.com/docs/codeengine?topic=codeengine-job-daemon). With this mode, runs of the job do not time out and any failed instances are automatically restarted indefinitely. 

In this example, the job use the default size (1vCPU/4GB RAM/400M ephemeral storage) for the job, but you could tune this to be a smaller (e.g.`ibmcloud ce job update -n $ce_jobname --memory 0.5G --cpu 0.25 --ephemeral-storage 400M`), see [more about Supported memory and CPU combinations in IBM Cloud Docs](https://cloud.ibm.com/docs/codeengine?topic=codeengine-mem-cpu-combo). 

For example:

```bash
% ibmcloud ce job update -n $ce_jobname --memory 0.5G --cpu 0.25 --ephemeral-storage 400M
Updating job 'vcd-scheduler'...
OK

% ibmcloud ce job get -n $ce_jobname                                               
Getting job 'vcd-scheduler'...
OK

Name:          vcd-scheduler  
ID:            781b7232-1aa4-4043-ae17-c0df89f05ace  
Project Name:  vcd-scheduler-project  
Project ID:    4f5ebd42-8f22-4c16-88c1-fd89bc9a4bf1  
Age:           8m29s  
Created:       2024-09-06T10:58:10+03:00  

Last Job Run:         
  Name:     vcd-scheduler-run  
  Age:      4m25s  
  Created:  2024-09-06T11:02:14+03:00  

Environment Variables:    
  Type                   Name                              Value  
  Secret full reference  ibmcloud-apikey-to-access-vcfaas    
  Literal                CE_API_BASE_URL                   https://api.us-south.codeengine.cloud.ibm.com  
  Literal                CE_PROJECT_ID                     4f5ebd42-8f22-4c16-88c1-fd89bc9a4bf1  
  Literal                CE_REGION                         us-south  
  Literal                ibmcloud_region                   us-south  
  Literal                ibmcloud_vcfaas_site              IBM VCFaaS Multitenant - DAL  
Image:                  private.us.icr.io/ce--72cbd-1li6yej9f3cd/job-vcd-scheduler  
Resource Allocation:      
  CPU:                0.25  
  Ephemeral Storage:  400M  
  Memory:             500M  
Registry Secrets:         
  ce-auto-icr-private-us-south  

Runtime:              
  Mode:           daemon  
  Array Indices:  0  

Build Information:    
  Build Run Name:     vcd-scheduler-run-240906-10580594  
  Build Type:         local  
  Build Strategy:     buildpacks-medium  
  Timeout:            600  
  Source:             ../scheduler  
                      
  Build Run Summary:  Succeeded  
  Build Run Status:   Succeeded  
  Build Run Reason:   All Steps have completed executing  
  Run 'ibmcloud ce buildrun get -n vcd-scheduler-run-240906-10580594' for details.  

```


You can delete the scheduler project with:

```bash
% ./code-engine-delete.sh
################################################################################
Login to IBMCloud with CLI...
################################################################################

API endpoint: https://cloud.ibm.com
Authenticating...
OK

Targeted account IBM - IC4VS - Architecture (72cbd8dc47ae35c60c925005d212fdbc) <-> 1318041

Targeted resource group Default

Targeted region us-south

                  
API endpoint:     https://cloud.ibm.com
Region:           us-south
User:             sami.kuronen@fi.ibm.com
Account:          IBM - IC4VS - Architecture (72cbd8dc47ae35c60c925005d212fdbc) <-> 1318041
Resource group:   Default

################################################################################
Deleting a job and the project...
################################################################################
                     
Selecting project 'vcd-scheduler-project'...
OK
Deleting job 'vcd-scheduler'...
OK
Deleting project 'vcd-scheduler-project'...
OK

```

You can check the script content to see more details how the Code Engine project, job and jobruns are built with IBM Cloud CLI.

