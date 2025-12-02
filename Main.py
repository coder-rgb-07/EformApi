from common.File import File
from data.Email import *
from common.logger import logger
from Config import Debug, ACTIVE_PROVIDER, get_provider_config
from data.Db import Db
from data.providers.factory import ProviderFactory
import os
import sys

from test.TestNet import testgetDocumentList


class Main:

    def __init__(self):
        logger.info(f'Running mode: {"Debug" if Debug else "Release"}')
        File.remove_folder_and_contents(File.getFwdDocFilesFolderPath())
        self.check_jars()

    def check_jars(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        jar_dir = os.path.join(base_path, "lib")
        logger.info("JAR files: %s", os.listdir(jar_dir))

    def makeFileTest(self):
        for i in range(5):
            folder_name = f'Folder_{i + 1}'
            File.createFolderUnder(folder_name, File.getTempFolderPath())
        pass

    def main(self):
        # 1. get policyno from amg emailinbox
        email = Email()
        allPolicyNo = email.getAllPolicyNo()

        if not allPolicyNo:
            logger.info('没有找到任何保单号，停止执行主程序。')
            return
        
        # 2. Initialize insurance provider using factory pattern
        provider_config = get_provider_config(ACTIVE_PROVIDER)
        provider = ProviderFactory.create_provider(ACTIVE_PROVIDER, provider_config)
        
        if provider is None:
            logger.error(f'Failed to initialize insurance provider: {ACTIVE_PROVIDER}')
            return
        
        provider_name = provider.get_provider_name()
        logger.info(f'Using insurance provider: {provider_name}')
        
        db = Db()
        for policy in allPolicyNo:

            policy_no = policy.PolicyNo
            logger.info(f'======== policy_no: {policy_no} ========')

            try:

                # 3. get document info and download document file
                #    by policyno from insurance provider
                agentId = provider.get_agent_id(policy_no)
                logger.info(f'agentId: {agentId}')

                # 4. get adviser email from amg db
                staffEmailAddress = ''
                isEmailExist = True
                staff = db.getStaffEmail(agentId)
                if not staff:
                    logger.error(f'{agentId} : Staff not exist.')
                    staffEmailAddress = 'NoStaff'
                    isEmailExist = False
                else:
                    if staff.EmailAddress is None or staff.EmailAddress == "":
                        logger.error(f'{agentId} : Staff email not found.')
                        staffEmailAddress = 'NoStaffEmail'
                        isEmailExist = False
                    else:
                        staffEmailAddress = staff.EmailAddress

                # 5. create folder for the staff
                fName = f'{provider_name}DocFiles-{agentId}-{policy_no}-{staffEmailAddress}'
                f = File.createFolderUnder(fName, File.getFwdDocFilesFolderPath())

                # 6. download documents
                document_list = provider.get_document_list(policy_no)
                for document_no in document_list:
                    provider.download_document(document_no, f)
                    pass

                emailTitleName = f'{provider_name} E-Application Acknowledgement - {policy_no}'
                
                logger.info(f'Staff email: {staffEmailAddress}, {emailTitleName}')
                # logger.info(f'======== Testing Release mode , not sending email. ========')
                if isEmailExist:
                    logger.info('Sending Email...')
                    success = email.sendEmailToAdviser(to_address=staffEmailAddress, subject=emailTitleName, body='test', documentFolder=f)
                    # success = email.sendEmailToAdviser(to_address='kyleliu@amgwealth.com', subject=emailTitleName, body='test', documentFolder=f)

                    if success:
                        logger.info('Success to send email.')
                        logger.info(f'{staffEmailAddress} exist, delete folder: {fName}.')
                        File.remove_folder_and_contents(f)
                    else:
                        raise Exception("Failed to send email.")
                else:
                    email.deleteItemFromLocalList(policy_no)
                    logger.info(f'{staffEmailAddress} not exist, keep folder: {fName}.')
                
            except Exception as e:
                logger.error(f'Error: {e}')
                email.deleteItemFromLocalList(policy_no)
                continue
        pass

if __name__ == '__main__':
    #

    try:
        Main().main()
    except Exception as e:
        logger.error(f'trycatch Main: {e}')

    #
    # testPolicyInfo()
    # testgettokenandpolicyinfo()
    # testgetToken()
    # test_decrypt_document()
    # string2Pdf()
    # testDecrypt()
    # testGetDocument()
    # testgetDocumentList()
    # testgetPolicyInfo()
    # testGetStaffEmail()
    # testGetEmailPolicyNo()
    # testGetLatestEmails()
    # testGetLatestEmailsUsingAccount()
    # testgetDocumentList()
    pass
