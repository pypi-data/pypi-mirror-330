# SwitchAI

SwitchAI is a lightweight and flexible library that provides a standardized interface for interacting with various AI
APIs like OpenAI, Anthropic, Mistral, and more. With SwitchAI, you can easily switch between AI providers or use
multiple APIs simultaneously, all with a simple and consistent interface.

## Installation

To install SwitchAI, simply use pip:

```bash
pip install switchai
```

For more details, refer to the [installation guide](https://switchai.readthedocs.io/en/latest/installation.html).

## Getting Started

To use SwitchAI, you will need API keys for the AI providers you intend to interact with. You can set these keys either
as environment variables or pass them as configuration to the `SwitchAI` client.

### Option 1: In Code

```python
from switchai import SwitchAI

client = SwitchAI(provider="openai", model_name="gpt-4", api_key="your_api_key")
```

### Option 2: Environment Variables

Set the API key as an environment variable:

**macOS/Linux:**

```bash
export PROVIDER_API_KEY="your_api_key"
```

**Windows:**

```bash
set PROVIDER_API_KEY="your_api_key"
```

Make sure you follow the correct naming conventions for each provider's API key, as outlined in
the [documentation](https://switchai.readthedocs.io/en/latest/api_keys.html). This ensures that SwitchAI can
automatically detect and use the appropriate key for the chosen provider.

## Example Usage

Here are some examples of how you can use SwitchAI to interact with different AI models:

### Chat

```python
from switchai import SwitchAI

# Initialize the client with the desired AI model
client = SwitchAI(provider="openai", model_name="gpt-4o")

# Send a message and receive a response
response = client.chat(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

# Print the response
print(response)
```

### Vision

```python
from switchai import SwitchAI

# Initialize the client with the vision model
client = SwitchAI(provider="mistral", model_name="pixtral-large-latest")

# Send an image with a question and receive a response
response = client.chat(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image", "image": "path/to/image/file.jpg"},
            ],
        }
    ]
)

# Print the response
print(response)
```

### Text Embedding

```python
from switchai import SwitchAI

# Initialize the client with the chosen embedding model
client = SwitchAI(provider="google", model_name="models/text-embedding-004")

# Generate embeddings for a list of text inputs
response = client.embed(
    inputs=[
        "I am feeling great today!",
        "I am feeling sad today."
    ]
)

# Print the response
print(response)
```

### Speech to Text

```python
from switchai import SwitchAI

# Initialize the client with the desired speech-to-text model
client = SwitchAI(provider="deepgram", model_name="nova-2")

# Transcribe an audio file
response = client.transcribe(
    audio_path="path/to/audio/file.wav"
)

# Print the response
print(response)
```

### Image Generation

```python
from switchai import SwitchAI

client = SwitchAI(provider="replicate", model_name="black-forest-labs/flux-schnell")
response = client.generate_image("A beautiful sunset over the mountains.")

image = response.images[0]
image.show()
```

## SuperClients

SuperClients are high-level interfaces that extend the base `SwitchAI` client to provide additional functionalities.

### Browser

Gives a chat model the ability to access websites.

```python

from switchai import SwitchAI, Browser

client = SwitchAI(provider="openai", model_name="gpt-4o")
client = Browser(client)

response = client.chat(
    messages=[
        {
            "role": "user",
            "content": "Can you summarize the content of this website: https://example.com?"
        },
    ]
)

print(response)
```

### Classifier

Assigns a label to a text or image input.

```python
from switchai import SwitchAI, Classifier

client = SwitchAI(provider="openai", model_name="gpt-4o-mini")
classifier = Classifier(client, classes=["negative", "positive"])

response = classifier.classify("I am feeling great today!")
print(response)  # Output: "positive"
```

### Illustrator

Creates SVG illustrations using simple textual descriptions.

```python
from switchai import SwitchAI, Illustrator

client = SwitchAI(provider="openai", model_name="gpt-4o")

illustrator = Illustrator(client)
illustrator.generate_illustration(
    "Design a futuristic logo for my AI app with a sleek, modern aesthetic.",
    output_path="logo.svg",
)
```

### ImageRetriever

Retrieves images from a folder of images based on a query.

```python

from switchai import SwitchAI, ImageRetriever

client = SwitchAI(provider="VoyageAI", model_name="voyage-multimodal-3")
image_retriever = ImageRetriever(client, images_folder_path="files/images")

results = image_retriever.retrieve_images("An orange cat in a green field.")
print(results)
```

## Documentation

For full documentation, visit [SwitchAI Documentation](https://switchai.readthedocs.io/).

## Contributing

Contributions are always welcome! If you'd like to help enhance SwitchAI, feel free to make a contribution.
