import os
import sys
import tarfile
import tempfile
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def compress_to_tar(source_path: str, output_tar_path: str) -> None:
    if os.path.isfile(source_path):
        with tarfile.open(output_tar_path, 'w:gz') as tar:
            tar.add(source_path, arcname=os.path.basename(source_path))
    elif os.path.isdir(source_path):
        with tarfile.open(output_tar_path, 'w:gz') as tar:
            for item in os.listdir(source_path):
                item_path = os.path.join(source_path, item)
                tar.add(item_path, arcname=item)
    else:
        raise ValueError(f"Source path '{source_path}' is neither a file nor a directory")

def encrypt_file(input_file: str, output_file: str, password: str) -> None:
    salt = os.urandom(16)
    key = generate_key_from_password(password, salt)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(salt)
        f.write(encrypted_data)

def encrypt_compress(source_path: str, output_path: str, password: str) -> None:
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source path '{source_path}' does not exist")

    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as temp_tar:
        temp_tar_path = temp_tar.name

    try:
        print(f"Compressing '{source_path}'...")
        compress_to_tar(source_path, temp_tar_path)
        print(f"Encrypting to '{output_path}'...")
        encrypt_file(temp_tar_path, output_path, password)
        print("Operation completed successfully!")
    finally:
        if os.path.exists(temp_tar_path):
            os.remove(temp_tar_path)

def main():
    parser = argparse.ArgumentParser(
        description="Compress and encrypt a file or directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encrypt and compress a file
  python encrypt_compress.py "C:\\path\\to\\file.txt" "C:\\output\\encrypted.enc" "mypassword"

  # Encrypt and compress a directory
  python encrypt_compress.py "C:\\path\\to\\folder" "C:\\output\\encrypted.enc" "mypassword"
        """
    )
    parser.add_argument("source", help="Source file or directory path to encrypt and compress")
    parser.add_argument("output", help="Output encrypted file path (.enc)")
    parser.add_argument("password", help="Password for encryption")

    args = parser.parse_args()

    try:
        encrypt_compress(args.source, args.output, args.password)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
