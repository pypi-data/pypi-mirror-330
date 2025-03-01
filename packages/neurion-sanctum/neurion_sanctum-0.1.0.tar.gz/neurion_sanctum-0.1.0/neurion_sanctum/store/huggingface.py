import os
import requests
from huggingface_hub.hf_api import HfApi, list_repo_files


def download_all_encrypted_files(repo_url, save_path="."):
    """
    Downloads all .enc files from the root directory of a Hugging Face dataset repository.

    :param repo_url: The full URL of the dataset repository (e.g., "https://huggingface.co/datasets/ryonzhang36/custom_dataset")
    :param save_path: The local directory where the files should be saved
    :return: List of downloaded file paths
    """
    # Extract the dataset repo ID from the URL
    repo_id = repo_url.replace("https://huggingface.co/datasets/", "").strip("/")

    # List all files in the repository
    files = list_repo_files(repo_id, repo_type="dataset")

    # Find all .enc files in the root directory (not in subfolders)
    enc_files = [f for f in files if f.endswith(".enc") and "/" not in f]  # Ensure it's in the root

    if not enc_files:
        raise FileNotFoundError("No .enc files found in the root directory of the dataset repository.")

    downloaded_files = []
    for enc_file in enc_files:
        file_url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{enc_file}"

        # Download the file
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        # Save the file locally
        local_file_path = os.path.join(save_path, enc_file)
        with open(local_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded '{enc_file}' from '{repo_url}' to '{local_file_path}'")
        downloaded_files.append(local_file_path)

    return downloaded_files

def upload_to_huggingface(file_list:list[str], repo_name:str, organization=None):
    """
    Uploads multiple encrypted dataset files to a Hugging Face dataset repository.

    :param file_list: List of file paths to upload
    :param repo_name: The name of the dataset repository on Hugging Face
    :param organization: (Optional) The organization under which to create the repo
    """

    # Get Hugging Face Token from environment
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN is not set in the environment.")

    # Initialize Hugging Face API
    api = HfApi()

    # Determine the full repository ID
    username = api.whoami(hf_token)["name"]
    repo_id = f"{organization}/{repo_name}" if organization else f"{username}/{repo_name}"

    print(f"Uploading files to Hugging Face dataset repository: {repo_id}")

    # Create a new dataset repository if it doesn't exist
    api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True, token=hf_token)

    # Iterate through each file and upload it
    for file_path in file_list:
        if not os.path.exists(file_path):
            print(f"Skipping '{file_path}': File does not exist.")
            continue

        file_name = os.path.basename(file_path)
        print(f"Uploading '{file_name}'...")

        api.upload_file(
            path_or_fileobj=file_path,  # Local file path
            path_in_repo=file_name,  # File name in Hugging Face dataset
            repo_id=repo_id,
            repo_type="dataset",
            token=hf_token
        )

        print(f"Successfully uploaded '{file_name}' to '{repo_id}'.")

    print("All files uploaded successfully!")

def upload_to_huggingface_with_token(file_list:list[str], repo_name:str, hf_token:str):
    """
    Uploads multiple encrypted dataset files to a Hugging Face dataset repository.

    :param file_list: List of file paths to upload
    :param repo_name: The name of the dataset repository on Hugging Face
    :param hf_token: Hugging Face API token
    """

    # Get Hugging Face Token from environment
    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN is not set.")

    # Initialize Hugging Face API
    api = HfApi()

    # Determine the full repository ID
    username = api.whoami(hf_token)["name"]
    repo_id = f"{username}/{repo_name}"

    print(f"Uploading files to Hugging Face dataset repository: {repo_id}")

    # Create a new dataset repository if it doesn't exist
    api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True, token=hf_token)

    # Iterate through each file and upload it
    for file_path in file_list:
        if not os.path.exists(file_path):
            print(f"Skipping '{file_path}': File does not exist.")
            continue

        file_name = os.path.basename(file_path)
        print(f"Uploading '{file_name}'...")

        api.upload_file(
            path_or_fileobj=file_path,  # Local file path
            path_in_repo=file_name,  # File name in Hugging Face dataset
            repo_id=repo_id,
            repo_type="dataset",
            token=hf_token
        )

        print(f"Successfully uploaded '{file_name}' to '{repo_id}'.")

    print("All files uploaded successfully!")