from setuptools import setup, find_packages

setup(
    name="one2x_sdk",
    version="0.0.16",
    author="Zhen",
    author_email="xiazhen@one2x.ai",
    description="A lightweight and efficient SDK for interacting with the One2X platform.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/one2x-ai/one2x_sdk",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
)
