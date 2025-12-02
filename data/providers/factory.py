"""
Provider Factory

This module provides a factory for creating insurance provider instances.
"""

from typing import Optional
from common.logger import logger
from data.providers.base import InsuranceProvider
from data.providers.fwd_provider import FWDProvider


class ProviderFactory:
    """
    Factory class for creating insurance provider instances.
    
    This factory pattern allows easy addition of new insurance providers
    without modifying existing code.
    """
    
    # Registry of available providers
    _providers = {
        'FWD': FWDProvider,
        # Add more providers here as they are implemented
        # 'COMPANY_B': CompanyBProvider,
        # 'COMPANY_C': CompanyCProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, config: dict) -> Optional[InsuranceProvider]:
        """
        Create an insurance provider instance.
        
        Args:
            provider_name: Name of the provider (e.g., 'FWD')
            config: Provider-specific configuration dictionary
            
        Returns:
            InsuranceProvider instance if provider exists, None otherwise
            
        Example:
            config = {
                'name': 'FWD',
                'base_url': 'https://apihk.fwd.com.hk',
                'client_id': '...',
                ...
            }
            provider = ProviderFactory.create_provider('FWD', config)
        """
        provider_class = cls._providers.get(provider_name.upper())
        
        if provider_class is None:
            logger.error(f"Unknown provider: {provider_name}. Available providers: {list(cls._providers.keys())}")
            return None
        
        try:
            # Ensure config has the provider name
            config['name'] = provider_name.upper()
            provider = provider_class(config)
            logger.info(f"Created provider: {provider_name}")
            return provider
        except Exception as e:
            logger.error(f"Failed to create provider {provider_name}: {e}")
            return None
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """
        Register a new provider class.
        
        This allows dynamic registration of new providers without modifying
        the factory code.
        
        Args:
            name: Provider name (will be converted to uppercase)
            provider_class: Provider class that implements InsuranceProvider
        """
        if not issubclass(provider_class, InsuranceProvider):
            raise ValueError(f"Provider class must inherit from InsuranceProvider")
        
        cls._providers[name.upper()] = provider_class
        logger.info(f"Registered provider: {name.upper()}")
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get list of available provider names.
        
        Returns:
            List of available provider names
        """
        return list(cls._providers.keys())

