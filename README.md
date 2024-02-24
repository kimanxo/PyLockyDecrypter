# PyLockyDecrypter
A Python tool for encrypting and decrypting files using Fernet cryptography and Typer.

## Overview

This tool provides functionalities to encrypt and decrypt files securely using Fernet encryption. It includes command-line interfaces for encrypting individual files, decrypting individual files, encrypting files recursively within a directory, and decrypting files recursively within a directory.

## Features

- Encrypt individual files
- Decrypt individual files
- Encrypt files recursively within a directory
- Decrypt files recursively within a directory

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kimanxo/PyLockyDecrypter.git
    ```

2. Navigate to the project directory:

    ```bash
    cd PyLockyDecrypter
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Encrypting a File

To encrypt a single file, use the following command:

```bash
python main.py encrypt --file <file_name> --output <output_file>
 ```

### Decrypting a File

To Decrypt a single file, use the following command:

```bash
python main.py decrypt --file <file_name>  --key <decryption_key>  --output <output_file>
```

### Encrypting Files Recursively

To encrypt all files within a directory recursively, use the following command:

```bash
python main.py encrypt_recursive <directory>
```



### Decrypting Files Recursively

To Decrypt all files within a directory recursively, use the following command:

```bash
python main.py decrypt_recursive <directory> --key <decryption_key>
```

## Note
Make sure to securely store your encryption keys. Losing the key will result in irreversible data loss.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
