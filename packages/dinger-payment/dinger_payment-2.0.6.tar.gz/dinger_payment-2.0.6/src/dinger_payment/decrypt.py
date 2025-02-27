from Crypto.Cipher import AES
import json
import base64

def decrypt_aes_ecb(encrypted_data, secret_key):
    # Ensure key is 32 bytes long (AES-256 requires a 32-byte key)
    key = secret_key.encode("utf-8").ljust(32, b"\0")  # Pad if less than 32 bytes

    # Decode from Base64 (since the input is Base64-encoded)
    encrypted_bytes = base64.b64decode(encrypted_data)

    # Create AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt and remove padding
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    decrypted_data = decrypted_bytes.rstrip(b"\x00").decode("utf-8")  # Remove null padding

    return json.loads(decrypted_data)