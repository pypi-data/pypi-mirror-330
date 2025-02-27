# zmbus-sdk

A Python SDK for interacting with Zima Sabus systems.

## Installation

```bash
pip install zmbus-sdk
```

## Usage

```python
from zimasabus_sdk import zmsystem

# Initialize the client
client = zmsystem.ZMSystem(
    api_key="your_api_key",
    base_url="https://api.example.com"
)

# Use the client to interact with the API
response = client.some_method()
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Development

This project uses Poetry for dependency management.

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## License

MIT
