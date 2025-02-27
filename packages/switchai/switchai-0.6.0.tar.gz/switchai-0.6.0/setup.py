from setuptools import setup, find_packages


deps = [
    "pydantic",
    "Pillow",
    "httpx",
    "numpy",
    "cairosvg",
    
    "openai",
    "mistralai",
    "anthropic",
    "google-generativeai",
    "deepgram-sdk",
    "voyageai",
    "replicate",
    "ollama"
]

extras = {}

setup(
    name="switchai",
    version="0.6.0",
    description="A unified library for interacting with various AI APIs through a standardized interface.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yassine El Boudouri",
    author_email="boudouriyassine@gmail.com",
    url="https://github.com/yelboudouri/SwitchAI",
    license="Apache 2.0 License",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=deps,
    extras_require=extras,
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
