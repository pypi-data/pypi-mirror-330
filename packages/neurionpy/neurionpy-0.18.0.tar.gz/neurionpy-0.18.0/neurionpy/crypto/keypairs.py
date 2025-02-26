import base64
import hashlib
from typing import Callable, Optional, Union

import bech32
import coincurve
import ecdsa
from ecdsa.curves import Curve
from ecdsa.util import sigencode_string, sigencode_string_canonize

from neurionpy.crypto.interface import Signer


def _base64_decode(value: str) -> bytes:
    try:
        return base64.b64decode(value)
    except Exception as error:
        raise RuntimeError("Unable to parse base64 value") from error


class PublicKey:
    """Public key class."""

    curve: Curve = ecdsa.SECP256k1
    hash_function: Callable = hashlib.sha256

    def __init__(self, public_key: Union[bytes, "PublicKey", ecdsa.VerifyingKey]):
        """Initialize.

        :param public_key: butes, public key or ecdsa verifying key instance
        :raises RuntimeError: Invalid public key
        """
        if isinstance(public_key, bytes):
            self._verifying_key = ecdsa.VerifyingKey.from_string(
                public_key, curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(public_key, PublicKey):
            self._verifying_key = public_key._verifying_key
        elif isinstance(public_key, ecdsa.VerifyingKey):
            self._verifying_key = public_key
        else:
            raise RuntimeError("Invalid public key type")  # noqa

        self._public_key_bytes: bytes = self._verifying_key.to_string("compressed")
        self._public_key: str = base64.b64encode(self._public_key_bytes).decode()

    @property
    def public_key(self) -> str:
        """
        Get public key.

        :return: str public key.
        """
        return self._public_key

    @property
    def public_key_hex(self) -> str:
        """
        Get public key hex.

        :return: str public key hex.
        """
        return self.public_key_bytes.hex()

    @property
    def public_key_bytes(self) -> bytes:
        """
        Get bytes public key.

        :return: bytes public key.
        """
        return self._public_key_bytes

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        Verify message and signature.

        :param message: bytes message content.
        :param signature: bytes signature.
        :return: bool is message and signature valid.
        """
        success: bool = False

        try:
            success = self._verifying_key.verify(signature, message)

        except ecdsa.keys.BadSignatureError:
            ...

        return success

    def verify_digest(self, digest: bytes, signature: bytes) -> bool:
        """
        Verify digest.

        :param digest: bytes digest.
        :param signature: bytes signature.
        :return: bool is digest valid.
        """
        success: bool = False

        try:
            success = self._verifying_key.verify_digest(signature, digest)

        except ecdsa.keys.BadSignatureError:  # pragma: no cover
            ...

        return success

    def to_address(self, prefix: str = "neurion") -> str:
        """
        Converts a public key in hex format to a Cosmos SDK-compatible Bech32 address.

        :param public_key_hex: Hex-encoded public key (compressed format).
        :param prefix: Bech32 address prefix (default is "neurion").
        :return: Cosmos SDK-compatible address.
        """
        # Step 1: Decode hex public key into bytes
        public_key_bytes = bytes.fromhex(self.public_key_hex)

        # Step 2: Perform SHA-256 hash on public key
        sha256_hash = hashlib.sha256(public_key_bytes).digest()

        # Step 3: Perform RIPEMD-160 hash on the SHA-256 result
        ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()

        # Step 4: Encode into Bech32 format with "neurion" prefix
        address = bech32.bech32_encode(prefix, bech32.convertbits(ripemd160_hash, 8, 5))

        return address

    @staticmethod
    def from_signature(message: bytes, signature: bytes) -> "PublicKey":
        """
        Recover the public key from a signed message.

        :param message: The original message that was signed.
        :param signature: The 65-byte signature containing the recovery id.
        :return: The recovered PublicKey instance.
        """
        message_hash = hashlib.sha256(message).digest()
        recovered_key = coincurve.PublicKey.from_signature_and_message(signature, message_hash)
        return PublicKey(recovered_key.format(compressed=True))

    @staticmethod
    def from_signature_hex(message: str, signature_hex: str) -> "PublicKey":
        """
        Recover the public key from a signed message.

        :param message: The original message that was signed.
        :param signature: The 65-byte signature containing the recovery id.
        :return: The recovered PublicKey instance.
        """
        message = message.encode()
        message_hash = hashlib.sha256(message).digest()
        signature = bytes.fromhex(signature_hex)
        recovered_key = coincurve.PublicKey.from_signature_and_message(signature, message_hash)
        return PublicKey(recovered_key.format(compressed=True))


class PrivateKey(Signer):
    """Private key class."""

    curve: Curve = ecdsa.SECP256k1
    hash_function: Callable = hashlib.sha256

    def __init__(self, private_key: Optional[Union[bytes, str]] = None):
        """
        Initialize.

        :param private_key: bytes private key (optional, None by default).
        :raises RuntimeError: if unable to load private key from input.
        """
        if private_key is None:
            self._signing_key = ecdsa.SigningKey.generate(
                curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(private_key, bytes):
            self._signing_key = ecdsa.SigningKey.from_string(
                private_key, curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(private_key, str):
            raw_private_key = _base64_decode(private_key)
            self._signing_key = ecdsa.SigningKey.from_string(
                raw_private_key, curve=self.curve, hashfunc=self.hash_function
            )

        else:
            raise RuntimeError("Unable to load private key from input")

        # cache the binary representations of the private key
        self._private_key_bytes = self._signing_key.to_string()
        self._private_key = base64.b64encode(self._private_key_bytes).decode()

    @property
    def private_key(self) -> str:
        """
        Get private key.

        :return: str private key.
        """
        return self._private_key

    @property
    def private_key_hex(self) -> str:
        """
        Get private key hex.

        :return: str private key hex.
        """
        return self.private_key_bytes.hex()

    @property
    def private_key_bytes(self) -> bytes:
        """
        Get bytes private key.

        :return: bytes private key.
        """
        return self._private_key_bytes

    @property
    def public_key(self) -> PublicKey:
        """
        Get public key.

        :return: public key.
        """
        return PublicKey(self._signing_key.get_verifying_key())

    def sign(
        self, message: bytes, deterministic: bool = True, canonicalise: bool = True
    ) -> bytes:
        """
        Sign message.

        :param message: bytes message content.
        :param deterministic: bool is deterministic.
        :param canonicalise: bool is canonicalise.

        :return: bytes signed message.
        """
        sigencode = sigencode_string_canonize if canonicalise else sigencode_string
        sign_fnc = (
            self._signing_key.sign_deterministic
            if deterministic
            else self._signing_key.sign
        )

        return sign_fnc(message, sigencode=sigencode)

    def sign_recoverable(self, message: bytes) -> bytes:
        """
        Sign message using a recoverable signature.

        :param message: bytes message content.
        :return: bytes signed message.
        """
        message_hash = hashlib.sha256(message).digest()
        return coincurve.PrivateKey(self._private_key_bytes).sign_recoverable(message_hash)

    def sign_digest(
        self, digest: bytes, deterministic=True, canonicalise: bool = True
    ) -> bytes:
        """
        Sign digest.

        :param digest: bytes digest content.
        :param deterministic: bool is deterministic.
        :param canonicalise: bool is canonicalise.

        :return: bytes signed digest.
        """
        sigencode = sigencode_string_canonize if canonicalise else sigencode_string
        sign_fnc = (
            self._signing_key.sign_digest_deterministic
            if deterministic
            else self._signing_key.sign_digest
        )

        return sign_fnc(digest, sigencode=sigencode)
