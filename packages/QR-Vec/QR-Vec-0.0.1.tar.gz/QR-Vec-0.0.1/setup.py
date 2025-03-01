from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="QR-Vec",
    version="0.0.1",
    description="QR code encode and decode functionality for embedding vectors.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/nickgerend/QR-Vec",
    author="Nick Gerend",
    author_email="nickgerend@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    install_requires=["numpy", "qrcode", "pyzbar", "pillow", "transformers", "torch"],
    include_package_data=True,
    package_data={'': ['data/*.csv']},
)