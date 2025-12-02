"""
Abstract base class for insurance providers.

This module defines the interface that all insurance company API providers must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class InsuranceProvider(ABC):
    """
    Abstract base class for insurance company API providers.
    
    All insurance company integrations must implement this interface to ensure
    consistent behavior across different providers.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the provider with configuration.
        
        Args:
            config: Dictionary containing provider-specific configuration
        """
        self.config = config
        self.provider_name = config.get('name', 'Unknown')
    
    @abstractmethod
    def get_agent_id(self, policy_no: str) -> Optional[str]:
        """
        Retrieve the agent ID associated with a policy number.
        
        Args:
            policy_no: The policy number to query
            
        Returns:
            Agent ID (LoginName) if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_document_list(self, policy_no: str) -> List[str]:
        """
        Retrieve a list of document reference numbers for a policy.
        
        Args:
            policy_no: The policy number to query
            
        Returns:
            List of document reference numbers
        """
        pass
    
    @abstractmethod
    def download_document(self, document_ref_no: str, document_folder: str) -> None:
        """
        Download a document by its reference number and save it to the specified folder.
        
        Args:
            document_ref_no: The document reference number
            document_folder: The folder path where the document should be saved
        """
        pass
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the insurance company's API.
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    def get_provider_name(self) -> str:
        """
        Get the name of this provider.
        
        Returns:
            Provider name
        """
        return self.provider_name
    
    def get_excluded_document_codes(self) -> List[str]:
        """
        Get list of document codes to exclude when fetching documents.
        
        This can be overridden by subclasses to provide provider-specific exclusions.
        
        Returns:
            List of document codes to exclude
        """
        return []

