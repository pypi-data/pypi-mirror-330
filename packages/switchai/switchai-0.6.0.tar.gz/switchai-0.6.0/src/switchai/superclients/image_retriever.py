import importlib
import json
from pathlib import Path
from typing import Optional, Union, Dict

import numpy as np
from PIL import Image

from .. import SwitchAI
from ..utils import Task


class ImageRetriever:
    """
    A superclient to retrieve images similar to a query image or text.

    Args:
        client: A SwitchAI client that supports text and image embedding.
        images_folder_path: The path to the folder containing the images.
        embeddings_cache_path: The path to the embeddings cache file, else a file named 'embeddings_cache.json' will be created in the images folder.
        batch_size: The batch size to use when embedding images.
    """

    def __init__(
        self,
        client: SwitchAI,
        images_folder_path: str,
        embeddings_cache_path: Optional[str] = None,
        batch_size: Optional[int] = 32,
    ):
        if Task.IMAGE_TEXT_TO_EMBEDDING not in client.supported_tasks:
            raise ValueError("ImageRetriever requires a text and image embedding model.")

        self.client = client

        if embeddings_cache_path is None:
            embeddings_cache_path = f"{images_folder_path}/embeddings_cache_{client.provider}_{client.model_name}.json"
        embeddings_cache_path = Path(embeddings_cache_path)

        # Load embeddings from cache file
        self.embeddings = {}
        if embeddings_cache_path.exists():
            self.embeddings = json.loads(embeddings_cache_path.read_text())

        # Determine which images need to be embedded
        images_to_embed = []
        for image_path in Path(images_folder_path).glob("*.[pjPJ][pnNP][gG]"):
            if image_path.name not in self.embeddings:
                images_to_embed.append(image_path)

        # Embed the images
        for i in range(0, len(images_to_embed), batch_size):
            batch = images_to_embed[i : i + batch_size]

            pil_images = [Image.open(image_path) for image_path in batch]

            batch_embeddings = self.client.embed(pil_images).embeddings

            for embedding in batch_embeddings:
                image_path = batch[embedding.index]
                self.embeddings[image_path.name] = embedding.data

        # Save the embeddings to the cache file
        embeddings_cache_path.write_text(json.dumps(self.embeddings))

    def retrieve_images(
        self, query: Union[str, Image.Image], similarity_metric: str = "cosine", threshold: float = 0.5
    ) -> Dict[str, float]:
        """
        Retrieve images similar to the query image or text.

        Args:
            query: The query image or text.
            similarity_metric: The similarity metric to use. Must be 'cosine' or 'euclidean'.
            threshold: The similarity threshold.

        Returns:
            A sorted dictionary containing the image filenames as keys and the similarity scores as values.
        """
        if similarity_metric == "cosine":
            similarity_method = self._cosine_similarity
        elif similarity_metric == "euclidean":
            similarity_method = self._euclidean_distance
        else:
            raise ValueError("Similarity metric must be 'cosine' or 'euclidean'.")

        query_embedding = self.client.embed(query).embeddings[0].data

        results = {}
        for image_path, image_embedding in self.embeddings.items():
            similarity = similarity_method(query_embedding, image_embedding)
            if similarity >= threshold:
                results[image_path] = float(similarity)

        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        return results

    def _euclidean_distance(self, embedding1, embedding2):
        return np.linalg.norm(np.array(embedding1) - np.array(embedding2))

    def _cosine_similarity(self, embedding1, embedding2):
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
