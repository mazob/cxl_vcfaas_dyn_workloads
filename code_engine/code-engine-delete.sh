
#!/bin/bash


### Delete

echo "################################################################################"
echo "Login to IBMCloud with CLI..."
echo "################################################################################"
echo

ibmcloud login -r $ibmcloud_region --apikey $ibmcloud_api_key -g $ibmcloud_resource_group

echo
echo "################################################################################"
echo "Deleting a job and the project..."
echo "################################################################################"
echo


ibmcloud ce project select  \
--name "$ce_jobname-project"


ibmcloud ce job delete -f \
--name $ce_jobname

ibmcloud ce project delete -f \
--name "$ce_jobname-project" \
--hard

