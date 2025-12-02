import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_base64(data):
    return base64.b64decode(data)

def decrypt_by_rsa(data, private_key):
    # Load the private key
    private_key = serialization.load_der_private_key(
        decrypt_base64(private_key),
        password=None,
        backend=default_backend()
    )

    # Decrypt the data
    decrypted_data = private_key.decrypt(
        decrypt_base64(data),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data.decode('utf-8')

def decrypt_by_aes_cbc(encrypted, key, init_vector):
    # Decode the key and initialization vector
    key = decrypt_base64(key)
    init_vector = init_vector.encode('utf-8')

    # Create the AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(init_vector), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(decrypt_base64(encrypted)) + decryptor.finalize()

    # Remove padding
    return decrypted_data.decode('utf-8')

def de_step2(private_key):
    # Decode the AES key using RSA
    aes_key = decrypt_by_rsa(jwe_encrypt_key, private_key)

    # Decode the initialization vector
    init_vector = decrypt_base64(jwe_vector).decode('utf-8')

    # Decrypt the payload using AES CBC
    jws_sign_str = decrypt_by_aes_cbc(jwe_payload, aes_key, init_vector)

    print(jws_sign_str)
    return jws_sign_str


private_key = "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"
jwe_encrypt_key = "YwkcvEkT/VjunzaBEncuLBhOfI7Zy8R9TSlq4bjoQXBBuBdbUnmvg/mCr5gs2XzCXS8xS8mPf+xzSYT7H6TpR1/hJMhiCEHLElVQyu5nkGnAhicl9QpHoghWxhXTB0jI29IEg3hhg5lZZ9wJ4pB4noTJkoTyhBonAc/4qas4c5VJuCOhijScmH0mxtJofT7Fj1/Wfpsf9apCwatRH7fA9SF/npWDBc6JP+MhrQPMv0ZptRuszmcuAmqdP0LpNfQk+2fV7/HE7LxcXMdGwc3VuEaP4Nw9w7AqgdCKp3cbwzqyv1UmLsLbgAql6++0xIELvaq8w7E+r4/wOLcV18AvTk5vli3biIXF5g4n1viYt/uzajm7gXPE8woL2XSbFO716UCgd5UaGLyBDqORq9kTTOqsvEBwAZzS1rXwutwUNjC+0q6S8J2OKng0s56Cm5V5cTGJ7JIBWBiN4d9wr3V4yP9Y/ATd1PxfR1sAbPgphb+eAWWYk5CZWSnt55lczFp9"
jwe_vector = "NTgzODJkMjZiODRhNGZkNw=="
jwe_payload = "KT6OpeYxa8S8ZIoU7Bgn8WXKDlzhCoO89luYPs/wPZPX4pvqtkxmEuEemF1iAtjXfaOU8pJnXwIZX+Kp27iLNMzSR3QyxiyvtXUoWbRfoorgYZY4n6asluEGqyFItu4Dl7X1Lm1MT3ToC22O2f92a4Sbl06nWLJSKcKlHRqyDL3Nnbdj6GatBCFtqCZ8j65gxlJ4WvvrZgC8iIO2v0D5rCznnbYPxxqRxMOQhvwIroBXDtIrLv8ZgLLmLYbogvXSVeXWEMkoQrjlxV9Z68L1ad8pT76yoiAKlevsCbADzQDpQ18ND9qe3rR3z1HEeCGYgZ0XXtbOHsLzlBSTzpE5iyROgiFFUiatUXsdpqjZRMSQI8YDvvJWdEY6UfCuL+CFF5MIXa433AQEheffQA5IozYQxAtd9XiahQr0wIxy0uWWTrrD7Uejwj/U11jHp3ExpGaNmotizuK3PFnymh/KZAOj+GR0hgUKc+VGojopaT3zNXLmowl7RBEclrovO/zDBBqO7E9DWpq8X3mYERQ0ul+cFAQmU7Vwiv7Jvj176BJA6KtO4UPvlj1cAKe9WjEI6IiRj6ihdzHeko3UEQG6LqzFT4xuP79hLJ+gSeCPLF2LkCc2HFcdAeGyFphuHK0voEaBfA5smZY1BZYEoibZfDgz4xV58/GCMiH9cLNdCNrILrKqBaay9exeTsWfNw3/TyJOYdAPpPxAKOlVRbKQbn4mPkgTef9lMSA/KM/P81eIX3gP46Q9M3SlHz5KwJlCtTiXMpkGvyVvPU8u89p0v79FxKPpNCQ2LcfsY9XrEc+vhP/V6rxz16hQAH7pFxsXFvbbCBYI+WQstwjcDOnTG5S3cczSVMbgg70ICl7WfNw="

de_step2(private_key)
