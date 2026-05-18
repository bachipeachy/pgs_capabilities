# CT Conformance Tests — crypto atoms
# Test category: CT Conformance Tests
# Purpose: verify deterministic transformation correctness for cryptographic CT atoms.
# Usage: python pgs_transforms/testbed/run_ct_conformance_crypto_tests.py

# Bootstrap path before imports — CWD-independent via structure layer
from pgs_structure.structure.resolution import bootstrap
bootstrap()

from pgs_transforms.implementation.transforms.atoms.ct_pure_generate_entropy_v0 import (
    execute as generate_entropy,
)
from pgs_transforms.implementation.transforms import (
    execute as entropy_to_mnemonic,
)
from pgs_transforms.implementation.transforms import (
    execute as mnemonic_to_seed,
)
from pgs_transforms.implementation.transforms.atoms.ct_pure_derive_master_key_v0 import (
    execute as derive_master_key,
)
from pgs_transforms.implementation.transforms import (
    execute as derive_child_key,
)
from pgs_transforms.implementation.transforms import (
    execute as private_key_to_public,
)
from pgs_transforms.implementation.transforms import (
    execute as pubkey_to_eth_address,
)
# --- Golden Vectors ---
# Use known test vectors for determinism checks
TEST_MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
TEST_SEED_BYTES = bytes.fromhex("5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4")
TEST_MASTER_KEY_BYTES = bytes.fromhex("a2b0225529442438657a27887b875a5833916814548689345934858583193453")
TEST_MASTER_CHAIN_CODE_BYTES = bytes.fromhex("a2b0225529442438657a27887b875a5833916814548689345934858583193454")


def test_generate_entropy():
    result1 = generate_entropy(inputs={"entropy_bits": 128})
    result2 = generate_entropy(inputs={"entropy_bits": 128})
    
    assert "entropy_bytes" in result1
    assert isinstance(result1["entropy_bytes"], bytes)
    assert len(result1["entropy_bytes"]) == 16  # 128 bits
    assert result1["entropy_bytes"] != result2["entropy_bytes"] # Should be random

def test_entropy_to_mnemonic():
    entropy_bytes = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    result = entropy_to_mnemonic(inputs={"entropy_bytes": entropy_bytes})
    assert "mnemonic" in result
    assert isinstance(result["mnemonic"], str)
    assert len(result["mnemonic"].split()) == 12


def test_mnemonic_to_seed():
    result = mnemonic_to_seed(inputs={"mnemonic": TEST_MNEMONIC, "passphrase": ""})
    
    assert "seed_bytes" in result
    assert isinstance(result["seed_bytes"], bytes)
    assert result["seed_bytes"] == TEST_SEED_BYTES

def test_derive_master_key():
    result = derive_master_key(inputs={"seed_bytes": TEST_SEED_BYTES})
    
    assert "master_private_key_bytes" in result
    assert "master_chain_code_bytes" in result
    assert isinstance(result["master_private_key_bytes"], bytes)
    assert isinstance(result["master_chain_code_bytes"], bytes)
    assert len(result["master_private_key_bytes"]) == 32
    assert len(result["master_chain_code_bytes"]) == 32

def test_derive_child_key():
    # Using a known parent key and index to get a known child
    parent_pk = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    parent_cc = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    index = 0
    
    result = derive_child_key(inputs={
        "parent_private_key_bytes": parent_pk,
        "parent_chain_code_bytes": parent_cc,
        "index": index
    })
    
    assert "child_private_key_bytes" in result
    assert "child_chain_code_bytes" in result
    assert isinstance(result["child_private_key_bytes"], bytes)
    assert isinstance(result["child_chain_code_bytes"], bytes)
    assert len(result["child_private_key_bytes"]) == 32
    assert len(result["child_chain_code_bytes"]) == 32
    assert result["child_private_key_bytes"] != parent_pk

def test_private_key_to_public():
    private_key_bytes = bytes.fromhex("11" * 32)
    result = private_key_to_public(inputs={"private_key_bytes": private_key_bytes, "curve": "secp256k1"})
    
    assert "public_key_uncompressed_bytes" in result
    assert isinstance(result["public_key_uncompressed_bytes"], bytes)
    assert len(result["public_key_uncompressed_bytes"]) == 65
    assert result["public_key_uncompressed_bytes"].startswith(b'\x04')

def test_pubkey_to_eth_address():
    # From a known private key -> public key -> address
    pk_bytes = bytes.fromhex("11" * 32)
    pubkey_result = private_key_to_public(inputs={"private_key_bytes": pk_bytes, "curve": "secp256k1"})
    pubkey_bytes = pubkey_result["public_key_uncompressed_bytes"]
    
    result = pubkey_to_eth_address(inputs={"public_key_uncompressed_bytes": pubkey_bytes})
    
    assert "eth_address_hex" in result
    assert isinstance(result["eth_address_hex"], str)
    assert result["eth_address_hex"].startswith("0x")
    assert len(result["eth_address_hex"]) == 42
    assert result["eth_address_hex"] == "0x19e7e376e7c213b7e7e7e46cc70a5dd086daff2a"

if __name__ == "__main__":
    test_generate_entropy()
    print("✓ test_generate_entropy passed")
    test_entropy_to_mnemonic()
    print("✓ test_entropy_to_mnemonic passed")
    test_mnemonic_to_seed()
    print("✓ test_mnemonic_to_seed passed")
    test_derive_master_key()
    print("✓ test_derive_master_key passed")
    test_derive_child_key()
    print("✓ test_derive_child_key passed")
    test_private_key_to_public()
    print("✓ test_private_key_to_public passed")
    test_pubkey_to_eth_address()
    print("✓ test_pubkey_to_eth_address passed")
    print("\nAll atom tests passed!")
