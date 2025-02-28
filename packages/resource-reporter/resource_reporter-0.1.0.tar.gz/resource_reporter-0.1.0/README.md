# Resource Reporter

A Python library for monitoring and reporting resource usage in containerized applications, with support for asynchronous event reporting and command listening.

## Features

- Regular resource usage reporting (CPU, memory, network, GPU)
- Asynchronous event reporting
- Command listening via Google PubSub for remote control of containers
- Support for graceful shutdown and restart

## Installation

### Basic Installation

```bash
pip install resource-reporter