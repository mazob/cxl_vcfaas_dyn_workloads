
#!/bin/bash

echo "################################################################################"
echo "Login to IBMCloud with CLI..."
echo "################################################################################"
echo

ibmcloud login -r $ibmcloud_region --apikey $ibmcloud_api_key -g $ibmcloud_resource_group

#ibmcloud target -g $ibmcloud_resource_group



### Stop

echo "################################################################################"
echo "Stopping a run..."
echo "################################################################################"
echo


ibmcloud ce project select  \
--name "$ce_jobname-project"


ibmcloud ce job delete \
--name $ce_jobname \