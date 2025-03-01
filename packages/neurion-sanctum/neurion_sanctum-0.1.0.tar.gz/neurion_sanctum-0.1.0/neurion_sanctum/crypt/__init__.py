from cryptography.fernet import Fernet


def generate_key():
    """Generate AES encryption key and return as a string."""
    key = Fernet.generate_key()
    print(f"Generated Encryption Key: {key.decode()}")  # Print the key (to use later)
    return key


def encrypt_file(key, input_file, output_file):
    """Encrypt any file using the provided key."""
    cipher = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    encrypted_data = cipher.encrypt(data)

    with open(f"{output_file}.enc", "wb") as file:
        file.write(encrypted_data)

    print(f"File '{input_file}' encrypted and saved as '{output_file}'.")


def decrypt_file(key, encrypted_file,output_file):
    """Decrypt an encrypted file using the provided key."""
    cipher = Fernet(key)

    with open(encrypted_file, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    with open(output_file, "wb") as file:
        file.write(decrypted_data)

    print(f"File '{encrypted_file}' decrypted and saved as '{output_file}'.")


