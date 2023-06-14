import os
from typing import Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def _encrypt_file(file_path_from: str, file_path_to: str, key: bytes):
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor = cipher.encryptor()

    with open(file_path_to, 'wb') as file_to:
        file_to.write(nonce)

        with open(file_path_from, 'rb') as file_from:
            while True:
                piece = file_from.read(16)
                file_to.write(encryptor.update(piece))

                if len(piece) < 16:
                    break

            file_to.write(encryptor.finalize())


def _decrypt_file(file_path_from: str, file_path_to: str, key: bytes):

    with open(file_path_from, 'rb') as file_from:
        nonce = file_from.read(16)
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        decryptor = cipher.decryptor()
        with open(file_path_to, 'wb') as file_to:
            while True:
                piece = file_from.read(16)
                file_to.write(decryptor.update(piece))

                if len(piece) < 16:
                    break

            file_to.write(decryptor.finalize())


def encrypt_file(file_path_from: str, file_path_to: str, key: Union[bytes,
                                                                    str]):
    if type(key) is str:
        decoded_key = bytes.fromhex(key)
        _encrypt_file(file_path_from, file_path_to, decoded_key)
    if type(key) is bytes:
        _encrypt_file(file_path_from, file_path_to, key)


def decrypt_file(file_path_from: str, file_path_to: str, key: Union[bytes,
                                                                    str]):
    if type(key) is str:
        decoded_key = bytes.fromhex(key)
        _decrypt_file(file_path_from, file_path_to, decoded_key)
    if type(key) is bytes:
        _decrypt_file(file_path_from, file_path_to, key)


def generate_key(size: int = 16) -> bytes:
    return os.urandom(size)