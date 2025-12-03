"""
Test script to get policy information for a specific policy number
"""
import sys
import os
import json
import io

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.Net import Net
from common.logger import logger


def get_policy_info(policy_no: str):
    """
    Get full policy information for a given policy number
    
    Args:
        policy_no: Policy number to query
    """
    print(f"\n{'='*60}")
    print(f"Getting policy information for policy number: {policy_no}")
    print(f"{'='*60}\n")
    
    try:
        # Initialize Net class (this will handle authentication)
        net = Net()
        
        # Call the getPolicyInfo method to get full policy information
        policy_info = net.getPolicyInfo(policy_no)
        
        # Print the full policy information
        print("Full Policy Information:")
        print("-" * 60)
        print(json.dumps(policy_info, indent=2, ensure_ascii=False))
        print("-" * 60)
        
        # Extract and print key information
        if 'agentId' in policy_info:
            print(f"\nAgent ID: {policy_info['agentId']}")
        
        # Print all available fields
        print("\nAvailable fields in response:")
        for key, value in policy_info.items():
            if isinstance(value, (dict, list)):
                print(f"  - {key}: {type(value).__name__} (see full JSON above)")
            else:
                print(f"  - {key}: {value}")
        
        return policy_info
        
    except Exception as e:
        logger.error(f"Error getting policy information: {e}")
        error_str = str(e)
        # Handle Unicode encoding for Windows console
        try:
            print(f"\nError: {error_str}")
        except UnicodeEncodeError:
            print(f"\nError: {error_str.encode('ascii', 'replace').decode('ascii')}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    # Policy number from the image: 20007752
    policy_number = "20003200"
    
    # Get policy information
    policy_info = get_policy_info(policy_number)
    
    if policy_info:
        print(f"\nSuccessfully retrieved policy information for {policy_number}")
    else:
        print(f"\nFailed to retrieve policy information for {policy_number}")

