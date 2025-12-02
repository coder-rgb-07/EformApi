import base64
import hmac
import hashlib
from typing import Optional


def encrypt_hmac(key: str, key_mac: str) -> bytes:
    # Decode the key from Base64
    decoded_key = base64.b64decode(key)

    # Create HMAC using the key and the hash function specified by key_mac (in this case 'HmacMD5')
    if key_mac == "HmacMD5":
        hash_function = hashlib.md5
    else:
        raise ValueError(f"Unsupported HMAC type: {key_mac}")

    hmac_object = hmac.new(decoded_key, msg=b"", digestmod=hash_function)
    return hmac_object.digest()





def encrypt_base64(key: bytes) -> str:
    # Return the Base64 encoded string of the byte array
    return base64.b64encode(key).decode('utf-8')

def decrypt_base64(key):
    return base64.b64decode(key)


def decrypt() -> bool:
    KEY_MAC = "HmacMD5"
    jwe_payload = "KT6OpeYxa8S8ZIoU7Bgn8WXKDlzhCoO89luYPs/wPZPX4pvqtkxmEuEemF1iAtjXfaOU8pJnXwIZX+Kp27iLNMzSR3QyxiyvtXUoWbRfoorgYZY4n6asluEGqyFItu4Dl7X1Lm1MT3ToC22O2f92a4Sbl06nWLJSKcKlHRqyDL3Nnbdj6GatBCFtqCZ8j65gxlJ4WvvrZgC8iIO2v0D5rCznnbYPxxqRxMOQhvwIroBXDtIrLv8ZgLLmLYbogvXSVeXWEMkoQrjlxV9Z68L1ad8pT76yoiAKlevsCbADzQDpQ18ND9qe3rR3z1HEeCGYgZ0XXtbOHsLzlBSTzpE5iyROgiFFUiatUXsdpqjZRMSQI8YDvvJWdEY6UfCuL+CFF5MIXa433AQEheffQA5IozYQxAtd9XiahQr0wIxy0uWWTrrD7Uejwj/U11jHp3ExpGaNmotizuK3PFnymh/KZAOj+GR0hgUKc+VGojopaT3zNXLmowl7RBEclrovO/zDBBqO7E9DWpq8X3mYERQ0ul+cFAQmU7Vwiv7Jvj176BJA6KtO4UPvlj1cAKe9WjEI6IiRj6ihdzHeko3UEQG6LqzFT4xuP79hLJ+gSeCPLF2LkCc2HFcdAeGyFphuHK0voEaBfA5smZY1BZYEoibZfDgz4xV58/GCMiH9cLNdCNrILrKqBaay9exeTsWfNw3/TyJOYdAPpPxAKOlVRbKQbn4mPkgTef9lMSA/KM/P81eIX3gP46Q9M3SlHz5KwJlCtTiXMpkGvyVvPU8u89p0v79FxKPpNCQ2LcfsY9XrEc+vhP/V6rxz16hQAH7pFxsXFvbbCBYI+WQstwjcDOnTG5S3cczSVMbgg70ICl7WfNw=";


    # Call encryption and compare authTag
    auth_tag = encrypt_base64(encrypt_hmac(jwe_payload, KEY_MAC))

    # Example "last" value for comparison
    last = "qn6v51ZQBOPndnKQtbQZeA=="

    return last == auth_tag


# Main function to execute the decryption logic
def main():
    try:
        print("Hello and welcome!")
        print(decrypt())
    except Exception as e:
        raise RuntimeError(e)


if __name__ == "__main__":
    main()
