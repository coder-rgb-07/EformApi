import os
import sys
from Config import *
import requests
from common.logger import logger
from data.Encrypt import Encrypt
import base64
import json


class Net:

    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0',
                       'Content-Type': 'application/json'}
        self.useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:68.0) Gecko/20100101 Firefox/68.0 Waterfox/56.6.2022.11'
        self.encrypt = Encrypt()
        self.refresh_token = ''
        self.token = self.__getToken()
        self.target_codes = [
            "0000103A", "0000103B", "0000103C", "0000103D",
            "0000103W", "0000103Y", "0000103Z", "000M103A",
            "000M103W", "0000116A", "0000275A"
        ]
        pass

    def __getToken(self):
        code = self.__getRedirectUrlAndTempCode()
        token = self.__getTokenExe(code)
        logger.info(f"#getToken fetched successfully. {token}")
        return token

    def __refreshToken(self):
        logger.info('refresh token >>>')
        url = f'{host_server}/authorization-api/v1/oauth2/token'
        payload = {
            'grant_type': grant_type_refresh,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': host_server,
            'refresh_token': self.refresh_token,
        }
        response = requests.post(url, headers=self.header, json=payload)
        logger.info(
            f"#refreshToken fetched successfully. {response.json()}")
        r = response.json()
        self.refresh_token = r['refresh_token']
        self.token = r['access_token']
        pass

    def __getRedirectUrlAndTempCode(self):
        url = f'{host_server}/authorization-api/v1/oauth2/authorize'
        payload = {
            'client_id': client_id,
            'response_type': response_type,
            'provision_key': provision_key,
            'authenticated_userid': authenticated_userid,
        }
        response = requests.post(url, headers=self.header, json=payload)
        logger.info(
            f"#getRedirectUrlAndTempCode fetched successfully. {response.json()}")
        code = response.json()['redirect_uri'].split('=')[1]
        logger.info(
            f"Redirect URL and temporary code fetched successfully. {code}")
        return code

    def __getTokenExe(self, code):
        url = f'{host_server}/authorization-api/v1/oauth2/token'
        payload = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': host_server,
            'code': code,
        }
        response = requests.post(url, headers=self.header, json=payload)
        logger.info(f"#getToken fetched successfully. {response.json()}")
        r = response.json()
        self.refresh_token = r['refresh_token']
        return r['access_token']

    def __getHeader(self, access_token):
        return {
            'User-Agent': self.useragent,
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}",
        }

    def __getPayload(self, encryptPayload):
        return {
            'channel': 'BKE',
            'extCode': 'AMG',
            'lang': 'EN',
            'location': 'HK',
            'timestamp': 0,
            'encryptPayload': encryptPayload,
        }

    def getAgentIdForLoginName(self, policy_no):
        data = {
            'policyNo': policy_no
        }
        # 加密
        e = self.encrypt.encryptParam(data)

        # 请求
        url = f'{host_server}/sales-api/v1/application/getPolicyInfo'
        result = self.__request(url, e)

        d = self.encrypt.decryptParam(result['encryptPayload'])
        agent_id = d.get('agentId')
        # logger.info(f"获取到 agentId: {agent_id}")
        return agent_id

    def getPolicyInfo(self, policy_no):
        """
        Get full policy information for a given policy number.
        
        Args:
            policy_no: Policy number to query
            
        Returns:
            Dictionary containing full policy information
            
        Raises:
            Exception: If encryption, API call, or decryption fails
        """
        try:
            logger.info(f"Getting policy info for policy number: {policy_no}")
            data = {
                'policyNo': policy_no
            }
            
            # 加密
            logger.info("Encrypting request payload...")
            e = self.encrypt.encryptParam(data)
            logger.info(f"Encryption successful, encrypted payload length: {len(e)}")

            # 请求
            url = f'{host_server}/sales-api/v1/application/getPolicyInfo'
            logger.info(f"Making API request to: {url}")
            result = self.__request(url, e)
            
            # 检查响应是否包含encryptPayload
            if 'encryptPayload' not in result:
                error_msg = f"API响应中缺少encryptPayload字段。响应内容: {result}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            # 检查encryptPayload是否为空
            if not result['encryptPayload'] or len(result['encryptPayload']) == 0:
                error_msg = f"API响应中的encryptPayload为空。响应内容: {result}"
                logger.error(error_msg)
                raise Exception(error_msg)

            # 解密
            logger.info("Decrypting response payload...")
            d = self.encrypt.decryptParam(result['encryptPayload'])
            logger.info(f"获取到完整保单信息: {json.dumps(d, indent=2, ensure_ascii=False)}")
            return d
            
        except Exception as e:
            error_msg = f"获取保单信息失败 (policy_no: {policy_no}): {str(e)}"
            logger.error(error_msg)
            import traceback
            logger.error(traceback.format_exc())
            raise Exception(error_msg) from e

    def getDocumentList(self, policy_no):
        data = {
            'policyNo': policy_no
        }
        # 加密
        e = self.encrypt.encryptParam(data)
        # 请求
        url = f'{host_server}/sales-api/v1/application/getDocumentList'
        result = self.__request(url, e)
        # 解密
        d = self.encrypt.decryptParam(result['encryptPayload'])
        logger.info(d)
        # 收集所有的 documentRefNoList 中的项
        all_document_ref_no = []
        for policy in d['policyDocumentList']:
            for document in policy['documentList']:
                if self.__isTargetCode(document['documentCode']):
                    all_document_ref_no.extend(document['documentRefNoList'])

        # 将文档引用编号列表转换为 JSON 格式
        json_document_ref_no = json.dumps(all_document_ref_no)
        # 计算文档引用编号的数量
        document_count = len(all_document_ref_no)
        logger.info(f"文档引用编号的数量: {document_count}")
        logger.info(f"文档引用编号列表的 JSON 格式: {json_document_ref_no}")
        print(json_document_ref_no)

        return all_document_ref_no

    def __isTargetCode(self, code):
        return code not in self.target_codes

    def downloadDoc(self, document_no, documentFolder):
        data = {
            'documentRefNo': document_no
        }
        # 加密
        e = self.encrypt.encryptParam(data)
        # 请求
        url = f'{host_server}/sales-api/v1/application/getDocument'
        result = self.__request(url, e)
        # 解密
        d = self.encrypt.decryptParam(result['encryptPayload'])
        # 解码 base64 编码的文件内容
        if 'fileContent' in d:
            document_ref_no = d.get('documentRefNo', '')

            document_file_type = d.get('fileType', '')
            if document_file_type == 'image/jpeg':
                file_suffix = 'jpg'
            elif document_file_type == 'application/pdf':
                file_suffix = 'pdf'
            else:
                logger.warning(f"未知的文件类型: {document_file_type}")

            if file_suffix == 'pdf':
                
                file_path = os.path.join(documentFolder, f'{document_ref_no}.{file_suffix}')
                logger.info(f"获取到文档编号: {document_ref_no}, fileType: {document_file_type}")
                pdf_data = base64.b64decode(d['fileContent'])
                # 将解码后的数据保存到 PDF 文件
                # 检查文件是否已经存在
                file_path = os.path.join(documentFolder, f'{document_ref_no}.{file_suffix}')
                if os.path.exists(file_path):
                    logger.info(f"文件 {document_ref_no}.{file_suffix} 已存在，跳过保存")
                    return
                else:
                    logger.info(f"保存文件 {document_ref_no}.{file_suffix}")
                    # 保存文件
                    with open(file_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_data)

    def __request(self, url, encryptPayload):
        # get the def name who invoke __request
        def_name = sys._getframe(1).f_code.co_name

        try:
            response = requests.post(url, headers=self.__getHeader(
                self.token), json=self.__getPayload(encryptPayload))
            
            # Log response status and headers for debugging
            logger.info(f"#{def_name} API Response Status: {response.status_code}")
            logger.debug(f"#{def_name} API Response Headers: {dict(response.headers)}")
            
            # Check if response is successful
            if response.status_code != 200:
                error_msg = f"#{def_name} API请求失败，HTTP状态码: {response.status_code}"
                logger.error(error_msg)
                logger.error(f"Response body: {response.text}")
                raise Exception(f"{error_msg}\nResponse: {response.text}")
            
            result = response.json()
            
            # Log the raw response (without sensitive data)
            logger.debug(f"#{def_name} API Response (raw): {json.dumps(result, indent=2)}")
            
            # if result contains error, refresh token
            if 'error' in result:
                logger.warning(f"#{def_name} fetched error. {result}")
                logger.info("Attempting to refresh token and retry...")
                self.__refreshToken()
                response = requests.post(url, headers=self.__getHeader(
                    self.token), json=self.__getPayload(encryptPayload))
                
                if response.status_code != 200:
                    error_msg = f"#{def_name} Retry failed, HTTP状态码: {response.status_code}"
                    logger.error(error_msg)
                    logger.error(f"Response body: {response.text}")
                    raise Exception(f"{error_msg}\nResponse: {response.text}")
                
                result = response.json()
                # if result contains error after refresh, raise exception
                if 'error' in result:
                    error_msg = f"#{def_name} fetched error after token refresh. {result}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
            else:
                logger.info(f"#{def_name} fetched successfully.")
            return result
        except requests.exceptions.RequestException as e:
            error_msg = f"#{def_name} 网络请求异常: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"#{def_name} JSON解析失败: {str(e)}\nResponse text: {response.text if 'response' in locals() else 'N/A'}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"#{def_name} 发生未知错误: {str(e)}"
            logger.error(error_msg)
            import traceback
            logger.error(traceback.format_exc())
            raise
