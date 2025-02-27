# Data Handles Package

A simple Python package for data encryption, decryption, hashing, and MySQL database handling via sockets.

## Features
- **Encryption & Decryption**: AES, DES, 3DES, Blowfish, RC4
- **Hashing**: SHA-256, SHA-512, MD5
- **Socket-based MySQL handling**: CRUD operations without external MySQL connectors

## Installation
```bash
pip install data_handles
```

## Usage

### Encryption & Hashing
```python
from data_handles import crypto

# Hashing example
hashed_value = crypto("hash", "mydata", b"mykey", "SHA-256")

# Encryption example
encrypted_value = crypto("encrypt", "mydata", b"mykey", "AES")

# Decryption example
decrypted_value = crypto("decrypt", encrypted_value, b"mykey", "AES")
```

### MySQL Socket Handler
```python
from data_handles import MySQLSocketHandler

# Initialize handler
mysql_handler = MySQLSocketHandler("127.0.0.1", 3306)

# Create table
mysql_handler.create_table("users", ["id INT PRIMARY KEY", "name VARCHAR(100)"])

# Insert data
mysql_handler.insert("users", {"id": 1, "name": "John Doe"})

# Read data
print(mysql_handler.read_one("users", {"id": 1}))

# Update data
mysql_handler.update("users", {"name": "Jane Doe"}, {"id": 1})

# Delete data
mysql_handler.delete("users", {"id": 1})

# Close connection
mysql_handler.close()
```
