from O365 import Account
from dataclasses import dataclass
from datetime import datetime
from common.logger import logger


@dataclass
class PolicynoEntity:
    PolicyNo: str
    EmailDateCreated: str

def testGetLatestEmailsUsingAccount():
    # 配置应用信息
    client_id = "c8057deb-a24e-484b-bf57-58bd5b196eb4"
    client_secret = "Tmh8Q~wLQbrdrNHa.H3Y7wl_w~YKvmuN4GgdAbyN"
    credentials = (client_id, client_secret)

    # 初始化账户并认证
    account = Account(credentials)
    if not account.is_authenticated:
        # 需要交互式登录（首次认证需浏览器操作）
        account.authenticate(scopes=['basic', 'mail_read'])

    # 获取邮箱
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()
    folder = inbox.get_folder(folder_name='New Business')

    policy_entities = []

    messages = folder.get_messages(limit=1000)
    # message_list = list(messages)  # 将生成器转换为列表
    # print(f"messages 里面有多少个 message: {len(message_list)}")
    for index, message in enumerate(messages):
        if "<policy no." in message.subject:
            # Extract the policy number from the subject (assuming it's a part of the subject text)
            # For simplicity, let's assume it's after "<policy no."
            # You might need to modify the extraction logic based on the actual format of the subject.
            start_index = message.subject.find("<policy no.") + len("<policy no.")
            end_index = message.subject.find(">", start_index)
            policy_no = message.subject[start_index:end_index].strip()

            # Convert the created date to a string if necessary (assuming message.created is a datetime object)
            email_date_created = message.created.strftime('%Y-%m-%d %H:%M:%S') if isinstance(message.created, datetime) else str(message.created)

            # Create PolicynoEntity instance
            policy_entity = PolicynoEntity(PolicyNo=policy_no, EmailDateCreated=email_date_created)

            # Add to the list
            policy_entities.append(policy_entity)

            # Print the details (if needed)
            print(f"Index: {index}, PolicyNo: {policy_no}")
            print(f"Created: {email_date_created}")
            print("--------------------------")
    print("policy_entities >>>")
    logger.info(policy_entities)
    logger.info(f"policy_entities 里面有多少个 policy: {len(policy_entities)}")
    for policy in policy_entities:
        print(f"PolicyNo: {policy.PolicyNo}, EmailDateCreated: {policy.EmailDateCreated}")

