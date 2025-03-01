# tenzro-trust/examples/tpm_example.py

import os
import sys
import json
import time

# Add parent directory to path to import tenzro_trust
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tenzro_trust import get_tenzro_trust, TenzroTrustException

def main():
    """Example using Tenzro Trust TPM provider with the new providers package structure."""
    
    print("Tenzro Trust TPM Provider Example (Updated Structure)")
    print("===================================================")
    
    try:
        # Initialize with simulated TPM for example purposes
        config = {
            "provider": "tpm",
            "simulator": True,  # Use simulator since most machines don't have accessible TPMs
            "key_handle": "0x81000001",
            "algorithm": "RSA"
        }
        
        # Get trust provider using config
        trust = get_tenzro_trust(provider_name="tpm")
        trust.initialize(config)
        
        print(f"Initialized TPM provider (simulation mode)")
        
        # Create some test data
        transaction = {
            "tx_id": "tx_67890",
            "timestamp": int(time.time()),
            "sender": "wallet_c",
            "receiver": "wallet_d",
            "amount": 25.5,
            "metadata": {
                "memo": "Payment for services",
                "category": "invoice"
            }
        }
        
        # Convert to bytes for signing
        tx_bytes = json.dumps(transaction).encode('utf-8')
        
        print(f"Transaction data: {transaction}")
        
        # Sign the transaction
        signature = trust.sign(tx_bytes)
        print(f"Generated signature: {signature.hex()[:20]}...")
        
        # Verify the signature
        is_valid = trust.verify(tx_bytes, signature)
        print(f"Signature verification result: {is_valid}")
        
        # Try modifying the data and verify again (should fail)
        modified_tx = transaction.copy()
        modified_tx["amount"] = 100.0
        modified_bytes = json.dumps(modified_tx).encode('utf-8')
        
        is_still_valid = trust.verify(modified_bytes, signature)
        print(f"Verification after data modification: {is_still_valid} (expected: False)")
        
        # Get attestation data
        attestation = trust.get_attestation()
        if attestation:
            print("\nTPM Attestation data:")
            for key, value in attestation.items():
                print(f"  {key}: {value}")
        
        # Show provider module path to confirm it's using the new structure
        provider_module = trust.__class__.__module__
        print(f"\nProvider module path: {provider_module}")
        
        # Example of integrating with a real TPM (commented out as most users won't have access)
        print("\nTo use a real TPM (on a Linux system with TPM 2.0):")
        print("  trust = get_tenzro_trust(provider_name=\"tpm\")")
        print("  trust.initialize({")
        print("      \"device\": \"/dev/tpmrm0\",  # TPM resource manager")
        print("      \"key_handle\": \"0x81000001\",")
        print("      \"algorithm\": \"RSA\"")
        print("  })")
        
    except TenzroTrustException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()