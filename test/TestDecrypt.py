import base64
import hmac
import hashlib


privateKey = ''
def decrypt(payload,private_key):
    
    parts = payload.split('.')
    
    c1 = check_auth_tag(parts[3],parts[4])
    if not c1:
        raise Exception("认证标签校验失败")
    
    d1 = ''
    


    raw = get_substring(d1,1)
    result = decrypt_base64(raw)
    print(result)
    pass

def check_auth_tag(payload,last):
    KEY_MAC = "HmacMD5"
    auth_tag = encrypt_base64(encrypt_hmac(payload, KEY_MAC))
    return auth_tag == last

def get_substring(input_string, part):
    # Split the string by "."
    parts = input_string.split('.')

    # Check if the part index is valid
    if part < 0 or part >= len(parts):
        return "Invalid part index"

    # Return the specific part
    return parts[part]


def encrypt_base64(key: bytes) -> str:
    # Return the Base64 encoded string of the byte array
    return base64.b64encode(key).decode('utf-8')

def decrypt_base64(key):
    return base64.b64decode(key)






def encrypt_hmac(key, key_mac):
    # Fix padding of the base64 key if necessary
    # missing_padding = len(key) % 4
    # if missing_padding:
    #     key += '=' * (4 - missing_padding)

    # Decode the key using base64
    decoded_key = base64.b64decode(key)

    # Create HMAC using the key and the hash function (SHA256 is used by default in Java)
    hmac_object = hmac.new(decoded_key, msg=key_mac.encode(), digestmod=hashlib.sha256)

    # Return the result of HMAC in bytes
    return hmac_object.digest()


def encrypt_base64(key):
    # Encode the byte array to base64 string
    return base64.b64encode(key).decode('utf-8')


# Example usage:
# key_mac = "your_key_mac_string"
# key = "your_key_base64_encoded_string"

key_mac = "HmacMD5"
key = "qn6v51ZQBOPndnKQtbQZeA=="


# Calculate the authTag equivalent
auth_tag_bytes = encrypt_hmac(key, key_mac)
auth_tag = encrypt_base64(auth_tag_bytes)

print(auth_tag)
