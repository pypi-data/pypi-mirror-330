# -*- encoding: utf-8 -*-

import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5


class Cipher:
    """
    A class for decrypting ciphertext using an RSA private key.

    This class takes a configuration dictionary containing ciphertext and a private key,
    decodes them from base64 to bytes, and provides a method to decrypt the ciphertext using the RSA private key.

    """

    _instance = None
    _cipher = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Cipher, cls).__new__(cls)
        return cls._instance

    def __init__(self, private_key: str):
        """
        Initialize the _Cipher class.
        """
        if self._cipher is None:
            private_key = base64.b64decode(private_key.encode('utf-8'))
            key = RSA.import_key(private_key)
            self._cipher = PKCS1_v1_5.new(key)

    def cipher_rsa_dec(self, ciphertext: str):
        """
        Decrypt the ciphertext using the RSA private key.

        Returns:
            bytes: The decrypted plaintext.
        """

        return self._cipher.decrypt(base64.b64decode(ciphertext.encode('utf-8')), None)
