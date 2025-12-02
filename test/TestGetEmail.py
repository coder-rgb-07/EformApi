import requests


def testGetLatestEmails():
    import msal
    import requests

    client_id = "c8057deb-a24e-484b-bf57-58bd5b196eb4"
    client_secret = "Tmh8Q~wLQbrdrNHa.H3Y7wl_w~YKvmuN4GgdAbyN"
    tenant_id = "abc55ec7-9e75-4a10-9bc8-8d81ca3e32a7"

    authority = f"https://login.microsoftonline.com/{tenant_id}"


    app = msal.ConfidentialClientApplication(
        client_id, 
        client_credential=client_secret, 
        authority=authority
    )

    # 获取令牌时使用 .default 作用域
    scopes=["Mail.Read"]
    # scopes=["https://graph.microsoft.com/.default"]
    token_response = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in token_response:
        token = token_response["access_token"]
        print("访问令牌: ", token)
        get_all_messages(token)
    else:
        print("获取令牌失败:", token_response.get("error_description", "未知错误"))

def get_all_messages(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    user_principal_name = 'life-enquiry@amgwealth.com'  # 确保邮箱地址正确
    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/messages"

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            messages = data.get('value', [])
            for message in messages:
                print(f"主题: {message['subject']}")
                print(f"发件人: {message['from']['emailAddress']['address']}")
                print(f"日期: {message['receivedDateTime']}")
                print("-" * 50)
            url = data.get('@odata.nextLink')
            print(url)
        else:
            print(f"错误: {response.status_code}", response.text)
            break
