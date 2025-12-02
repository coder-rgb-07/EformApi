import base64
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad



# 解密 JWE
def decrypt(jwe_encrypt_str, private_key):
    try:
        KEY_MAC = "HmacMD5"

        # 拆分 JWE 字符串
        en_codes = jwe_encrypt_str.split(".")
        if len(en_codes) != 5:
            raise ValueError("decrypt error, incorrect jweEncryptStr!")

        jwe_header, jwe_encrypt_key, jwe_vector, jwe_payload, jwe_auth_tag = en_codes

        # 校验 authTag 完整性
        auth_tag = base64.b64encode(
            HMAC.new(KEY_MAC.encode(), jwe_payload.encode(), SHA256).digest()
        ).decode()
        print('jwe1 '+jwe_auth_tag)
        print('jwe2 '+auth_tag)
        if jwe_auth_tag != auth_tag:
            raise ValueError("authTag check failure")

        # 解码 AES_KEY
        aes_key = decrypt_by_rsa(jwe_encrypt_key, private_key)

        # 解码 INIT_VECTOR
        init_vector = base64.b64decode(jwe_vector).decode()

        # 解码 Header
        header_str = base64.b64decode(jwe_header).decode()
        header = json.loads(header_str)

        # 解码 Payload
        jws_sign_str = decrypt_by_aes_cbc(jwe_payload, aes_key, init_vector)

        # 返回结果
        return {
            "code": jws_sign_str,
            "header": header
        }
    except Exception as e:
        raise Exception(f"Decryption failed: {e}")

# RSA 解密
def decrypt_by_rsa(encrypted_key, private_key):
    try:
        # 加载私钥
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_key))
        return decrypted.decode()
    except Exception as e:
        raise Exception(f"RSA decryption failed: {e}")

# AES CBC 解密
def decrypt_by_aes_cbc(encrypted, key, init_vector):
    try:
        # 解码密钥和初始化向量
        key = base64.b64decode(key)
        init_vector = init_vector.encode("utf-8")

        # 创建 AES 解密器
        cipher = AES.new(key, AES.MODE_CBC, init_vector)
        decrypted = cipher.decrypt(base64.b64decode(encrypted))

        # 去除填充
        return unpad(decrypted, AES.block_size).decode("utf-8")
    except Exception as e:
        raise Exception(f"AES decryption failed: {e}")

# # 示例
# if __name__ == "__main__":
#     # 示例 JWE 字符串和私钥
#     jwe_encrypt_str = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00ifQ.XXX.YYY.ZZZ.AAA.BBB"
#     private_key = """-----BEGIN RSA PRIVATE KEY-----
#     MIIEpAIBAAKCAQEA...
#     -----END RSA PRIVATE KEY-----"""
#
#     # 解密
#     try:
#         result = decrypt(jwe_encrypt_str, private_key)
#         print("解密结果:", result)
#     except Exception as e:
#         print("解密失败:", e)

# 示例
if __name__ == "__main__":
    # 示例 JWE 字符串和私钥
    # jwe_encrypt_str = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00ifQ.XXX.YYY.ZZZ.AAA.BBB"
    # private_key = """-----BEGIN RSA PRIVATE KEY-----
    # MIIEpAIBAAKCAQEA...
    # -----END RSA PRIVATE KEY-----"""
    jwe_encrypt_str = "eyJhbGciOiJSU0ExXzUiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0=.YwkcvEkT/VjunzaBEncuLBhOfI7Zy8R9TSlq4bjoQXBBuBdbUnmvg/mCr5gs2XzCXS8xS8mPf+xzSYT7H6TpR1/hJMhiCEHLElVQyu5nkGnAhicl9QpHoghWxhXTB0jI29IEg3hhg5lZZ9wJ4pB4noTJkoTyhBonAc/4qas4c5VJuCOhijScmH0mxtJofT7Fj1/Wfpsf9apCwatRH7fA9SF/npWDBc6JP+MhrQPMv0ZptRuszmcuAmqdP0LpNfQk+2fV7/HE7LxcXMdGwc3VuEaP4Nw9w7AqgdCKp3cbwzqyv1UmLsLbgAql6++0xIELvaq8w7E+r4/wOLcV18AvTk5vli3biIXF5g4n1viYt/uzajm7gXPE8woL2XSbFO716UCgd5UaGLyBDqORq9kTTOqsvEBwAZzS1rXwutwUNjC+0q6S8J2OKng0s56Cm5V5cTGJ7JIBWBiN4d9wr3V4yP9Y/ATd1PxfR1sAbPgphb+eAWWYk5CZWSnt55lczFp9.NTgzODJkMjZiODRhNGZkNw==.KT6OpeYxa8S8ZIoU7Bgn8WXKDlzhCoO89luYPs/wPZPX4pvqtkxmEuEemF1iAtjXfaOU8pJnXwIZX+Kp27iLNMzSR3QyxiyvtXUoWbRfoorgYZY4n6asluEGqyFItu4Dl7X1Lm1MT3ToC22O2f92a4Sbl06nWLJSKcKlHRqyDL3Nnbdj6GatBCFtqCZ8j65gxlJ4WvvrZgC8iIO2v0D5rCznnbYPxxqRxMOQhvwIroBXDtIrLv8ZgLLmLYbogvXSVeXWEMkoQrjlxV9Z68L1ad8pT76yoiAKlevsCbADzQDpQ18ND9qe3rR3z1HEeCGYgZ0XXtbOHsLzlBSTzpE5iyROgiFFUiatUXsdpqjZRMSQI8YDvvJWdEY6UfCuL+CFF5MIXa433AQEheffQA5IozYQxAtd9XiahQr0wIxy0uWWTrrD7Uejwj/U11jHp3ExpGaNmotizuK3PFnymh/KZAOj+GR0hgUKc+VGojopaT3zNXLmowl7RBEclrovO/zDBBqO7E9DWpq8X3mYERQ0ul+cFAQmU7Vwiv7Jvj176BJA6KtO4UPvlj1cAKe9WjEI6IiRj6ihdzHeko3UEQG6LqzFT4xuP79hLJ+gSeCPLF2LkCc2HFcdAeGyFphuHK0voEaBfA5smZY1BZYEoibZfDgz4xV58/GCMiH9cLNdCNrILrKqBaay9exeTsWfNw3/TyJOYdAPpPxAKOlVRbKQbn4mPkgTef9lMSA/KM/P81eIX3gP46Q9M3SlHz5KwJlCtTiXMpkGvyVvPU8u89p0v79FxKPpNCQ2LcfsY9XrEc+vhP/V6rxz16hQAH7pFxsXFvbbCBYI+WQstwjcDOnTG5S3cczSVMbgg70ICl7WfNw=.qn6v51ZQBOPndnKQtbQZeA=="
    private_key = "MIIG/gIBADANBgkqhkiG9w0BAQEFAASCBugwggbkAgEAAoIBgQCnzbhcRZS4vZYE7wLJJyEw80YVhic9ZxvIxdffgOQGdtUSazY85DjOB0QWs5mX5jT2Jl2f9d+1rPt71CVD/KsZEJHm5+mSOJLlG59isF0h3diwGjWreZ5SqQZSxSP4kuWxoQbVzHWbCYgwdioLsn/6qssMcwS0JSZ5vs+52buXhLl4eT9D3mrxNSqQXeLuz89bLLM9mTMEZ/McKETNJRl61GpQcghRtqgayMYKIncqVT347Sh6N3GAbUwrbZZfO9MWdKffR407DodhaPiC4p+pDuPXUxqYJUemNnzOEfXv3Ma23dFFgEU2K1sPrhQh5RzvYzFgYOPtJgJLxE8WWd1UUiYvX/JNTYoCClLs3yBzrYNYkGOd0zURa56Fmtz3Xct+vXypCQL99LLvWJU9hta/UT1prNk2Do58xB8FejkfRemwEWXKcOSG4W9QGlgkt7+jhJI80+2zgRRv8f88yBr3NPuGTDKFkc/oYD4OIk9DHxH7/+Vsu7j21j3vw4ZzJT0CAwEAAQKCAYAsw6F55An/mnvJxyT8GlctYsiAd3BCXh44WibzdcPewZanujgW2F8a/y83yyOfNQdN3wA86u+J3KKd7wMd9uqB3jy914IkwrjVK6BCSIAfx7nFiMhmfSQyMur/651j83QZBbb4E/oPqORO4UboJe8kJKnUIV7Q29Q+yBtMHfyAOCTuMZIh/dSTkjZPmuwt/vv2+565QQQuGbjt+wQXod0BOmc+HJ2BhvOjaYoDLByUC3djz4hryhyaQQ3/y9VAhImliDItNZgLXScoHA86d77r99u8lYXDIdYmKy7rcK6Naz9hdyWId++eglU+xesJmkks/E4P2wHEGpPNZyMzSQ+TzkvgjxC3lB1+Ozul3ZhtzMddvTj2pN72wPnOrM4W9Btexd1Z2k3oex6TfiyIE21X3N7i7BmVO5+1trdxaqAcmLDaRdtULc9s1wNCKmqYopB52n/DxFW4PgbmI3yWKQhygy0l1NCSNbxT+QORRyLBpmDJ4BOLM+hJ9pN6oiDSeXUCgcEAxJZeFA/Eq96u4bMvfLQEjEyD181Khgv+Zt1XENrhHJ9WWRWjCjIvCOx+gT16lqzxR3ii2ANp0qgTzkoRT3HtViu1BcPyIEPerTAKX1jtaO/VVoHS6Vb8oMIPSEvVcKeg0IL/wTo9spW2Kimf79F3UCnDplQb5H43WeTs32Zdm23N9QQogHm9011RjGHJ4CelidndFC7UIsecPPOM07UasaGr1O5AUsp+RxysuQgPxR9btz3gvz4pCn9yIl3aOHh3AoHBANqEZoCdwIzilSrd184/OENU5Sc67KiS8vFXWFXjBGT7kF1zvFD78HNMIas5peyLm8HXcn1Hj+8saqHOojDqgIElfrHRSCLGj26OBobqsEan/cY/QcSFgn6D61kIf52Frf+6EZtzWDVvjCw+OvSmz8x7996vWCHLxr0ZIpiczcbd/Pd43qqqF4lS4sBfWvVuTgR6pBTU7kXUjn9sdlcCtZmlLjRkKdNzEiwd1wciTRG2o1Ts7h+rG9ZGOocw0fvw6wKBwQCMb+cxabpUFbbVIc7QxUFigN7G8a9FZ5gMIB8suVCLxABJj71zcTpMo7YT2bmTnmSXbETZEEcu6EeN3TfUi0zDfGHLhpmYFyQikOk4CC1CA+Nh80iazTuYFEoamaIW4oltq8fNYC/nPjBummHZTshvigZs8jUi3E/qdjIJvfUtLhot6RSOA2pqboXtRYaUDX6ipfLbkkCVwAeLO2nla8FwGFDKwpFNE792SbPSU0IAzlAU7a16sYtcJoOArY9RPC0CgcEAlfAtiWk1WzaKVjycvNeiWokhJ/cFtnIGo1VktqIsPMJk/8rPV95X0jVWEPBgitwMx0h3NcFp4RpgHKD1p4zxGizJL2hEECChAKIRlnfo9sKEnoh/L0LRFNCeJ5xuPH8isotRU5Ik352n2B/nQkJH6a7SmQlF9wKlXtGlbISDqkZeMszMNNy7g63NC2Uiu6+xdt9UQTsON/ouwP6CgRfJ1iCCgM6N6JpXyM+84RdHPLVOg5KDnlVBp5jOxj7YhwB7AoHADif+Dl3c+H1csjozvb5zyE4W6sCEaZbEHHE6GbfKw6ProagCaGD0mshytycClbUwyTzC4FEMLFnZrjAjCngBkUEDfBSNsHmll3zmEhPx/QhxuV2KUMrQrKXnhUGKcTaA8Pj/jiu/NAulMCxaLyuef2oKyRjZMVb/T9wl/PGJY8BNprFuf4xkNRoAQabpGmJM8ZjhUAgL4UHIEdXPVE5/k7BUA8qxt6T5vhtO1AXKegJodu824WR4K1SYSK9IaYID"

    # 解密
    try:
        result = decrypt(jwe_encrypt_str, private_key)
        print("解密结果:", result)
    except Exception as e:
        print("解密失败:", e)


# token = "eyJhbGciOiJSU0ExXzUiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0=.YwkcvEkT/VjunzaBEncuLBhOfI7Zy8R9TSlq4bjoQXBBuBdbUnmvg/mCr5gs2XzCXS8xS8mPf+xzSYT7H6TpR1/hJMhiCEHLElVQyu5nkGnAhicl9QpHoghWxhXTB0jI29IEg3hhg5lZZ9wJ4pB4noTJkoTyhBonAc/4qas4c5VJuCOhijScmH0mxtJofT7Fj1/Wfpsf9apCwatRH7fA9SF/npWDBc6JP+MhrQPMv0ZptRuszmcuAmqdP0LpNfQk+2fV7/HE7LxcXMdGwc3VuEaP4Nw9w7AqgdCKp3cbwzqyv1UmLsLbgAql6++0xIELvaq8w7E+r4/wOLcV18AvTk5vli3biIXF5g4n1viYt/uzajm7gXPE8woL2XSbFO716UCgd5UaGLyBDqORq9kTTOqsvEBwAZzS1rXwutwUNjC+0q6S8J2OKng0s56Cm5V5cTGJ7JIBWBiN4d9wr3V4yP9Y/ATd1PxfR1sAbPgphb+eAWWYk5CZWSnt55lczFp9.NTgzODJkMjZiODRhNGZkNw==.KT6OpeYxa8S8ZIoU7Bgn8WXKDlzhCoO89luYPs/wPZPX4pvqtkxmEuEemF1iAtjXfaOU8pJnXwIZX+Kp27iLNMzSR3QyxiyvtXUoWbRfoorgYZY4n6asluEGqyFItu4Dl7X1Lm1MT3ToC22O2f92a4Sbl06nWLJSKcKlHRqyDL3Nnbdj6GatBCFtqCZ8j65gxlJ4WvvrZgC8iIO2v0D5rCznnbYPxxqRxMOQhvwIroBXDtIrLv8ZgLLmLYbogvXSVeXWEMkoQrjlxV9Z68L1ad8pT76yoiAKlevsCbADzQDpQ18ND9qe3rR3z1HEeCGYgZ0XXtbOHsLzlBSTzpE5iyROgiFFUiatUXsdpqjZRMSQI8YDvvJWdEY6UfCuL+CFF5MIXa433AQEheffQA5IozYQxAtd9XiahQr0wIxy0uWWTrrD7Uejwj/U11jHp3ExpGaNmotizuK3PFnymh/KZAOj+GR0hgUKc+VGojopaT3zNXLmowl7RBEclrovO/zDBBqO7E9DWpq8X3mYERQ0ul+cFAQmU7Vwiv7Jvj176BJA6KtO4UPvlj1cAKe9WjEI6IiRj6ihdzHeko3UEQG6LqzFT4xuP79hLJ+gSeCPLF2LkCc2HFcdAeGyFphuHK0voEaBfA5smZY1BZYEoibZfDgz4xV58/GCMiH9cLNdCNrILrKqBaay9exeTsWfNw3/TyJOYdAPpPxAKOlVRbKQbn4mPkgTef9lMSA/KM/P81eIX3gP46Q9M3SlHz5KwJlCtTiXMpkGvyVvPU8u89p0v79FxKPpNCQ2LcfsY9XrEc+vhP/V6rxz16hQAH7pFxsXFvbbCBYI+WQstwjcDOnTG5S3cczSVMbgg70ICl7WfNw=.qn6v51ZQBOPndnKQtbQZeA=="
# SP_PRIVATE_KEY_3072 = "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"
# decrypted_payload = decrypt_jwe(jwe_token, SP_PRIVATE_KEY_3072)
# print("解密后的 Payload:", decrypted_payload)