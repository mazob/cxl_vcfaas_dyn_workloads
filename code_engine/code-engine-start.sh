#!/bin/bash

echo "################################################################################"
echo "Login to IBMCloud with CLI..."
echo "################################################################################"
echo

ibmcloud login -r $ibmcloud_region --apikey $ibmcloud_api_key -g $ibmcloud_resource_group

#ibmcloud target -g $ibmcloud_resource_group



### Create a job

echo "################################################################################"
echo "Creating CE a job..."
echo "################################################################################"
echo

ibmcloud ce job create \
--name $ce_jobname \
--build-source ../scheduler \
--wait \
--mode daemon \
--env ibmcloud_region="$ibmcloud_region" \
--env ibmcloud_vcfaas_site="$ibmcloud_vcfaas_site" \
--env-from-secret ibmcloud-apikey-to-access-vcfaas

sleep 2

echo "################################################################################"
echo "Getting the CE job details..."
echo "################################################################################"
echo

ibmcloud ce job get \
--name $ce_jobname 

sleep 2

echo "################################################################################"
echo "Submit a CE jobrun..."
echo "################################################################################"
echo

ibmcloud ce jobrun submit  \
--name "$ce_jobname-run"  \
--job $ce_jobname

echo "################################################################################"
echo "Waiting for the container to start..."
echo "################################################################################"
echo

sleep 2

echo "Starting"

while ! [ $(ibmcloud ce jobrun get --name "$ce_jobname-run" --output json | jq '.instances[0].status.containerStatuses[0].started') ]
do 
  sleep 2
  echo -n "."
done
echo

echo
echo "################################################################################"
echo "Getting the CE jobrun details..."
echo "################################################################################"
echo

ibmcloud ce jobrun get \
--name "$ce_jobname-run"

sleep 2

echo "################################################################################"
echo "Follow STDIN log details..."
echo "################################################################################"
echo

ibmcloud ce jobrun logs -f \
--name "$ce_jobname-run"

