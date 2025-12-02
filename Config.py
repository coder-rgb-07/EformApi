# ============================================================================
# Application Configuration
# ============================================================================

import os
from pathlib import Path

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env file from project root
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, use environment variables directly
    pass

# Debug Mode
# Can be set via environment variable DEBUG=true or DEBUG=1
debug_env = os.getenv('DEBUG', '').lower()
Debug = debug_env in ('true', '1', 'yes') if debug_env else False
Release = not Debug

# ============================================================================
# Insurance Provider Configuration
# ============================================================================

# Active Provider: Set this to the provider you want to use
# Can be overridden via ACTIVE_PROVIDER environment variable
ACTIVE_PROVIDER = os.getenv('ACTIVE_PROVIDER', 'FWD')

# Provider Configurations
# Each provider has its own configuration dictionary
# Sensitive values are loaded from environment variables
PROVIDER_CONFIGS = {
    'FWD': {
        'name': 'FWD',
        'base_url': os.getenv('FWD_BASE_URL', 'https://apihk.fwd.com.hk'),
        'client_id': os.getenv('FWD_CLIENT_ID', ''),
        'client_secret': os.getenv('FWD_CLIENT_SECRET', ''),
        'provision_key': os.getenv('FWD_PROVISION_KEY', ''),
        'authenticated_userid': os.getenv('FWD_AUTHENTICATED_USERID', 'svc_amg_prd'),
        'grant_type': 'authorization_code',
        'grant_type_refresh': 'refresh_token',
        'response_type': 'code',
        'excluded_document_codes': [
            "0000103A", "0000103B", "0000103C", "0000103D",
            "0000103W", "0000103Y", "0000103Z", "000M103A",
            "000M103W", "0000116A", "0000275A"
        ]
    },
    # Add more provider configurations here as needed
    # Example:
    # 'COMPANY_B': {
    #     'name': 'COMPANY_B',
    #     'base_url': os.getenv('COMPANY_B_BASE_URL', 'https://api.companyb.com'),
    #     'api_key': os.getenv('COMPANY_B_API_KEY', ''),
    #     # ... other company-specific config
    # },
}

# Validate that required secrets are provided
if not PROVIDER_CONFIGS[ACTIVE_PROVIDER]['client_id']:
    raise ValueError(
        f"FWD_CLIENT_ID environment variable is required. "
        f"Please set it in your .env file or environment variables."
    )
if not PROVIDER_CONFIGS[ACTIVE_PROVIDER]['client_secret']:
    raise ValueError(
        f"FWD_CLIENT_SECRET environment variable is required. "
        f"Please set it in your .env file or environment variables."
    )
if not PROVIDER_CONFIGS[ACTIVE_PROVIDER]['provision_key']:
    raise ValueError(
        f"FWD_PROVISION_KEY environment variable is required. "
        f"Please set it in your .env file or environment variables."
    )

# ============================================================================
# Backward Compatibility (Deprecated - Use PROVIDER_CONFIGS instead)
# ============================================================================

# These variables are kept for backward compatibility with existing code
# They will be removed in a future version
host_server = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['base_url']
client_id = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['client_id']
client_secret = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['client_secret']
provision_key = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['provision_key']
authenticated_userid = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['authenticated_userid']
grant_type = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['grant_type']
grant_type_refresh = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['grant_type_refresh']
response_type = PROVIDER_CONFIGS[ACTIVE_PROVIDER]['response_type']


def get_provider_config(provider_name: str = None) -> dict:
    """
    Get configuration for a specific provider.
    
    Args:
        provider_name: Name of the provider (defaults to ACTIVE_PROVIDER)
        
    Returns:
        Configuration dictionary for the provider
        
    Raises:
        KeyError: If provider configuration not found
    """
    provider = provider_name or ACTIVE_PROVIDER
    if provider not in PROVIDER_CONFIGS:
        raise KeyError(f"Provider '{provider}' not found in PROVIDER_CONFIGS. Available: {list(PROVIDER_CONFIGS.keys())}")
    return PROVIDER_CONFIGS[provider].copy()
