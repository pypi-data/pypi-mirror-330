import io
import json
from typing import Union, Optional

import PIL
import cairosvg
from PIL.Image import Image
from pydantic import BaseModel, Field
from tqdm import tqdm

from .. import SwitchAI
from ..utils import Task


def svg_to_pil(svg_data):
    png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    pil_image = PIL.Image.open(io.BytesIO(png_data))

    return pil_image


class Illustration(BaseModel):
    svg_code: str


class CriticResponse(BaseModel):
    need_improvement: bool
    instructions: Optional[str] = Field(
        ...,
        description="If an illustration requires improvement, "
        "provide clear and precise instructions on how to enhance it. "
        "The instructions should specify details such as shapes to remove, "
        "add, or modify, changes to colors, size adjustments, or any other "
        "specific alterations needed.",
    )


class Illustrator:
    """
    The Illustrator superclient generates illustrations based on text descriptions.

    Args:
        client: A chat SwitchAI client.
    """

    def __init__(self, client: SwitchAI):
        if Task.IMAGE_TEXT_TO_TEXT not in client.supported_tasks:
            raise ValueError("Illustrator requires a chat model that has the 'vision' capability.")

        self.author = client
        self.critic = client

    def generate_illustration(
        self,
        description: str,
        output_path: str,
        image_reference: Union[str, bytes, Image] = None,
        max_revision_steps: int = 0,
        editor_mode: bool = False,
    ):
        """
        Generates an illustration based on the given description and saves it to the specified output path.

        Args:
            description: The description of the illustration.
            output_path: The path where the illustration will be saved. The file format should be SVG.
            image_reference: An image reference to be used to generate the illustration.
            max_revision_steps: The maximum number of revision steps allowed to improve the illustration.
            If set to 0, no revisions will be made. Otherwise, the model will continue refining the
            illustration until it reaches the maximum number of revision steps or until the illustration
            is considered satisfactory.
            editor_mode: If True, allows the user to interactively edit the illustration.
        """

        if not output_path.endswith(".svg"):
            raise ValueError("The output file format should be SVG.")

        main_thread = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": description,
                    }
                ],
            }
        ]
        if image_reference:
            main_thread[0]["content"].append(
                {
                    "type": "image",
                    "image": image_reference,
                }
            )

        full_description = [description]

        response = self._generate_and_illustration(
            main_thread, full_description, image_reference, output_path, max_revision_steps
        )
        main_thread.append({"role": "assistant", "content": response})

        if editor_mode:
            while True:
                user_input = input("How would you like to change the illustration? (or CTRL+C to exit): ").strip()

                main_thread.append({"role": "user", "content": user_input})
                full_description.append(user_input)

                response = self._generate_and_illustration(
                    main_thread, full_description, image_reference, output_path, max_revision_steps
                )
                main_thread.append({"role": "assistant", "content": response})

        print(f"Illustration saved to: {output_path}")

    def _generate_and_illustration(
        self, messages, full_description, image_reference, output_path: str, max_revision_steps: int
    ):
        max_revision_steps += 1

        pbar = tqdm(desc="Working on illustration", unit="step")
        for _ in range(max_revision_steps):
            response = self.author.chat(messages=messages, response_format=Illustration)

            json_data = json.loads(response.message.content)
            svg = json_data["svg_code"]

            critic_messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"How to improve this illustration?"},
                        {"type": "image", "image": svg_to_pil(svg)},
                        {"type": "text", "text": "Objective: " + "\n".join(full_description)},
                    ],
                }
            ]
            if image_reference:
                critic_messages.append(
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Reference image used:"},
                            {"type": "image", "image": image_reference},
                        ],
                    }
                )

            critic_response = self.critic.chat(
                messages=critic_messages,
                response_format=CriticResponse,
            )
            critic_response = json.loads(critic_response.message.content)
            critic_response = CriticResponse.model_validate(critic_response)

            if not critic_response.need_improvement:
                break

            messages.append({"role": "assistant", "content": response.message.content})
            messages.append({"role": "user", "content": critic_response.instructions})

            pbar.update(1)

        try:
            with open(output_path, "w") as f:
                f.write(svg)
        except IOError as e:
            raise RuntimeError(f"Failed to write to file: {output_path}") from e

        return response.message.content
