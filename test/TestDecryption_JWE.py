from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode, json_decode

# 生成密钥对
def generate_key():
    key = jwk.JWK.generate(kty="RSA", size=2048)
    return key

# 创建 JWE
def create_jwe(payload, public_key):
    protected_header = {
        "alg": "RSA-OAEP",  # 加密算法
        "enc": "A256GCM",   # 内容加密算法
        "typ": "JWT"
    }
    # 创建 JWE
    token = jwe.JWE(
        json_encode(payload),
        recipient=public_key,
        protected=protected_header
    )
    # 生成json格式
    # return token.serialize()
    # 生成string格式
    return token.serialize(compact=True)

# 解密 JWE
def decrypt_jwe(token, private_key):
    try:
        jwe_token = jwe.JWE()
        jwe_token.deserialize(token, key=private_key)  # 将 token 作为字符串传入
        decrypted_payload = json_decode(jwe_token.payload)  # 解码 payload
        return decrypted_payload
    except Exception as e:
        return f"解密失败: {e}"

# 测试
key = generate_key()
payload = {"user_id": 123, "username": "john_doe"}

# 创建 JWE
jwe_token = create_jwe(payload, key)
print("生成的 JWE:", jwe_token)

# 解密 JWE
decrypted_payload = decrypt_jwe(jwe_token, key)
print("解密后的 Payload:", decrypted_payload)


# 结果
# 生成的 JWE: {"ciphertext":"olBC4lZKmIufiF2Wef_5x1h7jHBXuwJSTycvQBr6hYrvRzGTcw","encrypted_key":"EHzM2ytKWU3F5QttPlqVSaAkyAzaMNE5Ag7Wy6K7g6npDIL5eSPqC8DHPHD5h6XAU-_W2aLeeu0X7Kb4n6cUU8YMIbKkkzUV35oy6N57JBcIqpt3w5av5ry2nU0BJlwBzP_tm1Vjy87vOqkKn5yKcUrjjbgVhZLLpEj0_pSqTz4thoVZDey3tXItuoBgLKTq2kto_E-tAsnGfTzA6ARAYfFQZtxFhazWwudKKc3bS8xdOeW_MLWrfRkdxxS7a9K6qpIr22_4ngw5OJG4-RTuuoobhvWbDL5gEY3IMu92iNu_flaJEDZOAxdksAmLCLFp9WL_zdbRVRCcWRmOFmFq-w","iv":"IOY2Hrpjoa85YPBK","protected":"eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJ0eXAiOiJKV1QifQ","tag":"PWc3KusTkKnH-KFvqbngZg"}
# 解密后的 Payload: {'user_id': 123, 'username': 'john_doe'}

# 生成的 JWE: eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJ0eXAiOiJKV1QifQ.AQkbjRghng9JU6kL3Jz-zLy8pd4aExavodeguwv8rMx8K2CZ_yCcE3JJEIGrv_znfZCkcNEWrd4q6NR5w0Y3uMWqfwqgm37MQP7lg-upcP477QKV8RP9CqdWiUhkiKlkeULbrK8zKVX7CQZ-DBZWiNLVFqsSrqPAEk4Rfa42y8qSI98XTMoni0Cf7_oumvNPRVgnO0ekN2KsP_9mt4aAmMxCiKXAvxZvsgz-1dAyoFcW3lyGCHvEIQinQkCJRIF17XSyxC0JNs7fBUcbBhRBEvLMkszcUF8aC1JlSj35i2szP6CiU-3v2mOBZykCyinyLfGA_stY3dWvEQ40COvK4w.tRlDnB91YeD7ohAN._2IuXXu_d5uiEzXEWjl9BeR4i30cesejbGyQe9AyyjbWbrWgXA.1xqkG_hAD3HpjnArnY_Bhg
# 解密后的 Payload: {'user_id': 123, 'username': 'john_doe'}

