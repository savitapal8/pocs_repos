import json
import subprocess
from tabulate import tabulate
import Services_Validations

def printvalidationerror(outputdict):
    errorlist = []
    successlist = []    
    
    ##Tenant Project Validation
    
    Services_Validations.validate_project("project_id",outputdict, errorlist, successlist)

    ##Shared Project Validation
    
    Services_Validations.validate_project("common_project_id",outputdict, errorlist, successlist)

    ##VPC Project Validation
    
    Services_Validations.validate_project("vpc_project_id",outputdict, errorlist, successlist)

    ##VPC Network Validation
    
    Services_Validations.validate_vpcnetwork("vpc_project_id", "vpc_network", outputdict, errorlist, successlist)

    ##VPC Subnet Validation

    Services_Validations.validate_subnetwork("vpc_project_id", "vpc_subnet", "region", outputdict, errorlist, successlist)

    ##Region Validation

    Services_Validations.validate_region("region",outputdict, errorlist, successlist)

    ##Worker Machine Validation

    Services_Validations.validate_machine_type("worker_machine_type", "region", outputdict, errorlist, successlist)

    ##KMS Keyring Validation

    Services_Validations.validate_keyring("common_project_id", "keyring", "keyring_location", outputdict, errorlist, successlist)

    ##KMS Key Validation

    Services_Validations.validate_kms_key("common_project_id", "keyring", "kms_keyname", "keyring_location", outputdict, errorlist, successlist)

    ##Dataflow Container Image Validation
    #Services_Validations.validate_df_container_image("dataflow_flex_container_image", outputdict, errorlist, successlist)
    
    ##Print Validation Result
    if len(successlist) > 0:
        print("List of validated resources successfully------------------\n")
        print(tabulate(successlist, headers=["Resource Id","Status"]))

    if len(errorlist) > 0:
        print("\n\nList of validation failed resources with error------------")
        print(tabulate(errorlist, headers=["Resource Id", "Error"]))
        


def main():
    f = open("../terraform.tfvars","r")
    output = f.readlines()
    outputdict = {}
    
    for i in range(0,len(output)):
        output[i] = output[i].replace("\n","").replace(" ","")
        
        if output[i].find("=") > 0:
            tempval = output[i].split("=")
            outputdict[tempval[0]] = tempval[1]

    ##Print Validation Errors   
    printvalidationerror(outputdict)
   
if __name__ == '__main__':
    main()

