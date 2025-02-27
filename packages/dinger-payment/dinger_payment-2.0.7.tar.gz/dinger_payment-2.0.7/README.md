# Dinger Prebuild Checkout From for generate URL

## Usage

### Encryption

```python
import json
from urllib.parse import urlencode, quote_plus

from dinger_payment import get_prebuild_form_url

if __name__ == '__main__':
    items = [
        {"name": "DiorAct Sandal", "amount": 250, "quantity": 1},
        {"name": "Aime Leon Dore", "amount": 250, "quantity": 1},
    ]
    data = {
        # items must be string
        "items": json.dumps(items),
        "customerName": "James",
        "totalAmount": 500,
        "merchantOrderId": "123456",
        # get from checkout-form page
        "clientId": "xxxx",
        # get from data-dashboard page
        "publicKey": "xxxx",
        # get from data-dashboard page
        "merchantKey": "xxxx",
        # your project name
        "projectName": "xxxx",
        # your account username
        "merchantName": "xxxx",
    }
    secretkey = "xxxx"
    public_key = "-----BEGIN PUBLIC KEY-----\n"
                 + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFD4IL1suUt/TsJu6zScnvsEdLPuACgBdjX82QQf8NQlFHu2v/84dztaJEyljv3TGPuEgUftpC9OEOuEG29z7z1uOw7c9T/luRhgRrkH7AwOj4U1+eK3T1R+8LVYATtPCkqAAiomkTU+aC5Y2vfMInZMgjX0DdKMctUur8tQtvkwIDAQAB"
                 + "\n-----END PUBLIC KEY-----"
    encrypted_payload, hash_value = get_prebuild_form_url(public_key=public_key, secretkey=secretkey, **data)
    host = "form.dinger.asia"  # for production
    # host = "prebuilt.dinger.asia" # for staging
    url = f"https://{host}?{urlencode({'payload': encrypted_payload, 'hashValue': hash_value}, quote_via=quote_plus)}"
    print(url)
```

### Decryption

```python
    from dinger_payment import decrypt_aes_ecb
    data = {'paymentResult': 'xxxx',
            'checksum': 'xxxx'}
    merchant_callback_key = "xxxx"
    
    # Example usage
    secret_key = callback_key  # Must be 32 characters or will be padded
    encrypted_data = data['paymentResult']  # Replace with actual encrypted data
    
    decrypted_value = decrypt_aes_ecb(encrypted_data, secret_key)
    print(decrypted_value)
```
