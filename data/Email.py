from dataclasses import dataclass
from O365 import Account, FileSystemTokenBackend
from common.File import File
from common.logger import logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from email.mime.application import MIMEApplication
from datetime import datetime
import os
import json
from data.Entity import PolicynoEntity
import requests
from email.mime.image import MIMEImage


class Email:

    def __init__(self):
        folderPath = File.getLocalDataFolderPath()
        self.locallistpath = folderPath + '/locallist.json'
        t = File.getCurrentTimeFormatted()
        self.locallistpath_remote = folderPath + f'/locallist_remote_{t}.json'
        pass

    # 从邮箱的邮件里面获取PolicyNo
    def getAllPolicyNo(self):
        # New list to save non-matching items
        newlist = []
        remotelist = self.__getRemoteList()
        locallist = self.__getLocalList()
        # Compare the lists
        for remote_item in remotelist:
            # Check if the remote_item is in locallist (by comparing PolicyNo and EmailDateCreated)
            if remote_item not in locallist:
                newlist.append(remote_item)
        self.__saveLocalList(locallist, newlist)
        # logger  newlist
        logger.info(f'getAllPolicyNo: {newlist}')
        return newlist

    def deleteItemFromLocalList(self, policyNo):
        # Read the existing JSON data from the file then delete the item by PolicyNo and save it back to the file
        jsonFilePath = self.locallistpath
        # Read the existing JSON data from the file
        with open(jsonFilePath, 'r') as file:
            data = json.load(file)
        # Find the item by PolicyNo and remove it
        data = [item for item in data if item.get('PolicyNo') != policyNo]
        # Save the updated data back to the file
        with open(jsonFilePath, 'w') as file:
            json.dump(data, file, indent=4)

    def __saveLocalList(self, locallist, newlist):
        jsonFilePath = self.locallistpath
        # Remove the old data (delete the file) before saving the new data
        if os.path.exists(jsonFilePath):
            os.remove(jsonFilePath)

        # Combine lists A and B (no duplicates, as they don't overlap)
        combined_list = locallist + newlist

        # Convert combined list of PolicynoEntity objects to dictionaries
        data_to_save = [
            {"PolicyNo": entity.PolicyNo, "EmailDateCreated": entity.EmailDateCreated}
            for entity in combined_list
        ]

        # Save the combined list back to the file in JSON format
        with open(jsonFilePath, 'w') as file:
            json.dump(data_to_save, file, indent=4)

    # save all latest emails in remote email_inbox
    def __saveRemoteList(self, remoteList):
        data_to_save = [
            {"PolicyNo": entity.PolicyNo, "EmailDateCreated": entity.EmailDateCreated}
            for entity in remoteList
        ]
        with open(self.locallistpath_remote, 'w') as file:
            json.dump(data_to_save, file, indent=4)

    def __getRemoteList(self):
        # 配置应用信息 - Load from environment variables
        client_id = os.getenv('O365_CLIENT_ID', '')
        client_secret = os.getenv('O365_CLIENT_SECRET', '')
        
        if not client_id or not client_secret:
            raise ValueError(
                "O365_CLIENT_ID and O365_CLIENT_SECRET environment variables are required. "
                "Please set them in your .env file or environment variables."
            )
        
        credentials = (client_id, client_secret)

        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""
        os.environ["no_proxy"] = "*"

        # 方法2：修改 requests 默认会话配置
        session = requests.Session()
        session.trust_env = False  # 不读取系统代理配置
        # 初始化令牌存储后端（不传递任何额外参数）
        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')

        # 正确初始化 Account
        account = Account(
            credentials,
            # auth_flow_type='public',  # 根据应用类型选择 'public' 或 'confidential'
            token_backend=token_backend,
            requests_ops={'session': session}  # 关键：在此处传递 session
        )

        if not account.is_authenticated:
            # 需要交互式登录（首次认证需浏览器操作）
            account.authenticate(scopes=['basic', 'mail_read'])

        # 获取邮箱
        mailbox = account.mailbox()
        inbox = mailbox.inbox_folder()
        folder = inbox.get_folder(folder_name='New Business')
        policy_entities = []
        messages = folder.get_messages(limit=1000)

        for index, message in enumerate(messages):
            if "<policy no." in message.subject:
                start_index = message.subject.find(
                    "<policy no.") + len("<policy no.")
                end_index = message.subject.find(">", start_index)
                policy_no = message.subject[start_index:end_index].strip()
                email_date_created = message.created.strftime('%Y-%m-%d %H:%M:%S') if isinstance(message.created,
                                                                                                 datetime) else str(
                    message.created)
                policy_entity = PolicynoEntity(
                    PolicyNo=policy_no, EmailDateCreated=email_date_created)
                policy_entities.append(policy_entity)
        self.__saveRemoteList(policy_entities)
        return policy_entities

    def __getLocalList(self):
        jsonFilePath = self.locallistpath
        # Step 1: Check if the file exists
        if not os.path.exists(jsonFilePath):
            # If not, create the file with an empty string
            with open(jsonFilePath, 'w') as file:
                file.write('')

        # Step 2: Read the content from the file
        with open(jsonFilePath, 'r') as file:
            content = file.read().strip()

            # If the file is empty, ensure it's an empty string
            if not content:
                content = ''

            # Step 3: Parse content as JSON (empty JSON object if blank)
            try:
                data = json.loads(content) if content else []
            except json.JSONDecodeError:
                # If content is not valid JSON, treat it as an empty object
                data = []

            # Convert the parsed data to a list of PolicynoEntity instances
            policy_entities = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'PolicyNo' in item and 'EmailDateCreated' in item:
                        policy_entity = PolicynoEntity(
                            PolicyNo=item['PolicyNo'],
                            EmailDateCreated=item['EmailDateCreated']
                        )
                        policy_entities.append(policy_entity)

            return policy_entities

    def sendEmailToAdviser2(self, to_address, subject, body="None", documentFolder=None):
        try:
            # Load SMTP credentials from environment variables
            smtp_email = os.getenv('SMTP_EMAIL', '')
            smtp_password = os.getenv('SMTP_PASSWORD', '')
            
            if not smtp_email or not smtp_password:
                raise ValueError(
                    "SMTP_EMAIL and SMTP_PASSWORD environment variables are required. "
                    "Please set them in your .env file or environment variables."
                )
            
            # 创建邮件对象
            mail = MIMEMultipart()
            mail['From'] = smtp_email
            mail['To'] = to_address
            mail['Subject'] = subject

            path = os.path.join(File.getExeProjectRootPath(), 'FWDEmailBody')
            path = os.path.join(path, 'FWDEmailBody.txt')
            with open(path, 'r', encoding='utf-8') as file:
                    body = file.read()

            # 添加邮件正文
            mime_html = MIMEText(body, 'html')
            mail.attach(mime_html)

            # add all files in documentFolder
            if documentFolder:
                for file_path in Path(documentFolder).glob('*'):
                    if file_path.is_file():
                        with open(file_path, 'rb') as f:
                            attachment = MIMEApplication(f.read(), _subtype='pdf')
                            attachment.add_header('Content-Disposition', 'attachment', filename=file_path.name)
                            mail.attach(attachment)

            # get the only one zip file in documentFolder
            # for file_path in Path(documentFolder).glob('*.zip'):
            #     if file_path.is_file():
            #         with open(file_path, 'rb') as f:
            #             attachment = MIMEApplication(f.read(), _subtype='zip')
            #             attachment.add_header('Content-Disposition', 'attachment', filename=file_path.name)
            #             mail.attach(attachment)

            # 发送邮件
            s = smtplib.SMTP(host='smtp.office365.com', port=587)
            s.starttls()
            s.login(smtp_email, smtp_password)
            s.send_message(mail)
            del mail
            s.quit()

            logger.info(f"邮件已发送至 {to_address}")
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            raise  # 重新抛出异常以便上层处理

    def sendEmailToAdviser(self, to_address, subject, body="None", documentFolder=None):
        try:
            # Load SMTP credentials from environment variables
            smtp_email = os.getenv('SMTP_EMAIL', '')
            smtp_password = os.getenv('SMTP_PASSWORD', '')
            
            if not smtp_email or not smtp_password:
                raise ValueError(
                    "SMTP_EMAIL and SMTP_PASSWORD environment variables are required. "
                    "Please set them in your .env file or environment variables."
                )
            
            # 创建邮件对象
            mail = MIMEMultipart('related')
            mail['From'] = smtp_email
            mail['To'] = to_address
            mail['Subject'] = subject

            path1 = os.path.join(File.getExeProjectRootPath(), 'FWDEmailBody')
            path = os.path.join(path1, 'FWDEmailBody.txt')
            with open(path, 'r', encoding='utf-8') as file:
                    body = file.read()

            # 添加邮件正文
            mime_html = MIMEText(body, 'html')
            mail.attach(mime_html)

            # 添加图片
            img_path = os.path.join(path1, 'image.png')
            if not os.path.exists(img_path):
                 raise FileNotFoundError(f"图片文件不存在: {img_path}")
            
            with open(img_path, 'rb') as img_file:
                mime_img = MIMEImage(img_file.read(), _subtype='jpeg')
                mime_img.add_header('Content-ID', '<image1>')
                mail.attach(mime_img)

            # add all files in documentFolder
            if documentFolder:
                for file_path in Path(documentFolder).glob('*'):
                    if file_path.is_file():
                        with open(file_path, 'rb') as f:
                            attachment = MIMEApplication(f.read(), _subtype='pdf')
                            attachment.add_header('Content-Disposition', 'attachment', filename=file_path.name)
                            mail.attach(attachment)

            # 发送邮件
            s = smtplib.SMTP(host='smtp.office365.com', port=587)
            s.starttls()
            s.login(smtp_email, smtp_password)
            s.send_message(mail)
            del mail
            s.quit()

            logger.info(f"邮件已发送至 {to_address}")
            return True
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False
