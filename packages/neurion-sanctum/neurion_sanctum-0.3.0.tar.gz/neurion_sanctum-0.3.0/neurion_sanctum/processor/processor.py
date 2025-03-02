import secrets
import threading
import time

import requests
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from neurion_sanctum.aws.ec2 import setup_enclave
from neurion_sanctum.blockchain.message import process_dataset_usage_request
from neurion_sanctum.blockchain.query import get_pending_usage_requests


class Processor:
    def __init__(self, *args, **kwargs):
        """Prevent instantiation of Task class."""
        raise RuntimeError("Use `Processor.new` to create an Processor server.")

    @classmethod
    def new(cls)->"Processor":
        """
        Processor Server to dynamically handle training and upload tasks.
        """
        self = object.__new__(cls)  # Manually create instance

        self.port = 8000

        self.app = FastAPI()
        self._setup_routes()

        return self

    def get_public_ip(self):
        try:
            response = requests.get("https://api64.ipify.org?format=json")
            return response.json().get("ip")
        except requests.RequestException:
            return "Unable to fetch public IP"

    def _setup_routes(self):
        @self.app.get("/health")
        def health_check():
            """Health check endpoint."""
            return {"status": "healthy"}

        @self.app.post("/{request_id}/completed")
        async def training_completed(request_id: str):
            """
            Endpoint to be called when training is successfully completed.
            """
            # TODO: inform the user that the training is completed
            return {"status": "success", "message": f"Training {request_id} completed."}

        @self.app.post("/{request_id}/train")
        async def start_training(request_id: str):
            """
            Endpoint to be called to start training.
            """
            # TODO: check the API key and start training
            print(f"Training {request_id} started...")

        @self.app.post("/{request_id}/failed")
        async def training_failed(request_id: str, request: Request):
            """
            Endpoint to be called when training fails.
            Accepts any JSON format in the request body.
            Generates an API key to restart training.
            """
            failure_data = await request.json()  # Accept any random JSON format

            # TODO: generate a restart API key, we need to store this key somewhere
            api_key = secrets.token_hex(16)  # Generate a restart API key


            print(f"Training {request_id} failed: {failure_data}")
            print(f"Restart API Key generated: {api_key}")

            return {
                "status": "failed",
                "message": f"Training {request_id} failed.",
                "error": failure_data,
                "restart_api_key": api_key
            }

    def _background_task(self):
        """Background task that runs continuously."""
        while True:
            pending_usage_response=get_pending_usage_requests()
            for request in pending_usage_response.requests:
                print(f"Processing request: {request}")
                # start processing the request
                process_dataset_usage_request(request.id)
                # get the repository path
                url=request.training_repository
                my_ip=self.get_public_ip()
                setup_enclave(url,my_ip,request.id)
                print(f"Enclave setup for {url}")
                time.sleep(60)
            time.sleep(60)

    def start(self):
        """Start the FastAPI server and the background task."""
        print("Starting background task...")
        threading.Thread(target=self._background_task, daemon=True).start()

        print("Starting FastAPI server...")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)