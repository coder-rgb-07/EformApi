"""
Template for creating a new insurance provider.

Copy this file and rename it to {company_name}_provider.py, then implement
all the required methods according to the insurance company's API documentation.
"""

from typing import List, Optional
from common.logger import logger
from data.providers.base import InsuranceProvider


class TemplateProvider(InsuranceProvider):
    """
    Template Insurance Provider
    
    This is a template class. Replace all template code with your actual
    implementation based on the insurance company's API.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the provider with configuration.
        
        Args:
            config: Dictionary containing provider-specific configuration
        """
        super().__init__(config)
        
        # Extract configuration values
        self.base_url = config.get('base_url')
        self.api_key = config.get('api_key')  # Example: API key authentication
        # Add other configuration values as needed
        
        # Initialize provider-specific components
        # Example: HTTP client, encryption handler, etc.
        
        # Authenticate on initialization
        if not self.authenticate():
            raise Exception(f"Failed to authenticate with {self.provider_name}")
    
    def authenticate(self) -> bool:
        """
        Authenticate with the insurance company's API.
        
        Implement authentication logic here. This could be:
        - API key validation
        - OAuth2 token generation
        - Session creation
        - etc.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # TODO: Implement authentication logic
            # Example:
            # response = requests.post(f"{self.base_url}/auth", headers={"X-API-Key": self.api_key})
            # if response.status_code == 200:
            #     self.token = response.json()['token']
            #     return True
            
            logger.info(f"{self.provider_name}: Authentication successful")
            return True
        except Exception as e:
            logger.error(f"{self.provider_name}: Authentication failed: {e}")
            return False
    
    def get_agent_id(self, policy_no: str) -> Optional[str]:
        """
        Retrieve the agent ID associated with a policy number.
        
        Args:
            policy_no: The policy number to query
            
        Returns:
            Agent ID (LoginName) if found, None otherwise
        """
        try:
            # TODO: Implement API call to get agent ID
            # Example:
            # response = requests.get(
            #     f"{self.base_url}/policies/{policy_no}/agent",
            #     headers={"Authorization": f"Bearer {self.token}"}
            # )
            # if response.status_code == 200:
            #     data = response.json()
            #     return data.get('agentId')
            
            logger.info(f"{self.provider_name}: Retrieved agent ID for policy {policy_no}")
            return None  # Replace with actual implementation
        except Exception as e:
            logger.error(f"{self.provider_name}: Failed to get agent ID for {policy_no}: {e}")
            return None
    
    def get_document_list(self, policy_no: str) -> List[str]:
        """
        Retrieve a list of document reference numbers for a policy.
        
        Args:
            policy_no: The policy number to query
            
        Returns:
            List of document reference numbers
        """
        try:
            # TODO: Implement API call to get document list
            # Example:
            # response = requests.get(
            #     f"{self.base_url}/policies/{policy_no}/documents",
            #     headers={"Authorization": f"Bearer {self.token}"}
            # )
            # if response.status_code == 200:
            #     data = response.json()
            #     documents = data.get('documents', [])
            #     # Filter excluded codes if needed
            #     excluded_codes = self.get_excluded_document_codes()
            #     return [
            #         doc['refNo'] for doc in documents
            #         if doc.get('code') not in excluded_codes
            #     ]
            
            logger.info(f"{self.provider_name}: Retrieved document list for policy {policy_no}")
            return []  # Replace with actual implementation
        except Exception as e:
            logger.error(f"{self.provider_name}: Failed to get document list for {policy_no}: {e}")
            return []
    
    def download_document(self, document_ref_no: str, document_folder: str) -> None:
        """
        Download a document by its reference number and save it to the specified folder.
        
        Args:
            document_ref_no: The document reference number
            document_folder: The folder path where the document should be saved
        """
        try:
            # TODO: Implement API call to download document
            # Example:
            # response = requests.get(
            #     f"{self.base_url}/documents/{document_ref_no}",
            #     headers={"Authorization": f"Bearer {self.token}"}
            # )
            # if response.status_code == 200:
            #     # Determine file type from response headers or content
            #     content_type = response.headers.get('Content-Type', 'application/pdf')
            #     if 'pdf' in content_type:
            #         file_suffix = 'pdf'
            #     elif 'jpeg' in content_type or 'jpg' in content_type:
            #         file_suffix = 'jpg'
            #     else:
            #         logger.warning(f"Unknown file type: {content_type}")
            #         return
            #     
            #     file_path = os.path.join(document_folder, f"{document_ref_no}.{file_suffix}")
            #     if os.path.exists(file_path):
            #         logger.info(f"File already exists: {file_path}")
            #         return
            #     
            #     with open(file_path, 'wb') as f:
            #         f.write(response.content)
            #     logger.info(f"Downloaded document: {file_path}")
            
            logger.info(f"{self.provider_name}: Downloaded document {document_ref_no}")
        except Exception as e:
            logger.error(f"{self.provider_name}: Failed to download document {document_ref_no}: {e}")
            raise
    
    def get_excluded_document_codes(self) -> List[str]:
        """
        Get list of document codes to exclude when fetching documents.
        
        Override this method if your provider has specific document codes to exclude.
        
        Returns:
            List of document codes to exclude
        """
        # Get from config if provided, otherwise return empty list
        return self.config.get('excluded_document_codes', [])

