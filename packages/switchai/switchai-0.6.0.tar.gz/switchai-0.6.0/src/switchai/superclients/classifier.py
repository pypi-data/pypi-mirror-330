import json
from enum import Enum
from typing import Union, List

from PIL.Image import Image
from pydantic import BaseModel, Field

from .. import SwitchAI
from ..utils import Task


class Classifier:
    """
    A superclient that extends a chat SwitchAI client to support classification tasks. It can be used to classify text or images.

    Args:
        client: A SwitchAI client initialized with a chat model.
        classes: The classes to classify the data into.
        task_description: A description of the classification task.
        multi_label: Whether the classifier should support multi-label classification or single-label classification.
    """

    def __init__(self, client: SwitchAI, classes: List[str], task_description: str = None, multi_label: bool = False):
        if (
            Task.TEXT_GENERATION not in client.supported_tasks
            and Task.IMAGE_TEXT_TO_TEXT not in client.supported_tasks
        ):
            raise ValueError("The classifier client only supports chat models.")

        self.client = client
        self.task_description = task_description

        ClassesType = Enum("ClassesType", {class_: class_ for class_ in classes}, type=str)
        if multi_label:
            self.ClassificationResult = type(
                "ClassificationResult",
                (BaseModel,),
                {
                    "__annotations__": {"class_name": List[ClassesType]},
                    "class_name": Field(...),
                    "__module__": __name__,
                },
            )
        else:
            self.ClassificationResult = type(
                "ClassificationResult",
                (BaseModel,),
                {
                    "__annotations__": {"class_name": ClassesType},
                    "class_name": Field(...),
                    "__module__": __name__,
                },
            )

    def classify(self, data: Union[str, Image, List[Union[str, Image]]]) -> Union[str, List[str]]:
        """
        Classifies the given data.

        Args:
            data: The data to classify.

        Returns:
            The classification result(s).
        """
        if isinstance(data, list):
            return [self._classify_single(item) for item in data]
        return self._classify_single(data)

    def _classify_single(self, data: Union[str, Image]) -> str:
        messages = self._create_messages(data)
        response = self.client.chat(messages=messages, response_format=self.ClassificationResult)
        return self._parse_response(response)

    def _create_messages(self, data: Union[str, Image]) -> List[dict]:
        messages = []
        if self.task_description:
            messages = [
                {
                    "role": "system",
                    "content": f"Your task is to classify data.\nTask description: {self.task_description}",
                }
            ]
        if isinstance(data, str):
            messages.append({"role": "user", "content": data})
            return messages
        elif isinstance(data, Image):
            messages.append({"role": "user", "content": [{"type": "image", "image": data}]})
            return messages
        else:
            raise ValueError("Unsupported data type for classification")

    def _parse_response(self, response: dict) -> str:
        try:
            return json.loads(response.message.content)["class_name"]
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise ValueError("Invalid response format") from e
