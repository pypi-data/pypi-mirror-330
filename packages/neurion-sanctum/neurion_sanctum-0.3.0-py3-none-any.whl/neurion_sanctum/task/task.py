import os

import requests
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from typing import Callable
from pydantic import BaseModel, RootModel
from requests import Request


class Task:
    def __init__(self, *args, **kwargs):
        """Prevent instantiation of Task class."""
        raise RuntimeError("Use `Task.create_training_task` to create an Task server.")

    @classmethod
    def create_training_task(cls,train_handler: Callable[[str],None], upload_handler: Callable[[dict],None])->"Task":
        """
            Task Server to dynamically handle training and upload tasks.

        Args:
            train_handler (Callable): Function that processes training requests.
            upload_handler (Callable): Function that processes upload requests.
        """
        """Internal method to instantiate Ion (bypasses __init__)."""
        self = object.__new__(cls)  # Manually create instance

        self.port = 8000
        self.train_handler = train_handler
        self.upload_handler = upload_handler
        self.processor_ip = os.getenv("PROCESSOR_IP")
        self.request_id = int(os.getenv("REQUEST_ID"))

        self.app = FastAPI()
        self._setup_routes()

        return self

    def _train_task(self, key: str):
        """
        Background task for training with error handling.
        """
        try:
            print("Training started...")
            self.train_handler(key)  # Call the training function
            print("Training completed successfully!")
            requests.post(f"http://{self.processor_ip}:8000/{self.request_id}/completed")

        except Exception as e:
            print(f"Training failed: {str(e)}")
            requests.post(f"http://{self.processor_ip}:8000/{self.request_id}/failed", json={"error": str(e)})

    def verify_ip(self,request: Request):
        """
        Dependency function to check if the request is coming from an allowed IP.
        """
        client_ip = request.client.host  # Extract the request's IP address
        if client_ip != self.processor_ip:
            raise HTTPException(status_code=403, detail="Forbidden: Your IP is not allowed to access this resource.")
        return client_ip

    def _setup_routes(self):
        """Automatically register `/execute` with correct schemas."""
        @self.app.get("/health")
        def health_check():
            """Health check endpoint."""
            return {"status": "healthy"}

        class TrainInput(BaseModel):
            key: str

        @self.app.post("/train")
        async def train(trainInput: TrainInput, background_tasks: BackgroundTasks, client_ip: str = Depends(self.verify_ip)):
            """
            Asynchronous function to train a sentiment analysis model using a decrypted dataset.
            """
            print(f"Training started from IP: {client_ip}")
            background_tasks.add_task(self._train_task, trainInput.key)
            return {"status": "started", "message": "Training has started in the background."}

        @self.app.post("/upload")
        def upload(data: RootModel[dict[str, str]]):
            self.upload_handler(data.root)

    def start(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)