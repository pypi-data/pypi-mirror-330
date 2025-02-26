from typing import Union

from multiformats import multicodec, multibase
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidKey


class Multikey:
    def __init__(
        self,
        id: str,
        controller: str,
        publicKeyMultibase: Union[
            ed25519.Ed25519PublicKey | rsa.RSAPublicKey, str
        ] = None,
        secretKeyMultibase: Union[
            ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey, str
        ] = None,
    ):
        self.id = id
        self.controller = controller
        self.publicKeyMultibase = (
            self.__load_public_key(publicKeyMultibase)
            if isinstance(publicKeyMultibase, str)
            else publicKeyMultibase
        )
        self.secretKeyMultibase = (
            self.__load_secret_key(secretKeyMultibase)
            if isinstance(secretKeyMultibase, str)
            else secretKeyMultibase
        )

    def dump_json(self):
        return {
            "type": "Multikey",
            "id": self.id,
            "controller": self.controller,
            "publicKeyMultibase": self.__encode_multibase(self.publicKeyMultibase),
            "secretKeyMultibase": self.__encode_multibase(self.secretKeyMultibase),
        }

    def __encode_multibase(self, key) -> str:
        if isinstance(key, rsa.RSAPublicKey):
            prefixed = multicodec.wrap(
                "rsa-pub",
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.PKCS1,
                ).hex(),
            )
        elif isinstance(key, rsa.RSAPublicKey):
            prefixed = multicodec.wrap(
                "ed25519-pub",
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw,
                ),
            )
        elif isinstance(key, rsa.RSAPrivateKey):
            prefixed = multicodec.wrap(
                "rsa-priv",
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.PKCS1,
                ).hex(),
            )
        elif isinstance(key, ed25519.Ed25519PrivateKey):
            prefixed = multicodec.wrap(
                "ed25519-priv",
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw,
                ),
            )
        else:
            raise Exception("Unknown Key: " + str(type(key)))
        return multibase.encode(prefixed, "base58btc")

    def __load_public_key(self, key):
        decoded = multibase.decode(key)
        codec, data = multicodec.unwrap(decoded)
        if codec.name == "ed25519-pub":
            try:
                return ed25519.Ed25519PublicKey.from_public_bytes(data)
            except InvalidKey:
                raise Exception("Invalid ed25519 public key passed.")
        elif codec.name == "rsa-pub":
            try:
                rsa.RSAPublicKey
                return serialization.load_der_public_key(data)
            except ValueError:
                raise Exception("Invalid rsa public key passed.")
        else:
            raise ValueError("Unsupported Codec: {}".format(codec.name))

    def __load_secret_key(self, key):
        decoded = multibase.decode(key)
        codec, data = multicodec.unwrap(decoded)
        if codec.name == "ed25519-priv":
            try:
                return ed25519.Ed25519PrivateKey.from_private_bytes(data)
            except InvalidKey:
                raise Exception("Invalid ed25519 private key passed.")
        elif codec.name == "rsa-priv":
            try:
                return serialization.load_der_private_key(data)
            except ValueError:
                raise Exception("Invalid rsa private key passed.")
        else:
            raise ValueError("Unsupported Codec: {}".format(codec.name))
