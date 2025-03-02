# Neurion Sanctum

## Overview
Neurion Sanctum provides a **secure, decentralized infrastructure** for AI model training and dataset usage requests. It allows users to securely train AI models while ensuring data privacy using **Trusted Execution Environments (TEE)**.

This library enables users to create and manage tasks, handling dataset usage requests seamlessly while abstracting the complexities of enclave execution and secure computing.

## Features
- **Task Management**: Users can start AI model training tasks with ease.
- **Secure Processing**: The processor securely handles dataset usage requests using **TEE-enabled AWS Nitro Enclaves**.
- **Automatic Model Upload**: Trained models are uploaded to storage solutions like **Hugging Face**.
- **Seamless Blockchain Integration**: Automates blockchain-based dataset access requests.

## Installation

Ensure you have **Python 3.8+** installed. Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Running a Training Task
Users can start a training task with the following:

```python
from neurion_sanctum.task.task import Task

def train_model(key: str):
    """
    Function to train a model using a secure dataset.
    """
    pass  # Implement your training logic here

def upload(data: dict):
    """
    Function to handle model uploads.
    """
    pass  # Implement your upload logic here

if __name__ == "__main__":
    Task.create_training_task(train_model, upload).start()
```

### Running the Processor
The processor handles dataset usage requests and manages enclave execution:

```python
from neurion_sanctum.processor.processor import Processor

if __name__ == "__main__":
    Processor.new().start()
```

The processor continuously checks for pending dataset usage requests and securely executes them within an enclave.

## Environment Variables
Ensure the following environment variables are set before running:

```sh
NEURION_PRIVATE_KEY=<private_key>
NEURION_MNEMONIC=<mnemonic>
NEURION_NETWORK=alphanet
AWS_ACCESS_KEY=<your_aws_access_key>
AWS_SECRET_KEY=<your_aws_secret_key>
AWS_REGION=us-east-1
AWS_INSTANCE_TYPE=c6a.2xlarge
AWS_AMI=<your_aws_ami>
AWS_SECURITY_GROUP_NAME=<your_security_group>
AWS_INSTANCE_EBS_SIZE_IN_GB=100
AWS_ENCLAVE_IMAGE_SIZE_IN_MB=10000
AWS_ENCLAVE_ALLOWED_EGRESS=huggingface.co,cdn-lfs-us-1.hf.co,hf-hub-lfs-us-east-1.*.amazonaws.com
DOCKER_USERNAME=<your_docker_username>
DOCKER_TOKEN=<your_docker_token>
```

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

For further information, refer to the documentation or open an issue in the repository.

