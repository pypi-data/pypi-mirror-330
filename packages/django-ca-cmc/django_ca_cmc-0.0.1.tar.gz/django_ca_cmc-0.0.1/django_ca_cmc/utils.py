"""Utility functions, mostly for converting from/to cryptography/asn1crypto."""

from typing import cast

import asn1crypto.algos
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed448, ed25519, rsa
from django_ca.typehints import AllowedHashTypes


def _get_ec_signed_digest_algorithm(
    curve: ec.EllipticCurve,
) -> asn1crypto.algos.SignedDigestAlgorithm:
    # Helper function to get the digest algorithm for EC keys.
    if isinstance(curve, ec.SECP256R1):
        return asn1crypto.algos.SignedDigestAlgorithmId("sha256_ecdsa")
    elif isinstance(curve, ec.SECP384R1):
        return asn1crypto.algos.SignedDigestAlgorithmId("sha384_ecdsa")
    elif isinstance(curve, ec.SECP521R1):
        return asn1crypto.algos.SignedDigestAlgorithmId("sha512_ecdsa")
    else:
        # TODO: Support other curves
        raise ValueError(f"{curve.name}: Elliptic curve not supported.")


def get_signed_digest_algorithm(
    certificate: x509.Certificate,
) -> asn1crypto.algos.SignedDigestAlgorithm:
    """Get the ``asn1crypto.algos.SignedDigestAlgorithm`` of the given certificate."""
    # equivalent to signed_digest_algo() in
    # https://github.com/SUNET/pkcs11_ca/blob/main/tests/lib.py#L16
    algo = asn1crypto.algos.SignedDigestAlgorithm()
    if not isinstance(certificate, x509.Certificate):
        raise TypeError(f"{certificate}: Must be of type cryptography.x509.Certificate.")

    public_key = certificate.public_key()
    if isinstance(public_key, ed25519.Ed25519PublicKey):
        algo["algorithm"] = asn1crypto.algos.SignedDigestAlgorithmId("ed25519")
    elif isinstance(public_key, ed448.Ed448PublicKey):
        algo["algorithm"] = asn1crypto.algos.SignedDigestAlgorithmId("ed448")
    elif isinstance(public_key, ec.EllipticCurvePublicKey):
        algo["algorithm"] = _get_ec_signed_digest_algorithm(public_key.curve)
    elif isinstance(public_key, rsa.RSAPublicKey):
        algorithm = cast(AllowedHashTypes, certificate.signature_hash_algorithm)
        if isinstance(algorithm, hashes.SHA224):
            algo["algorithm"] = asn1crypto.algos.SignedDigestAlgorithmId("sha224_rsa")
        elif isinstance(algorithm, hashes.SHA256):
            algo["algorithm"] = asn1crypto.algos.SignedDigestAlgorithmId("sha256_rsa")
        elif isinstance(algorithm, hashes.SHA384):
            algo["algorithm"] = asn1crypto.algos.SignedDigestAlgorithmId("sha384_rsa")
        elif isinstance(algorithm, hashes.SHA512):
            algo["algorithm"] = asn1crypto.algos.SignedDigestAlgorithmId("sha512_rsa")
        else:
            raise ValueError(f"{algorithm.name}: Signature hash algorithm not supported.")
    else:
        # TODO: Add support for DSA
        raise ValueError(f"{public_key}: Public key type not supported.")

    return algo
