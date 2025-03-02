import os
import threading

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
        self.training_lock = threading.Lock()
        self.training_in_progress = False

        return self

    def _train_task(self, key: str):
        """
        Background task for training with error handling.
        """
        with self.training_lock:
            self.training_in_progress = True
        try:
            print("Training started...")
            self.train_handler(key)  # Call the training function
            print("Training completed successfully!")
            requests.post(f"http://{self.processor_ip}:8000/{self.request_id}/completed")

        except Exception as e:
            print(f"Training failed: {str(e)}")
            requests.post(f"http://{self.processor_ip}:8000/{self.request_id}/failed", json={"error": str(e)})

        finally:
            with self.training_lock:
                self.training_in_progress = False

    def _setup_routes(self):
        """Automatically register `/execute` with correct schemas."""
        @self.app.get("/health")
        def health_check():
            """Health check endpoint."""
            return {"status": "healthy"}

        class TrainInput(BaseModel):
            key: str

        @self.app.post("/train")
        async def train(trainInput: TrainInput, background_tasks: BackgroundTasks):
            """
            Asynchronous function to train a model using a decrypted dataset.
            If training is already in progress, return immediately.
            """
            with self.training_lock:
                if self.training_in_progress:
                    return {"status": "in_progress", "message": "Training is already ongoing. Please wait."}

            background_tasks.add_task(self._train_task, trainInput.key)
            return {"status": "started", "message": "Training has started in the background."}

        @self.app.post("/upload")
        def upload(data: RootModel[dict[str, str]]):
            self.upload_handler(data.root)

    def start(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)