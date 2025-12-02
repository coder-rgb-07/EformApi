import jwt
from datetime import datetime, timedelta

# 密钥（用于签名）
SECRET_KEY = "your-secret-key"

# 创建 JWT（带签名）
def create_jwt():
    payload = {
        "user_id": 123,
        "username": "john_doe",
        "exp": datetime.utcnow() + timedelta(hours=1)  # 过期时间
    }
    # 使用 HS256 算法签名
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# 验证 JWT
def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token 已过期"
    except jwt.InvalidTokenError:
        return "无效的 Token"

# 测试
token = create_jwt()
print("生成的 JWT:", token)
decoded = verify_jwt(token)
print("解码后的 JWT:", decoded)

# 结果
# 生成的 JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9obl9kb2UiLCJleHAiOjE3MzkzNDU4MDd9.XWGpFQQabATh5e6UC9psNIOM3PplkY4BW8qsfrRmxms
# 解码后的 JWT: {'user_id': 123, 'username': 'john_doe', 'exp': 1739345807}