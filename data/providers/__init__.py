"""
Insurance Provider Module

This module provides a generic interface for integrating with different insurance company APIs.
"""

from .base import InsuranceProvider
from .fwd_provider import FWDProvider
from .factory import ProviderFactory

__all__ = ['InsuranceProvider', 'FWDProvider', 'ProviderFactory']

