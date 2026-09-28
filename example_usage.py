from client import VRFSimulator

vrf = VRFSimulator("secret_validator_key_10200")
out, proof = vrf.evaluate("epoch_seed_42")

print(f"Generated Random Output: {out}")
print("Verification status:", VRFSimulator.verify(vrf.pk, "epoch_seed_42", out, proof))
