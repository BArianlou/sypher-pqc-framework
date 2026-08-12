import json

# Ge's Execution Fix: CI/CD and isolated test compatibility
try:
    from .symmetric_cipher import SypherCipher
except ImportError:
    from symmetric_cipher import SypherCipher

def package_sypher_payload(agent_state: dict, shared_secret: bytes, session_id: bytes = None) -> bytes:
    """
    Serializes and encrypts the agent state, optionally binding it to a session ID.
    """
    cipher = SypherCipher(shared_secret)
    
    # Triune Fix 1: Deterministic Serialization
    # Strips whitespace to ensure the exact same byte-string across all OS/environments
    data_string = json.dumps(agent_state, separators=(',', ':'))
    
    # Triune Fix 2: Expose Associated Data (AAD)
    return cipher.encrypt(data_string, associated_data=session_id)

def unpack_sypher_payload(payload: bytes, shared_secret: bytes, session_id: bytes = None) -> dict:
    """
    Decrypts and deserializes the payload, verifying cryptographic integrity.
    """
    cipher = SypherCipher(shared_secret)
    
    # Triune Fix 2: Verify Associated Data (AAD)
    decrypted_data = cipher.decrypt(payload, associated_data=session_id)
    
    return json.loads(decrypted_data)
