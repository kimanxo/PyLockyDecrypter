import os
import typer
from cryptography.fernet import InvalidToken, Fernet


class EncryptionTool:
    """A tool for encrypting and decrypting files using Fernet cryptography."""

    def __init__(self, key=None):
        """
        Initialize the EncryptionTool with a Fernet key.

        Args:
            key (str, optional): The encryption key. If not provided, a new key will be generated.
        """
        self.key = key if key else Fernet.generate_key().decode()

    def encrypt_file(self, file_name, output_file=None):
        """
        Encrypts a file using the Fernet key.

        Args:
            file_name (str): The name of the file to encrypt.
            output_file (str, optional): The name of the encrypted output file.
                Defaults to the original filename with a '.rex' extension.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            KeyError: If the key is invalid or not set.
            IOError: If an error occurs during file operations.
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File not found: {file_name}")

        with open(file_name, "rb") as file:
            file_data = file.read()

        try:
            fernet = Fernet(self.key.encode())
            encrypted_data = fernet.encrypt(file_data)
        except InvalidToken as e:
            raise KeyError(f"Invalid key: {e}") from e

        output_file = output_file or f"{file_name}.rex"
        with open(output_file, "wb") as file:
            file.write(encrypted_data)

        typer.echo(f"File encrypted successfully: {output_file}")

    def decrypt_file(self, file_name, output_file=None):
        """
        Decrypts a file using the Fernet key.

        Args:
            file_name (str): The name of the encrypted file to decrypt.
            output_file (str, optional): The name of the decrypted output file.
                Defaults to the original filename without the '.rex' extension.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            KeyError: If the key is invalid or not set.
            IOError: If an error occurs during file operations.
            InvalidToken: If the provided key is invalid.
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File not found: {file_name}")

        with open(file_name, "rb") as file:
            encrypted_data = file.read()

        try:
            fernet = Fernet(self.key.encode())
            decrypted_data = fernet.decrypt(encrypted_data)
        except InvalidToken as e:
            raise InvalidToken(f"Invalid key: {e}") from e

        output_file = output_file or os.path.splitext(file_name)[0]
        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        typer.echo(f"File decrypted successfully: {output_file}")


app = typer.Typer()


def encrypt(
    file_name: str = typer.Option(None, "--file", help="Specify the file name."),
    output_file: str = typer.Option(
        None, "--output", help="Specify the output file name."
    ),
):
    """
    Encrypts a file using a random Fernet-generated key and stores it securely for decryption.

    Args:
        file_name (str): The name of the file to encrypt.
        output_file (str, optional): The name of the encrypted output file.
            Defaults to the original filename with a '.rex' extension.
    """
    try:
        tool = EncryptionTool()
        tool.encrypt_file(file_name, output_file)
        with open("encryption_key.key", "wb") as key:
            key.write(tool.key.encode())
        typer.echo(
            f"File encrypted successfully with a random key. Store this key securely for decryption."
        )
    except (FileNotFoundError, KeyError, IOError) as e:
        typer.echo(f"Error: {str(e)}")


def decrypt(
    file_name: str = typer.Option(None, "--file", help="Specify the file name."),
    output_file: str = typer.Option(
        None, "--output", help="Specify the output file name."
    ),
    key: str = typer.Option(
        None, "--key", prompt=False, help="Specify the decryption key."
    ),
):
    """
    Decrypts a file using a provided key.

    Args:
        file_name (str): The name of the file to decrypt.
        output_file (str, optional): The name of the decrypted output file.
        key (str, optional): The decryption key.
    """
    try:
        if not key:
            typer.echo(
                "Error: Decryption key is required. Please provide the key using the --key option."
            )
            return
        tool = EncryptionTool(key)
        tool.decrypt_file(file_name, output_file)
    except (FileNotFoundError, KeyError, IOError, InvalidToken) as e:
        typer.echo(f"Error: {str(e)}")


def encrypt_recursive(
    directory: str = typer.Argument(
        ..., help="The directory containing the files to encrypt recursively."
    )
):
    """
    Encrypts all files within a directory recursively.

    Args:
        directory (str): The directory containing the files to encrypt recursively.
    """
    try:
        tool = EncryptionTool()
        root_folder = os.path.dirname(os.path.abspath(directory))
        encrypted_folder = os.path.join(root_folder, f"Encrypted_data")
        os.makedirs(
            encrypted_folder, exist_ok=True
        )  # Create "encrypted" folder if it doesn't exist
        for root, _, files in os.walk(directory):
            for file_name in files:
                if not file_name.endswith(".rex"):  # Skip files with ".rex" extension
                    file_path = os.path.join(root, file_name)
                    output_file = os.path.join(encrypted_folder, file_name + ".rex")
                    tool.encrypt_file(file_path, output_file)

        with open("encryption_key.key", "wb") as key:
            key.write(tool.key.encode())
        typer.echo(
            f"All files within directory encrypted successfully with a random key, stored securely for decryption."
        )
    except (FileNotFoundError, KeyError, IOError) as e:
        typer.echo(f"Error: {str(e)}")


def decrypt_recursive(
    directory: str = typer.Argument(
        ..., help="The directory containing the files to decrypt recursively."
    ),
    key: str = typer.Option(..., "--key", prompt=True, help="The decryption key."),
):
    """
    Decrypts all .rex files within a directory recursively.

    Args:
        directory (str): The directory containing the files to decrypt recursively.
        key (str): The decryption key.
    """
    try:
        tool = EncryptionTool(key)
        root_folder = os.path.dirname(os.path.abspath(directory))
        decrypted_folder = os.path.join(root_folder, "Decrypted_data")
        os.makedirs(
            decrypted_folder, exist_ok=True
        )  # Create "decrypted" folder if it doesn't exist
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".rex"):  # Decrypt only .rex files
                    file_path = os.path.join(root, file_name)
                    output_file = os.path.join(decrypted_folder, file_name[:-4])
                    tool.decrypt_file(file_path, output_file)
        typer.echo(f"All .rex files within directory decrypted successfully.")
    except (FileNotFoundError, KeyError, IOError, InvalidToken) as e:
        typer.echo(f"Error: {str(e)}")


if __name__ == "__main__":
    app.command()(encrypt)
    app.command()(decrypt)
    app.command()(encrypt_recursive)
    app.command()(decrypt_recursive)
    app()
