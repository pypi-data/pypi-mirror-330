from ruamel.yaml import YAML

def create_yaml_file(name: str, source: str, memory_mb: int, egress_list: list)->(str,str):
    """
    Creates a YAML configuration file with the specified parameters.

    :param name: The name of the service.
    :param source: The source image reference.
    :param memory_mb: The default memory in MB.
    :param egress_list: A list of allowed egress domains.
    """
    file_path = f"{name}.yaml"
    target = f"{name}:latest"

    data = {
        "version": "v1",
        "name": name,
        "target": target,
        "sources": {
            "app": source
        },
        "defaults": {
            "memory_mb": memory_mb
        },
        "ingress": [
            {"listen_port": 8000}
        ],
        "egress": {
            "allow": egress_list
        }
    }

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)  # Ensures proper formatting

    with open(file_path, "w") as yaml_file:
        yaml.dump(data, yaml_file)

    print(f"YAML file '{file_path}' created successfully.")
    return target,file_path

# Example usage