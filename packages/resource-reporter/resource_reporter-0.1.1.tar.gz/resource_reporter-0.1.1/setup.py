from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resource-reporter",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for monitoring and reporting resource usage in containerized applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resource-reporter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "psutil>=5.8.0",
        "google-cloud-pubsub>=2.0.0",
    ],
    extras_require={
        "gpu": ["pynvml>=11.0.0"],
    },
)
