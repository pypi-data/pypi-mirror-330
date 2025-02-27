from typing import Optional

from PIL import Image

from ..base_client import BaseClient
from ..types import ImageGenerationResponse, TranscriptionResponse
from ..utils import Task

from replicate.client import Client


SUPPORTED_MODELS = {
    "openai/whisper": [Task.AUDIO_TO_TEXT],
    "black-forest-labs/flux-schnell": [Task.TEXT_TO_IMAGE],
    "stability-ai/sdxl": [Task.TEXT_TO_IMAGE],
}

API_KEY_NAMING = "REPLICATE_API_TOKEN"


class ReplicateClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = Client(api_token=api_key)

    def generate_image(self, prompt: str, n: Optional[int] = 1) -> ImageGenerationResponse:
        latest_version_id = self.client.models.get(self.model_name).latest_version.id
        response = self.client.run(
            ref=f"{self.model_name}:{latest_version_id}",
            input={"prompt": prompt, "num_outputs": n, "output_format": "png"},
        )

        return ReplicateImageGenerationResponseAdapter(response)

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> TranscriptionResponse:
        latest_version_id = self.client.models.get(self.model_name).latest_version.id
        with open(audio_path, "rb") as audio_file:
            response = self.client.run(
                ref=f"{self.model_name}:{latest_version_id}",
                input={"audio": audio_file, "language": language if language else "auto"},
            )

        return ReplicateTranscriptionResponseAdapter(response)


class ReplicateTranscriptionResponseAdapter(TranscriptionResponse):
    def __init__(self, response):
        super().__init__(text=response["transcription"])


class ReplicateImageGenerationResponseAdapter(ImageGenerationResponse):
    def __init__(self, response):
        images = []
        for image_file in response:
            pil_image = Image.open(image_file)
            images.append(pil_image)

        super().__init__(images=images)
