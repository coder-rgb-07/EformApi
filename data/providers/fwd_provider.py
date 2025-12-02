"""
FWD Insurance Provider Implementation

This module implements the InsuranceProvider interface for FWD insurance company.
"""

import os
import sys
import requests
import base64
import json
from typing import List, Optional
from common.logger import logger
from data.providers.base import InsuranceProvider
from data.Encrypt import Encrypt


class FWDProvider(InsuranceProvider):
    """
    FWD Insurance Company API Provider
    
    Implements the InsuranceProvider interface for FWD's API system.
    Uses OAuth2 authentication and encrypted payloads.
    """
    
    def __init__(self, config: dict):
        """
        Initialize FWD provider with configuration.
        
        Args:
            config: Dictionary containing FWD-specific configuration:
                - base_url: Base API URL (e.g., "https://apihk.fwd.com.hk")
                - client_id: OAuth2 client ID
                - client_secret: OAuth2 client secret
                - provision_key: Provision key for authorization
                - authenticated_userid: Service account user ID
                - grant_type: OAuth2 grant type (default: "authorization_code")
                - grant_type_refresh: Refresh token grant type (default: "refresh_token")
                - response_type: OAuth2 response type (default: "code")
                - excluded_document_codes: List of document codes to exclude
        """
        super().__init__(config)
        
        # Extract configuration
        self.base_url = config.get('base_url', 'https://apihk.fwd.com.hk')
        self.client_id = config.get('client_id')
        self.client_secret = config.get('client_secret')
        self.provision_key = config.get('provision_key')
        self.authenticated_userid = config.get('authenticated_userid')
        self.grant_type = config.get('grant_type', 'authorization_code')
        self.grant_type_refresh = config.get('grant_type_refresh', 'refresh_token')
        self.response_type = config.get('response_type', 'code')
        
        # Initialize components
        self.header = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json'
        }
        self.useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:68.0) Gecko/20100101 Firefox/68.0 Waterfox/56.6.2022.11'
        self.encrypt = Encrypt()
        self.refresh_token = ''
        self.token = None
        
        # Document codes to exclude (FWD-specific)
        self.excluded_document_codes = config.get('excluded_document_codes', [
            "0000103A", "0000103B", "0000103C", "0000103D",
            "0000103W", "0000103Y", "0000103Z", "000M103A",
            "000M103W", "0000116A", "0000275A"
        ])
        
        # Authenticate on initialization
        self.authenticate()
    
    def authenticate(self) -> bool:
        """
        Authenticate with FWD API using OAuth2.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.token = self._get_token()
            logger.info(f"FWD authentication successful. Token fetched.")
            return True
        except Exception as e:
            logger.error(f"FWD authentication failed: {e}")
            return False
    
    def _get_token(self) -> str:
        """Get access token from FWD API."""
        code = self._get_authorization_code()
        token = self._exchange_code_for_token(code)
        logger.info(f"FWD token fetched successfully.")
        return token
    
    def _get_authorization_code(self) -> str:
        """Get authorization code from FWD API."""
        url = f'{self.base_url}/authorization-api/v1/oauth2/authorize'
        payload = {
            'client_id': self.client_id,
            'response_type': self.response_type,
            'provision_key': self.provision_key,
            'authenticated_userid': self.authenticated_userid,
        }
        response = requests.post(url, headers=self.header, json=payload)
        logger.info(f"FWD authorization code fetched successfully.")
        code = response.json()['redirect_uri'].split('=')[1]
        return code
    
    def _exchange_code_for_token(self, code: str) -> str:
        """Exchange authorization code for access token."""
        url = f'{self.base_url}/authorization-api/v1/oauth2/token'
        payload = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.base_url,
            'code': code,
        }
        response = requests.post(url, headers=self.header, json=payload)
        logger.info(f"FWD token exchange successful.")
        r = response.json()
        self.refresh_token = r['refresh_token']
        return r['access_token']
    
    def _refresh_token(self) -> None:
        """Refresh the access token."""
        logger.info('FWD: Refreshing token...')
        url = f'{self.base_url}/authorization-api/v1/oauth2/token'
        payload = {
            'grant_type': self.grant_type_refresh,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.base_url,
            'refresh_token': self.refresh_token,
        }
        response = requests.post(url, headers=self.header, json=payload)
        logger.info(f"FWD token refresh successful.")
        r = response.json()
        self.refresh_token = r['refresh_token']
        self.token = r['access_token']
    
    def _get_header(self, access_token: str) -> dict:
        """Get request headers with authorization."""
        return {
            'User-Agent': self.useragent,
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}",
        }
    
    def _get_payload(self, encrypt_payload: str) -> dict:
        """Get standard payload structure for FWD API."""
        return {
            'channel': 'BKE',
            'extCode': 'AMG',
            'lang': 'EN',
            'location': 'HK',
            'timestamp': 0,
            'encryptPayload': encrypt_payload,
        }
    
    def _request(self, url: str, encrypt_payload: str) -> dict:
        """
        Make a request to FWD API with automatic token refresh on error.
        
        Args:
            url: API endpoint URL
            encrypt_payload: Encrypted payload string
            
        Returns:
            Response JSON as dictionary
        """
        def_name = sys._getframe(1).f_code.co_name
        
        response = requests.post(
            url,
            headers=self._get_header(self.token),
            json=self._get_payload(encrypt_payload)
        )
        result = response.json()
        
        # If error, try refreshing token once
        if 'error' in result:
            logger.info(f"FWD {def_name} error. Attempting token refresh...")
            self._refresh_token()
            response = requests.post(
                url,
                headers=self._get_header(self.token),
                json=self._get_payload(encrypt_payload)
            )
            result = response.json()
            if 'error' in result:
                logger.error(f"FWD {def_name} error after refresh: {result}")
                raise Exception(f"FWD API error: {result}")
        else:
            logger.info(f"FWD {def_name} successful.")
        
        return result
    
    def get_agent_id(self, policy_no: str) -> Optional[str]:
        """
        Get agent ID for a policy number.
        
        Args:
            policy_no: Policy number
            
        Returns:
            Agent ID if found, None otherwise
        """
        data = {'policyNo': policy_no}
        
        # Encrypt request
        encrypted = self.encrypt.encryptParam(data)
        
        # Make request
        url = f'{self.base_url}/sales-api/v1/application/getPolicyInfo'
        result = self._request(url, encrypted)
        
        # Decrypt response
        decrypted = self.encrypt.decryptParam(result['encryptPayload'])
        agent_id = decrypted.get('agentId')
        
        return agent_id
    
    def get_document_list(self, policy_no: str) -> List[str]:
        """
        Get list of document reference numbers for a policy.
        
        Args:
            policy_no: Policy number
            
        Returns:
            List of document reference numbers (excluding excluded codes)
        """
        data = {'policyNo': policy_no}
        
        # Encrypt request
        encrypted = self.encrypt.encryptParam(data)
        
        # Make request
        url = f'{self.base_url}/sales-api/v1/application/getDocumentList'
        result = self._request(url, encrypted)
        
        # Decrypt response
        decrypted = self.encrypt.decryptParam(result['encryptPayload'])
        logger.info(f"FWD document list response: {decrypted}")
        
        # Collect all document reference numbers
        all_document_ref_no = []
        for policy in decrypted.get('policyDocumentList', []):
            for document in policy.get('documentList', []):
                document_code = document.get('documentCode')
                if self._is_target_code(document_code):
                    all_document_ref_no.extend(document.get('documentRefNoList', []))
        
        document_count = len(all_document_ref_no)
        logger.info(f"FWD: Found {document_count} documents for policy {policy_no}")
        
        return all_document_ref_no
    
    def _is_target_code(self, code: str) -> bool:
        """Check if document code should be included (not in excluded list)."""
        return code not in self.excluded_document_codes
    
    def download_document(self, document_ref_no: str, document_folder: str) -> None:
        """
        Download a document by reference number.
        
        Args:
            document_ref_no: Document reference number
            document_folder: Folder path to save the document
        """
        data = {'documentRefNo': document_ref_no}
        
        # Encrypt request
        encrypted = self.encrypt.encryptParam(data)
        
        # Make request
        url = f'{self.base_url}/sales-api/v1/application/getDocument'
        result = self._request(url, encrypted)
        
        # Decrypt response
        decrypted = self.encrypt.decryptParam(result['encryptPayload'])
        
        # Process document
        if 'fileContent' in decrypted:
            document_ref_no = decrypted.get('documentRefNo', '')
            document_file_type = decrypted.get('fileType', '')
            
            # Determine file extension
            if document_file_type == 'image/jpeg':
                file_suffix = 'jpg'
            elif document_file_type == 'application/pdf':
                file_suffix = 'pdf'
            else:
                logger.warning(f"FWD: Unknown file type: {document_file_type}")
                return
            
            # Build file path
            file_path = os.path.join(document_folder, f'{document_ref_no}.{file_suffix}')
            
            # Skip if file already exists
            if os.path.exists(file_path):
                logger.info(f"FWD: File {document_ref_no}.{file_suffix} already exists, skipping")
                return
            
            # Decode and save file
            logger.info(f"FWD: Saving document {document_ref_no}.{file_suffix}")
            pdf_data = base64.b64decode(decrypted['fileContent'])
            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(pdf_data)
    
    def get_excluded_document_codes(self) -> List[str]:
        """Get list of excluded document codes."""
        return self.excluded_document_codes

