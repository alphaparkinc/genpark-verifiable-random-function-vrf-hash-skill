"""Verifiable Random Function (VRF) Engine.
100% Python Standard Library.
"""

import hashlib

class VRFSimulator:
    """Deterministic Verifiable Random Function generating output with proof."""
    def __init__(self, private_key="sk_vrf_default_9921"):
        self.sk = private_key
        self.pk = hashlib.sha256(private_key.encode("utf-8")).hexdigest()

    def evaluate(self, input_val):
        proof = hashlib.sha256(f"{self.sk}:{input_val}".encode("utf-8")).hexdigest()
        output = hashlib.sha256(proof.encode("utf-8")).hexdigest()
        return output, proof

    @staticmethod
    def verify(public_key, input_val, output, proof):
        expected_output = hashlib.sha256(proof.encode("utf-8")).hexdigest()
        return output == expected_output
