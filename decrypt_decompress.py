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

def decrypt_file(input_file: str, output_file: str, password: str) -> None:
    with open(input_file, 'rb') as f:
        salt = f.read(16)
        encrypted_data = f.read()

    key = generate_key_from_password(password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        raise ValueError("Decryption failed. Wrong password or corrupted file.") from e

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

def decompress_tar(tar_path: str, output_dir: str) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=output_dir)

def decrypt_decompress(encrypted_file: str, output_path: str, password: str) -> None:
    if not os.path.exists(encrypted_file):
        raise FileNotFoundError(f"Encrypted file '{encrypted_file}' does not exist")

    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as temp_tar:
        temp_tar_path = temp_tar.name

    try:
        print(f"Decrypting '{encrypted_file}'...")
        decrypt_file(encrypted_file, temp_tar_path, password)
        print(f"Extracting to '{output_path}'...")
        decompress_tar(temp_tar_path, output_path)
        print("Operation completed decompressed successfully!")
    finally:
        if os.path.exists(temp_tar_path):
            os.remove(temp_tar_path)

def main():
    parser = argparse.ArgumentParser(
        description="Decrypt and decompress an encrypted file or directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decrypt and decompress to a directory
  python decrypt_decompress.py "C:\\path\\to\\encrypted.enc" "C:\\output\\folder" "mypassword"

  # Decrypt and decompress to current directory
  python decrypt_decompress.py "C:\\path\\to\\encrypted.enc" "." "mypassword"
        """
    )
    parser.add_argument("encrypted_file", help="Encrypted file path (.enc) to decrypt and decompress")
    parser.add_argument("output", help="Output directory path where files will be extracted")
    parser.add_argument("password", help="Password for decryption")

    args = parser.parse_args()

    try:
        decrypt_decompress(args.encrypted_file, args.output, args.password)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
