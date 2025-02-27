from typing import Union, List

import voyageai
from PIL.Image import Image

from ..base_client import BaseClient
from ..types import EmbeddingResponse, EmbeddingUsage, Embedding
from ..utils import Task

SUPPORTED_MODELS = {
    "voyage-3-large": [Task.TEXT_TO_EMBEDDING],
    "voyage-3": [Task.TEXT_TO_EMBEDDING],
    "voyage-3-lite": [Task.TEXT_TO_EMBEDDING],
    "voyage-code-3": [Task.TEXT_TO_EMBEDDING],
    "voyage-finance-2": [Task.TEXT_TO_EMBEDDING],
    "voyage-law-2": [Task.TEXT_TO_EMBEDDING],
    "voyage-code-2": [Task.TEXT_TO_EMBEDDING],
    "voyage-multimodal-3": [Task.IMAGE_TEXT_TO_EMBEDDING],
}

API_KEY_NAMING = "VOYAGE_API_KEY"


class VoyageaiClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = voyageai.Client(api_key=api_key)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        if Task.TEXT_TO_EMBEDDING in SUPPORTED_MODELS[self.model_name]:
            response = self.client.embed(inputs, model=self.model_name)
        else:
            if isinstance(inputs, str) or isinstance(inputs, Image):
                inputs = [[inputs]]
            else:
                inputs = [inputs]

            response = self.client.multimodal_embed(inputs, model=self.model_name)

        return VoyageaiEmbeddingResponseAdapter(response)


class VoyageaiEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=response.text_tokens,
                total_tokens=response.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=index,
                    data=data,
                )
                for index, data in enumerate(response.embeddings)
            ],
        )
