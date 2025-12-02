# Insurance Provider Architecture

This module provides a generic, extensible architecture for integrating with multiple insurance company APIs. The system uses a provider pattern that allows easy addition of new insurance companies without modifying existing code.

## Architecture Overview

The provider system consists of:

1. **Base Class** (`base.py`): Abstract interface that all providers must implement
2. **Provider Implementations**: Concrete implementations for each insurance company (e.g., `fwd_provider.py`)
3. **Factory** (`factory.py`): Creates provider instances based on configuration
4. **Configuration** (`Config.py`): Centralized configuration for all providers

## Current Providers

- **FWD**: FWD Insurance Company API integration

## Adding a New Provider

To add support for a new insurance company, follow these steps:

### Step 1: Create Provider Class

Create a new file `{company_name}_provider.py` in the `data/providers/` directory:

```python
from typing import List, Optional
from data.providers.base import InsuranceProvider
from common.logger import logger

class CompanyBProvider(InsuranceProvider):
    """
    Company B Insurance API Provider
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        # Initialize provider-specific components
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url')
        # ... other initialization
    
    def authenticate(self) -> bool:
        """Authenticate with Company B API"""
        try:
            # Implement authentication logic
            return True
        except Exception as e:
            logger.error(f"Company B authentication failed: {e}")
            return False
    
    def get_agent_id(self, policy_no: str) -> Optional[str]:
        """Get agent ID for a policy number"""
        # Implement API call to get agent ID
        pass
    
    def get_document_list(self, policy_no: str) -> List[str]:
        """Get list of document reference numbers"""
        # Implement API call to get document list
        pass
    
    def download_document(self, document_ref_no: str, document_folder: str) -> None:
        """Download a document by reference number"""
        # Implement API call to download document
        pass
```

### Step 2: Register Provider in Factory

Update `factory.py` to register your new provider:

```python
from data.providers.company_b_provider import CompanyBProvider

class ProviderFactory:
    _providers = {
        'FWD': FWDProvider,
        'COMPANY_B': CompanyBProvider,  # Add your provider here
    }
    # ... rest of factory code
```

### Step 3: Add Configuration

Add provider configuration to `Config.py`:

```python
PROVIDER_CONFIGS = {
    'FWD': {
        # ... existing FWD config
    },
    'COMPANY_B': {
        'name': 'COMPANY_B',
        'base_url': 'https://api.companyb.com',
        'api_key': 'your_api_key_here',
        # ... other company-specific settings
    },
}
```

### Step 4: Update Provider Module Exports

Update `__init__.py` to export your new provider:

```python
from .company_b_provider import CompanyBProvider

__all__ = ['InsuranceProvider', 'FWDProvider', 'CompanyBProvider', 'ProviderFactory']
```

### Step 5: Switch Provider (Optional)

To use the new provider, update `Config.py`:

```python
ACTIVE_PROVIDER = 'COMPANY_B'  # Change from 'FWD' to your provider
```

## Provider Interface Requirements

All providers must implement these methods from `InsuranceProvider`:

### Required Methods

1. **`authenticate() -> bool`**
   - Authenticate with the insurance company's API
   - Should be called during initialization
   - Returns `True` if successful, `False` otherwise

2. **`get_agent_id(policy_no: str) -> Optional[str]`**
   - Retrieve agent ID (LoginName) for a given policy number
   - Returns agent ID string or `None` if not found

3. **`get_document_list(policy_no: str) -> List[str]`**
   - Retrieve list of document reference numbers for a policy
   - Returns list of document reference number strings
   - Should filter out excluded document codes if applicable

4. **`download_document(document_ref_no: str, document_folder: str) -> None`**
   - Download a document by its reference number
   - Save the document to the specified folder
   - Handle file type detection and naming

### Optional Overrides

- **`get_excluded_document_codes() -> List[str]`**
  - Override to provide provider-specific document codes to exclude
  - Default implementation returns empty list

## Configuration Structure

Each provider configuration should include:

- **`name`**: Provider identifier (must match factory key)
- **`base_url`**: Base API URL
- Provider-specific authentication credentials
- Provider-specific API settings
- **`excluded_document_codes`**: (Optional) List of document codes to exclude

## Example: Complete Provider Implementation

See `fwd_provider.py` for a complete reference implementation that includes:

- OAuth2 authentication with token refresh
- Encrypted request/response handling
- Error handling and retry logic
- Document filtering
- File download and saving

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks and log errors
2. **Logging**: Use the logger module to log important operations
3. **Token Management**: If using OAuth, implement automatic token refresh
4. **Configuration**: Store all provider-specific settings in `Config.py`
5. **Documentation**: Add docstrings explaining provider-specific behavior
6. **Testing**: Create test files for your provider before production use

## Backward Compatibility

The old `Net` class is still available for backward compatibility but is deprecated. New code should use the provider pattern. The system maintains backward compatibility by:

- Keeping old `Config.py` variables (deprecated)
- Old code using `Net` class will continue to work
- Gradual migration path to new provider system

## Migration Guide

To migrate existing code from `Net` to providers:

**Old Code:**
```python
from data.Net import Net

net = Net()
agent_id = net.getAgentIdForLoginName(policy_no)
documents = net.getDocumentList(policy_no)
net.downloadDoc(doc_no, folder)
```

**New Code:**
```python
from Config import ACTIVE_PROVIDER, get_provider_config
from data.providers.factory import ProviderFactory

config = get_provider_config(ACTIVE_PROVIDER)
provider = ProviderFactory.create_provider(ACTIVE_PROVIDER, config)
agent_id = provider.get_agent_id(policy_no)
documents = provider.get_document_list(policy_no)
provider.download_document(doc_no, folder)
```

## Support

For questions or issues with the provider system, refer to:
- Base class documentation: `base.py`
- FWD implementation example: `fwd_provider.py`
- Factory implementation: `factory.py`

