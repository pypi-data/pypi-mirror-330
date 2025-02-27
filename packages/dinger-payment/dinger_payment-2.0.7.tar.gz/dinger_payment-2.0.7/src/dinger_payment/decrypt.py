from Crypto.Cipher import AES
import json
import base64


def decrypt_aes_ecb(encrypted_data, secret_key):
    # Ensure key is exactly 32 bytes long
    key = secret_key.encode("utf-8").ljust(32, b"\0")[:32]

    try:
        # Decode from Base64
        encrypted_bytes = base64.b64decode(encrypted_data)

        # Create AES cipher in ECB mode
        cipher = AES.new(key, AES.MODE_ECB)

        # Decrypt data
        decrypted_bytes = cipher.decrypt(encrypted_bytes)

        # Remove PKCS7 padding correctly
        pad_length = decrypted_bytes[-1]
        decrypted_data = decrypted_bytes[:-pad_length].decode("utf-8")

        # Try parsing as JSON
        return json.loads(decrypted_data)

    except (ValueError, json.JSONDecodeError) as e:
        print(f"Decryption error: {e}")
        return None  # Or return decrypted_data for debugging