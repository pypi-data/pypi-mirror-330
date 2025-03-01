# Tenzro Store

Tenzro Store is a lightweight, modular, and extensible storage framework designed as the data layer for the Tenzro Ledger Framework. Inspired by RocksDB, it provides robust key-value storage for distributed ledger systems, using a custom `.tzds` (Tenzro Data Store) file format. It supports thread-safe operations and data replication, making it ideal for secure, scalable ledger applications.

## Key Features
- **Custom `.tzds` File Format**: Stores data in uniquely branded `.tzds` files, enhancing visibility and integration within the Tenzro ecosystem.
- **Thread-Safe Operations**: Ensures reliable concurrent access for multi-threaded applications.
- **Replication Support**: Seamlessly replicates data to follower nodes for redundancy and scalability.
- **JSON-Based Storage**: Uses JSON for flexible, human-readable data serialization.
- **No External Dependencies**: Lightweight and easy to integrate into any Python project.
- **Tenzro Ledger Integration**: Works as the storage backbone for Tenzro Trust and the broader Tenzro Ledger Framework.

## Installation

Install Tenzro Store via PyPI:
```bash
pip install tenzro-store
```

Or install from source:
```bash
git clone https://github.com/tenzro/tenzro-store.git
cd tenzro-store
pip install .
```

## Quick Start
Here's a basic example of using Tenzro Store:

```python
from tenzro_store import TenzroStore

# Initialize a store instance
store = TenzroStore(base_dir="ledger_data", node_id="node1")

# Store a transaction
transaction = {
    "transaction_id": "tx_123",
    "metadata": {"project": "test", "timestamp": "2025-02-28"},
    "payload": {"amount": 100, "currency": "USD"}
}
store.put("tx_123", transaction)

# Retrieve the transaction
data = store.get("tx_123")
print(f"Retrieved: {data}")

# Replicate to a follower node
store.replicate_to("follower_data")
```

This creates a `tx_123.tzds` file in the `ledger_data` directory and replicates it to `follower_data`.

## File Format
Tenzro Store uses the `.tzds` extension to store data as JSON files. Each file represents a key-value pair, where:
- **Key**: The filename (without `.tzds`)
- **Value**: The JSON content inside the file

Example `tx_123.tzds` content:
```json
{
    "transaction_id": "tx_123",
    "metadata": {"project": "test", "timestamp": "2025-02-28"},
    "payload": {"amount": 100, "currency": "USD"}
}
```

## Requirements
- Python 3.9 or higher
- No external dependencies

## Examples
Check out the `examples/` directory for more detailed usage:
- `basic_usage.py`: Demonstrates basic storage, retrieval, and replication.

Run the example:
```bash
python examples/basic_usage.py
```

## Testing
The package includes a comprehensive test suite. Run it with:
```bash
python -m unittest discover tests
```

Tests cover:
- Basic put/get operations
- Handling nonexistent keys
- Data replication
- Thread safety
- Edge cases like empty stores and invalid keys

## Contributing
We welcome contributions! Follow these steps:
1. Fork the repository: `https://github.com/tenzro/tenzro-store`
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add your feature'`
4. Push to GitHub: `git push origin feature/your-feature`
5. Open a Pull Request

Please include tests for new features and update documentation as needed.

## License
Distributed under the MIT License. See `LICENSE` for details.

## Part of Tenzro Ledger Framework
Tenzro Store is a core component of the Tenzro Ledger Framework, designed to work seamlessly with Tenzro Trust for hardware-rooted security and Tenzro Crypto. The `.tzds` file format provides a standardized way to store ledger data, making it easy to integrate with other Tenzro components.

## Development Status
- **Version**: 0.1.0 (Alpha)
- **Roadmap**:
  - Add compression for `.tzds` files
  - Implement batch operations
  - Add encryption support
  - Enhance replication with delta updates

## Contact
Maintained by [Hilal Agil] | [hilaal@gmail.com](mailto:hilaal@gmail.com)  
GitHub: [https://github.com/tenzro/tenzro-store](https://github.com/your-org/tenzro-store)