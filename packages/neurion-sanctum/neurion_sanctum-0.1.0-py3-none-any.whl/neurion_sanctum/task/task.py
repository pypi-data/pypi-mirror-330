import uvicorn
from fastapi import FastAPI, BackgroundTasks
from typing import Callable
from pydantic import BaseModel, RootModel



class Task:
    def __init__(self, *args, **kwargs):
        """Prevent instantiation of Task class."""
        raise RuntimeError("Use `Task.create_training_task` to create an Task server.")

    @classmethod
    def create_training_task(cls,train_handler: Callable, upload_handler: Callable)->"Task":
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

        self.app = FastAPI()
        self._setup_routes()

        return self

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
            Asynchronous function to train a sentiment analysis model using a decrypted dataset.
            """
            background_tasks.add_task(self.train_handler, trainInput.key)
            return {"status": "started", "message": "Training has started in the background."}

        @self.app.post("/upload")
        def upload(data: RootModel[dict[str, str]]):
            self.upload_handler(data.root)

    def start(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)