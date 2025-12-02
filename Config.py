# ============================================================================
# Application Configuration
# ============================================================================

# Debug Mode
# Debug = True
Debug = False
Release = not Debug

# ============================================================================
# Insurance Provider Configuration
# ============================================================================

# Active Provider: Set this to the provider you want to use
# Available providers: 'FWD'
ACTIVE_PROVIDER = 'FWD'

# Provider Configurations
# Each provider has its own configuration dictionary
PROVIDER_CONFIGS = {
    'FWD': {
        'name': 'FWD',
        'base_url': 'https://apihk.fwd.com.hk',
        'client_id': '3tZsJZLi3BhjC7RjtLNVmi40cow5Jvsm',
        'client_secret': '8U04MKDugrlUTcfssxKuVOjInHxFRUJP',
        'provision_key': 'Di4ft7rYG3qPXXoRx5AsVajZSYonxcD0',
        'authenticated_userid': 'svc_amg_prd',
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
    #     'base_url': 'https://api.companyb.com',
    #     'api_key': 'your_api_key',
    #     # ... other company-specific config
    # },
}

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
