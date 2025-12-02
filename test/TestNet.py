import imaplib

import requests
from data.Net import Net
from data.Email import Email
from data.Encrypt import Encrypt
import json
from common.logger import logger
from Config import Debug
from data.Db import Db
from O365 import Account, FileSystemTokenBackend
from common.logger import logger
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from email.mime.application import MIMEApplication


def testgetToken():
    print("runTest")
    net = Net()
    token = net.getTokenForTest()
    print(token)


def testPolicyInfo():
    print("testPolicyInfo")
    net = Net()
    net.getAgentIdForLoginName('85485832')


def testgettokenandpolicyinfo():
    print("testgettokenandpolicyinfo")
    net = Net()
    token = net.getToken()
    print(token)
    net.getAgentIdForLoginName('85485832', token)


def testEncryptParamAndToJson():
    print("testEncryptAndToJson")
    encrypt = Encrypt()
    # filePath = encrypt.encryptParam({'policyNo':'85485832'})
    filePath = encrypt.encryptParam(
        {'documentRefNo': '675a93ae927484f3e4f2ed59'})
    encryptPayload = None
    with open(filePath, 'r') as f:
        encryptPayload = f.read()
    payload = {
        'channel': 'BKE',
        'extCode': 'AMG',
        'lang': 'EN',
        'location': 'HK',
        'timestamp': 0,
        'encryptPayload': encryptPayload,
    }
    print(json.dumps(payload, indent=4))


def testDecrypt():
    print("testDecrypt")
    encrypt = Encrypt()
    encrypt.decryptParam('list.txt', 'decrypt_out.txt')
    # encrypt.decryptParam('decrypt_documentlist.txt','decrypt_documentlist_out.txt')
    decryptPayload = None
    with open('decrypt_out2.txt', 'r') as f:
        decryptPayload = f.read()
    print(decryptPayload)
    print('end>>>')


def testgetDocumentList():
    print("testgetDocumentList")
    net = Net()
    # token = net.getTokenForTest()
    # print(token)
    net.getDocumentList( '85485832')


def testgetPolicyInfo():
    print("testgetPolicyInfo")
    net = Net()
    net.getAgentIdForLoginName('85485832')


def testGetDocument():
    print("testGetDocument")
    net = Net()
    token = net.getTokenForTest()
    print(token)
    # 根据上下文中的 documentRefNo 示例使用
    document_ref_no = "675a93ae927484f3e4f2ed59"
    net.downloadDoc(token, document_ref_no)


def test_decrypt_document():
    print("testDecrypt")
    encrypt = Encrypt()
    encrypt.decryptParam('document_encrypted.txt',
                         'document_encrypted_out.txt')


def string2Pdf():
    import base64
    # 从文本文件中读取 base64 编码的字符串
    with open('document_file_content.txt', 'r') as file:
        base64_string = file.read().strip()  # 使用 .strip() 去除换行符和空格
    # 解码 base64 字符串
    pdf_data = base64.b64decode(base64_string)
    # 将解码后的数据保存到 PDF 文件
    with open('document_file_content.pdf', 'wb') as pdf_file:
        pdf_file.write(pdf_data)
    print("PDF 文件已保存为 'document_file_content.pdf'")


def testGetStaffEmail():
    print("测试获取员工db信息")
    db = Db()
    staff = db.getStaffEmail('Y0987W')
    if staff:
        print(f'员工邮箱: {staff.EmailAddress}')
    else:
        print('未找到员工信息')

def testGetEmailPolicyNo():
    print("测试从邮件获取保单号")

    # 使用一个过去的时间戳作为测试
    timestamp_before = 1704067200  # 2024-01-01 00:00:00

    pending_policy = []

    try:
        token_backend = FileSystemTokenBackend(
            token_path=MAIL_CREDENTIALS['token_path'], token_filename=MAIL_CREDENTIALS['token_filename'])
        account = Account(credentials=(
            MAIL_CREDENTIALS['client_id'], MAIL_CREDENTIALS['client_secret']))
        inbox = account.mailbox().inbox_folder()
        folder = inbox.get_folder(folder_name='New Business')
        messages = folder.get_messages(limit=99)
        for message in messages:
            logger.info(
                f"Message info - Subject: {message.subject}, Created: {message.created}, Received: {message.received}, Sender: {message.sender.address}, To: {message.to.addresses}")
        logger.info("Fetched pending policies from email.")
    except Exception as e:
        logger.error(f"Failed to fetch policies from email: {e}")
    return pending_policy


def testGetLatestEmails1():
    print("测试获取最新10封邮件")
    try:
        # # 连接到SMTP服务器
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.starttls()
        server.login('life-enquiry@amgwealth.com', 'awm21089$')

        # 使用IMAP获取邮件
        imap_server = "outlook.office365.com"
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login('life-enquiry@amgwealth.com', 'awm21089$')

        # 选择收件箱
        imap.select('INBOX')

        # 搜索所有邮件并获取最新的10封
        _, message_numbers = imap.search(None, 'ALL')
        email_ids = message_numbers[0].split()
        latest_emails = email_ids[-10:] if len(email_ids) > 10 else email_ids

        # 获取每封邮件的详细信息
        for email_id in latest_emails:
            _, msg_data = imap.fetch(email_id, '(RFC822)')
            email_body = msg_data[0][1]
            from email import message_from_bytes
            message = message_from_bytes(email_body)

            print(f"\n主题: {message['subject']}")
            print(f"发件人: {message['from']}")
            print(f"日期: {message['date']}")

        # 关闭连接
        imap.close()
        imap.logout()
        print("\n成功获取最新10封邮件")

    except Exception as e:
        print(f"获取邮件时发生错误: {e}")


def testGetLatestEmails2():
    # 使用IMAP获取最新的10封邮件
    try:
        imap_server = "outlook.office365.com"
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login('life-enquiry@amgwealth.com', 'awm21089$')

        # 选择收件箱
        imap.select('INBOX')

        # 搜索所有邮件并获取最新的10封
        _, message_numbers = imap.search(None, 'ALL')
        email_ids = message_numbers[0].split()
        latest_emails = email_ids[-10:] if len(email_ids) > 10 else email_ids

        # 获取每封邮件的详细信息
        for email_id in latest_emails:
            _, msg_data = imap.fetch(email_id, '(RFC822)')
            email_body = msg_data[0][1]
            message = message_from_bytes(email_body)

            print(f"\n主题: {message['subject']}")
            print(f"发件人: {message['from']}")
            print(f"日期: {message['date']}")

        # 关闭连接
        imap.close()
        imap.logout()
        print("\n成功获取最新10封邮件")

    except Exception as e:
        print(f"获取邮件时发生错误: {e}")


def testGetLatestEmails5():

    # 你的客户端 ID 和客户端密钥（可以从 Azure 获取）
    client_id = 'c8057deb-a24e-484b-bf57-58bd5b196eb4'
    client_secret = '24d06109-8fab-4492-ad71-a12e343bacbf'
#     client id: c8057deb-a24e-484b-bf57-58bd5b196eb4
#  tenant id: abc55ec7-9e75-4a10-9bc8-8d81ca3e32a7
#  secret id: 24d06109-8fab-4492-ad71-a12e343bacbf
#  secret value: Tmh8Q~wLQbrdrNHa.H3Y7wl_w~YKvmuN4GgdAbyN'

    # 设置 Token 存储的路径
    token_backend = FileSystemTokenBackend(
        token_path='.', token_filename='o365_token.txt')
    scopes = ['https://graph.microsoft.com/Mail.Read']  # 使用完整URI格式

    # 使用客户端 ID 和客户端密钥进行身份验证
    credentials = (client_id, client_secret)
    account = Account(credentials, token_backend=token_backend)

    # 如果没有授权（token），则进行授权
    if not account.is_authenticated:
        # 打开浏览器进行授权并获取认证令牌
        auth_url, _ = account.con.get_authorization_url(
            requested_scopes=scopes)
        print(f"请访问此链接进行授权: {auth_url}")
        # 输入认证码（从浏览器中复制授权后的代码）
        token = input("输入授权码：")
        account.con.request_token(token)

    # 获取邮件数据
    mailbox = account.mailbox()

    # 获取最新的10封邮件
    messages = mailbox.get_messages(limit=10)

    # 打印每封邮件的主题和发件人
    for message in messages:
        print(f"主题: {message.subject}")
        print(f"发件人: {message.sender['name']}")
        print(f"收件人: {message.to[0]['name']}")
        print(f"日期: {message.received}")
        print("-" * 50)


def testGetLatestEmails6():
    import msal
    import requests

    # Azure 注册应用的相关信息
    client_id = "c8057deb-a24e-484b-bf57-58bd5b196eb4"
    client_secret = "Tmh8Q~wLQbrdrNHa.H3Y7wl_w~YKvmuN4GgdAbyN"
    tenant_id = "abc55ec7-9e75-4a10-9bc8-8d81ca3e32a7"

    # 获取访问令牌

    authority = f"https://login.microsoftonline.com/{tenant_id}"

    # 创建 MSAL 应用对象
    app = msal.ConfidentialClientApplication(
        client_id, client_credential=client_secret, authority=authority
    )

    # 获取令牌
    token_response = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"])

    if "access_token" in token_response:
        token = token_response["access_token"]
        print("访问令牌:", token_response["access_token"])

        get_all_messages6(token)
        # return token_response["access_token"]
    else:
        print("Error obtaining access token")
        print(token_response)
        # return None


def get_all_messages6(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    user_principal_name = 'life-enquiry@amgwealth.com'
    # url = "https://graph.microsoft.com/v1.0/me/messages"
    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/messages"

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            messages = data.get('value', [])
            for message in messages:
                print(f"Subject: {message['subject']}")
                print(f"From: {message['from']['emailAddress']['address']}")
                print(f"Received: {message['receivedDateTime']}")
                print("-" * 50)

            # 检查是否有更多邮件
            url = data.get('@odata.nextLink')
            print("检查是否有更多邮件 : "+url)
        else:
            print(f"Error fetching messages: {response.status_code}")
            print(response.text)
            break
