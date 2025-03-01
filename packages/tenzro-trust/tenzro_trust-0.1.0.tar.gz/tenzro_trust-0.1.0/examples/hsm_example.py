# tenzro-trust/examples/hsm_example.py

import os
import sys
import json
import time

# Add parent directory to path to import tenzro_trust
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tenzro_trust import get_tenzro_trust, TenzroTrustException

def main():
    """Example using Tenzro Trust HSM provider with the new providers package structure."""
    
    print("Tenzro Trust HSM Provider Example (Updated Structure)")
    print("===================================================")
    
    try:
        # Initialize with simulated HSM for example purposes
        config = {
            "provider": "hsm",
            "hsm_type": "simulated",
            "key_id": "example-key-1"
        }
        
        # Get trust provider using config
        trust = get_tenzro_trust(provider_name="hsm")
        trust.initialize(config)
        
        print(f"Initialized HSM provider ({config['hsm_type']} mode)")
        
        # Create some test data
        transaction = {
            "tx_id": f"tx_{int(time.time())}",
            "timestamp": int(time.time()),
            "sender": "wallet_a",
            "receiver": "wallet_b",
            "amount": 50.0,
            "fee": 0.01,
            "currency": "ETH",
            "network": "mainnet"
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
        
        # Demonstrate tamper detection
        print("\n--- Demonstrating Tamper Detection ---")
        
        # Create a malicious modified transaction
        tampered_tx = transaction.copy()
        tampered_tx["amount"] = 500.0  # Changed from 50.0 to 500.0
        tampered_bytes = json.dumps(tampered_tx).encode('utf-8')
        
        # Try to verify the tampered transaction with original signature
        tamper_result = trust.verify(tampered_bytes, signature)
        print(f"Original transaction: amount = {transaction['amount']}")
        print(f"Tampered transaction: amount = {tampered_tx['amount']}")
        print(f"Tamper verification result: {tamper_result} (Expected: False)")
        
        # Get attestation data
        attestation = trust.get_attestation()
        if attestation:
            print("\nHSM Attestation data:")
            for key, value in attestation.items():
                print(f"  {key}: {value}")
        
        # Show provider module path to confirm it's using the new structure
        provider_module = trust.__class__.__module__
        print(f"\nProvider module path: {provider_module}")
        
        # Example configurations for different HSM types
        print("\nExample configurations for different HSM types:")
        
        print("\n1. AWS CloudHSM:")
        print("  trust = get_tenzro_trust(provider_name=\"hsm\")")
        print("  trust.initialize({")
        print("      \"hsm_type\": \"aws\",")
        print("      \"region\": \"us-west-2\",")
        print("      \"key_id\": \"alias/tenzro-signing-key\",")
        print("      \"profile\": \"production\"")
        print("  })")
        
        print("\n2. Google Cloud HSM:")
        print("  trust = get_tenzro_trust(provider_name=\"hsm\")")
        print("  trust.initialize({")
        print("      \"hsm_type\": \"google\",")
        print("      \"project_id\": \"my-project\",")
        print("      \"location_id\": \"global\",")
        print("      \"key_id\": \"my-signing-key\"")
        print("  })")
        
        print("\n3. Azure Key Vault HSM:")
        print("  trust = get_tenzro_trust(provider_name=\"hsm\")")
        print("  trust.initialize({")
        print("      \"hsm_type\": \"azure\",")
        print("      \"vault_name\": \"my-key-vault\",")
        print("      \"tenant_id\": \"my-tenant-id\",")
        print("      \"key_id\": \"my-key-name\"")
        print("  })")
        
    except TenzroTrustException as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()