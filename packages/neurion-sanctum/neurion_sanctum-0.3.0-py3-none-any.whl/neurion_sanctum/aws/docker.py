import os
import subprocess
import shutil

def is_docker_logged_in()->bool:
    """Checks if the user is logged into Docker."""
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        return True  # Logged in
    except subprocess.CalledProcessError:
        return False  # Not logged in


def modify_dockerfile(dockerfile_path: str, processor_ip: str, request_id: int):
    """
    Modifies a Dockerfile to inject PROCESSOR_IP and REQUEST_ID as environment variables.

    :param dockerfile_path: Path to the Dockerfile.
    :param processor_ip: The processor IP to be injected.
    :param request_id: The request ID to be injected.
    """
    env_lines = [
        f'ENV PROCESSOR_IP="{processor_ip}"\n',
        f'ENV REQUEST_ID="{request_id}"\n'
    ]

    with open(dockerfile_path, "r") as file:
        lines = file.readlines()

    # Find the index of the EXPOSE line
    insert_index = next(i for i, line in enumerate(lines) if line.strip().startswith("EXPOSE"))

    # Ensure proper formatting and insert ENV variables before EXPOSE
    modified_lines = lines[:insert_index] + env_lines + lines[insert_index:]

    # Write the modified Dockerfile
    with open(dockerfile_path, "w") as file:
        file.writelines(modified_lines)

    print(f"Dockerfile updated with PROCESSOR_IP={processor_ip} and REQUEST_ID={request_id}")



def docker_build_and_push(github_repo_url: str, processor_ip: str, request_id:int, tag: str = "latest")-> (str,str):
    """
    Clones a GitHub repo, builds a Docker image, and pushes it to a registry.
    Skips authentication if already logged in.
    """
    registry_url = "docker.io"
    username = os.getenv("DOCKER_USERNAME")

    # Extract repo owner and repo name
    repo_name = github_repo_url.split("/")[-1].replace(".git", "")
    repo_owner = github_repo_url.split("/")[-2]
    image_name = f"{repo_owner}_{repo_name}"

    # Clone the repository
    repo_dir = f"/tmp/{repo_name}"
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir, exist_ok=True)

    print(f"Cloning repository: {github_repo_url}")
    subprocess.run(["git", "clone", github_repo_url, repo_dir], check=True)

    # Check if Dockerfile exists
    dockerfile = os.path.join(repo_dir, "Dockerfile")
    if not os.path.exists(dockerfile):
        raise FileNotFoundError("Dockerfile not found in the repository.")

    modify_dockerfile(dockerfile, processor_ip, request_id)

    # Check if already logged into Docker
    def is_docker_logged_in():
        try:
            subprocess.run(["docker", "info"], check=True, capture_output=True)
            return True  # Logged in
        except subprocess.CalledProcessError:
            return False  # Not logged in

    if not is_docker_logged_in():
        print(f"Logging into {registry_url}...")
        subprocess.run(f'echo "{os.getenv('DOCKER_TOKEN')}" | docker login {registry_url} --username "{username}" --password-stdin',
                       shell=True, check=True)
    else:
        print("Already logged into Docker.")

    # Build the Docker image
    full_image_path = f"{username}/{image_name}:{tag}"
    print(f"Building Docker image: {full_image_path}")
    subprocess.run(["docker", "build", "-t", full_image_path, repo_dir], check=True)

    # Push the Docker image
    print(f"Pushing image: {full_image_path}")
    subprocess.run(["docker", "push", full_image_path], check=True)

    print(f"Successfully pushed {full_image_path} to {registry_url}")

    return image_name,full_image_path
