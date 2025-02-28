from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resource-reporter",
    version="0.1.3",
    author="QuangLe",
    author_email="joneyquang1997@gmail.com",
    description="A comprehensive monitoring library for real-time resource tracking and remote management of containerized applications with support for metrics reporting, asynchronous event notifications, and command listening via Google PubSub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resource-reporter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Development Status :: 4 - Beta",
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
    keywords="monitoring, resource, metrics, pubsub, containers, kubernetes, docker, reporting, distributed, cloud",
)
