# dbay-client/README.md

# DBay Client

DBay is a Python client for interacting with the DBay web server. This client allows you to manage and control various modules such as `dac4D` and `dac16D` through a simple interface.

## Installation

To install the DBay client, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd dbay-client
pip install -e .
```

## Usage

To use the DBay client, you need to create an instance of the `DBay` class with the server address (IP address and port). The client will automatically call the `/full-state` endpoint to retrieve the current state of the server.

```python
from src.client import DBay

# Initialize the client with the server address
client = DBay("0.0.0.0", port=8345)

# Access the modules
modules = client.modules
```

## Modules

The client supports the following modules:

- **dac4D**: Represents a DAC4D module and includes methods for controlling its functionality.
- **dac16D**: Represents a DAC16D module and includes methods for controlling its functionality.
- **Empty**: Represents an empty module.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.