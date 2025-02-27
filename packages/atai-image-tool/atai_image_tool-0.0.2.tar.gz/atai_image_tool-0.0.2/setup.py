from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atai-image-tool",
    version="0.0.2",
    author="AtomGradient",
    author_email="alex@atomgradient.com",
    description="Extract text from images using OCR and save to JSON or print to console",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AtomGradient/atai-image-tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "easyocr",
    ],
    entry_points={
        "console_scripts": [
            "atai-image-tool=atai_image_tool.cli:main",
        ],
    },
)