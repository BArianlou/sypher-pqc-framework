import json
from .symmetric_cipher import SypherCipher

def package_sypher_payload(agent_state, shared_secret):
    cipher = SypherCipher(shared_secret)
    data_string = json.dumps(agent_state)
    return cipher.encrypt(data_string)

def unpack_sypher_payload(payload, shared_secret):
    cipher = SypherCipher(shared_secret)
    decrypted_data = cipher.decrypt(payload)
    return json.loads(decrypted_data)
