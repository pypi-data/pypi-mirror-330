import json
import os
import subprocess
import time
import boto3
import paramiko

from neurion_sanctum.aws.docker import docker_build_and_push
from neurion_sanctum.aws.enclave import create_yaml_file


def setup_enclave(github_repo_url: str, processor_id:str,request_id:int):
    # build and push docker image
    image_name,full_image_path=docker_build_and_push(github_repo_url,processor_id,request_id)

    # Get the egress list as a string
    egress_str = os.getenv("AWS_ENCLAVE_ALLOWED_EGRESS")
    egress_list = egress_str.split(",") if egress_str else []
    egress_list.append(processor_id)

    # create enclave yaml file
    enclave_target,enclave_config_yaml_path=create_yaml_file(
        name=image_name,
        source=full_image_path,
        memory_mb=int(os.getenv("AWS_ENCLAVE_IMAGE_SIZE_IN_MB")),
        egress_list=egress_list
    )

    # create ec2 instance
    instance_id, public_ip = create_ec2()
    wait_for_ec2_ready(instance_id)

    # install enclaver
    install_enclaver(public_ip,enclave_target,enclave_config_yaml_path)


def create_ec2():
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_INSTANCE_TYPE = os.getenv("AWS_INSTANCE_TYPE")
    AWS_AMI=os.getenv("AWS_AMI")
    AWS_KEYPAIR_NAME =os.getenv("AWS_KEYPAIR_NAME")
    AWS_SECURITY_GROUP_NAME = os.getenv("AWS_SECURITY_GROUP_NAME")
    AWS_INSTANCE_EBS_SIZE_IN_GB = int(os.getenv("AWS_INSTANCE_EBS_SIZE_IN_GB"))


    # Initialize EC2 client
    ec2_client = boto3.client(
        "ec2",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    # Launch a t3.medium Nitro-enabled instance
    response = ec2_client.run_instances(
        ImageId=AWS_AMI,
        InstanceType=AWS_INSTANCE_TYPE,
        MinCount=1,
        MaxCount=1,
        KeyName=AWS_KEYPAIR_NAME,
        SecurityGroupIds=[AWS_SECURITY_GROUP_NAME],
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",  # The root volume for Amazon Linux 2
                "Ebs": {
                    "VolumeSize": AWS_INSTANCE_EBS_SIZE_IN_GB,  # Change this to the desired disk size (GB)
                    "VolumeType": "gp3",  # General Purpose SSD (gp3 is cheaper & better than gp2)
                    "DeleteOnTermination": True  # Delete volume when instance is terminated
                }
            }
        ],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": "Sanctum-Enclave"}]
            }
        ],
        EnclaveOptions={'Enabled': True}
    )

    instance_id = response["Instances"][0]["InstanceId"]
    print(f"Nitro Enclave EC2 instance started! Instance ID: {instance_id}")

    # Wait for the instance to be in 'running' state
    print("Waiting for instance to start...")
    waiter = ec2_client.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])

    # Retrieve the public IP
    instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = instance_info["Reservations"][0]["Instances"][0].get("PublicIpAddress")

    if public_ip:
        print(f"Public IP: {public_ip}")
    else:
        print("No public IP assigned. Ensure the instance is in a public subnet with auto-assign public IP enabled.")

    return instance_id, public_ip


def wait_for_ec2_ready(instance_id):
    """
    Waits for an EC2 instance to be fully running and have all status checks passed.
    """
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")

    # Initialize EC2 client
    ec2_client = boto3.client(
        "ec2",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    print(f"Waiting for instance {instance_id} to reach 'running' state...")

    # Wait until instance is in "running" state
    waiter = ec2_client.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is now 'running'.")

    # Wait until status checks are complete (both System and Instance status)
    print(f"⏳ Waiting for instance {instance_id} to pass all status checks...")
    while True:
        response = ec2_client.describe_instance_status(InstanceIds=[instance_id])

        if response["InstanceStatuses"]:
            instance_status = response["InstanceStatuses"][0]
            system_status = instance_status["SystemStatus"]["Status"]
            instance_status = instance_status["InstanceStatus"]["Status"]

            if system_status == "ok" and instance_status == "ok":
                print(f"Instance {instance_id} is fully initialized and ready!")
                break

        print(f"Instance {instance_id} is still initializing... Retrying in 10 seconds.")
        time.sleep(10)


def install_enclaver(public_ip, target,yaml_path):
    print(f"Connecting to EC2 {public_ip} via SSH...")
    """Uses SSH to install Docker on Amazon Linux 2."""
    SSH_KEY_PATH = os.getenv("AWS_KEYPAIR_NAME") + ".pem"
    SSH_USER = "ec2-user"  # Default user for Amazon Linux 2

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=public_ip, username=SSH_USER, key_filename=SSH_KEY_PATH, timeout=30)

        print("Installing Enclaver and Dependencies...")
        commands = [
            "sudo yum install --assumeyes aws-nitro-enclaves-cli aws-nitro-enclaves-cli-devel git",
            "sudo amazon-linux-extras install aws-nitro-enclaves-cli -y",
            f"sudo sed --in-place 's/memory_mib: 512/memory_mib: {os.getenv('AWS_ENCLAVE_IMAGE_SIZE_IN_MB')}/g' /etc/nitro_enclaves/allocator.yaml",
            "sudo systemctl enable --now nitro-enclaves-allocator.service",
            "sudo systemctl enable --now docker"
        ]

        # Execute setup commands
        for cmd in commands:
            print(f"Running: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode(errors="ignore"), stderr.read().decode(errors="ignore"))

        # Fetch Enclaver Download URL using Python
        print("Fetching latest Enclaver release URL...")
        enclaver_release_url = get_enclaver_download_url()
        if not enclaver_release_url:
            print("Error: Failed to fetch Enclaver release URL.")
            return

        # Download and Install Enclaver
        enclaver_install_commands = [
            f"curl -L -o enclaver.tar.gz {enclaver_release_url}",
            "tar --extract --verbose --file enclaver.tar.gz",
            "sudo install enclaver-linux-$(uname -m)-v*/enclaver /usr/bin"
        ]

        for cmd in enclaver_install_commands:
            print(f"Running: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode(errors="ignore"), stderr.read().decode(errors="ignore"))

        print("Installation completed successfully!")

        print("Enclave installation complete! Instance will reboot.")

        print(f"Uploading {yaml_path} to {yaml_path} on EC2...")
        sftp = ssh.open_sftp()
        sftp.put(yaml_path, yaml_path)
        sftp.close()
        print("YAML file copied successfully!")

        # Build enclave image and start enclave
        enclaver_image_commands = [
            f"sudo enclaver build --file  {yaml_path}",
            f"sudo enclaver run --publish 8000:8000 {target}"
        ]

        for cmd in enclaver_image_commands:
            print(f"Running: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode(errors="ignore"), stderr.read().decode(errors="ignore"))

        ssh.close()

    except Exception as e:
        print(f"SSH Connection Failed: {e}")


def get_enclaver_download_url():
    """
    Fetches the latest Enclaver release download URL from GitHub API.
    """
    try:
        # Get latest release JSON from GitHub
        response = subprocess.run(
            ["curl", "-s", "https://api.github.com/repos/edgebitio/enclaver/releases/latest"],
            capture_output=True,
            text=True
        )
        release_data = json.loads(response.stdout)

        # Find matching asset for the architecture
        for asset in release_data["assets"]:
            if asset["name"].startswith(f"enclaver-linux-{os.getenv('INSTANCE_ARCHITECTURE')}-") and asset["name"].endswith(".tar.gz"):
                return asset["browser_download_url"]

    except Exception as e:
        print(f"Error fetching Enclaver URL: {e}")

    return None

def destroy_ec2(instance_id):
    """
    Terminates an EC2 instance given its instance ID.
    """
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")

    # Initialize EC2 client
    ec2_client = boto3.client(
        "ec2",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    try:
        # Send terminate request
        print(f"Terminating instance {instance_id}...")
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])

        # Get current state
        state = response["TerminatingInstances"][0]["CurrentState"]["Name"]
        print(f"Instance {instance_id} is now {state}")

    except Exception as e:
        print(f"Error terminating instance: {e}")