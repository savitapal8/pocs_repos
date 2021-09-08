import os
import json
import subprocess
import docker

error_sub_message = "Please re-validate the "
success_sub_message = " validated successfully"

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE)
        return result.returncode
    except Exception as e:
        return e 


def run_command_output(command):
    try:
        result = os.popen(command)
        return result.read()
    except Exception as e:
        return e


def validate_project(field_name,op_dict, errorlist, successlist):
    val = op_dict[field_name].strip('"')
    cmd = f"gcloud projects describe {val} --format json".split()
    result = run_command(cmd)
    if result == 1:
          errorlist.append([op_dict[field_name].strip('"'), f"{error_sub_message}{field_name}"])
    else: 
          successlist.append([op_dict[field_name].strip('"'), f"{field_name}{success_sub_message}"])


def validate_region(field_name,op_dict, errorlist, successlist):
    val = op_dict[field_name].strip('"')
    cmd = f"gcloud compute regions describe {val} --format json".split()
    result = run_command(cmd)
    if result == 1:
          errorlist.append([op_dict[field_name].strip('"'), f"{error_sub_message}{field_name}"])
    else: 
          successlist.append([op_dict[field_name].strip('"'), f"{field_name}{success_sub_message}"])


def validate_vpcnetwork(vpc_projectid, vpc_network, op_dict, errorlist, successlist):
    val_projectid = op_dict[vpc_projectid].strip('"')
    val_vpcnetwork = op_dict[vpc_network].strip('"')
    
    cmd = f"gcloud compute networks describe {val_vpcnetwork} --project {val_projectid} --format json".split()
    result = run_command(cmd)

    if result == 1:
            errorlist.append([op_dict[vpc_network].strip('"'), f"{error_sub_message}{vpc_network}"])
    else: 
          successlist.append([op_dict[vpc_network].strip('"'), f"{vpc_network}{success_sub_message}"])


def validate_subnetwork(vpc_projectid, vpc_subnet, sn_region, op_dict, errorlist, successlist):
    inputVal = "vpc_project_id"
    val1 = op_dict[vpc_projectid].strip('"')

    inputVal = "vpc_subnet_region"
    val2 = op_dict[sn_region].strip('"')

    inputVal = "vpc_subnet"
    val = op_dict[vpc_subnet].strip('"')

    cmd = f"gcloud compute networks subnets describe {val} --project {val1} --region {val2} --format json".split()
    result = run_command(cmd)

    if result == 1:
            errorlist.append([op_dict[vpc_subnet].strip('"'), f"{error_sub_message}{vpc_subnet}"])
    else: 
          successlist.append([op_dict[vpc_subnet].strip('"'), f"{vpc_subnet}{success_sub_message}"])


def validate_machine_type(machine_type, region_name, op_dict, errorlist, successlist):
    val_machine_type = op_dict[machine_type].strip('"')
    val_region = op_dict[region_name].strip('"')
    
    cmd = f'gcloud compute zones list --filter="region={val_region}"  --format json'#.split()
    zone_result = run_command_output(cmd)
    zones = json.loads(zone_result)
    
    for i in range(0, len(zones)):
       cmd = f"gcloud compute machine-types describe {val_machine_type} --zone {zones[i]['name']} --format json".split()
       result = run_command(cmd)

       if result == 1:
            errorlist.append([val_machine_type, f"{machine_type} is not available for {zones[i]['name']}"])
       else: 
            successlist.append([val_machine_type, f"{machine_type} is available for {zones[i]['name']}"])


def validate_keyring(kr_projectid, kr_name, region, op_dict, errorlist, successlist):
    val = op_dict[kr_name].strip('"')
    val1 = op_dict[kr_projectid].strip('"')
    val2 = op_dict[region].strip('"')
    
    cmd = f"gcloud kms keyrings describe {val} --location={val2} --project={val1} --format json".split()
    result = run_command(cmd)

    if result == 1:
            errorlist.append([op_dict[kr_name].strip('"'), f"{error_sub_message}{kr_name}"])
    else: 
            successlist.append([op_dict[kr_name].strip('"'), f"{kr_name}{success_sub_message}"])


def validate_kms_key(kr_projectid, kr_name, key_name, region, op_dict, errorlist, successlist):
    val = op_dict[key_name].strip('"')
    val1 = op_dict[kr_projectid].strip('"')
    val2 = op_dict[region].strip('"')
    val3 = op_dict[kr_name].strip('"')
    
    cmd = f"gcloud kms keys describe {val} --keyring={val3} --location={val2} --project={val1} --format json".split()
    result = run_command(cmd)

    if result == 1:
            errorlist.append([op_dict[key_name].strip('"'), f"{error_sub_message}{key_name}"])
    else: 
            successlist.append([op_dict[key_name].strip('"'), f"{key_name}{success_sub_message}"])


def validate_df_container_image(container_image, op_dict, errorlist, successlist):
    client = docker.from_env()
    container = client.containers.get(op_dict[container_image].strip('"'))    
    print(container.attrs['Config']['Image'])
