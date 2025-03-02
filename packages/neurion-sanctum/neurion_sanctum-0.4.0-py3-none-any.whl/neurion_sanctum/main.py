from neurion_sanctum.aws.docker import docker_build_and_push
from neurion_sanctum.processor.processor import Processor

if __name__ == "__main__":
    # Processor.new().start()
    docker_build_and_push("https://github.com/neurion-xyz/neurion-sanctum-task","23.233.238.5",1)