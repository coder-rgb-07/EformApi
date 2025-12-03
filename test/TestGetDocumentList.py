"""
Test script to get document list for a specific policy number
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
from Config import host_server


def get_document_list(policy_no: str):
    """
    Get document list for a given policy number
    
    Args:
        policy_no: Policy number to query
    """
    print(f"\n{'='*60}")
    print(f"Getting document list for policy number: {policy_no}")
    print(f"{'='*60}\n")
    
    try:
        # Initialize Net class (this will handle authentication)
        net = Net()
        
        # Prepare the request data
        data = {
            'policyNo': policy_no
        }
        
        # Encrypt the request payload
        encrypt = net.encrypt
        logger.info("Encrypting request payload...")
        encrypted_payload = encrypt.encryptParam(data)
        logger.info(f"Encryption successful, encrypted payload length: {len(encrypted_payload)}")

        # Make the API request
        url = f'{host_server}/sales-api/v1/application/getDocumentList'
        logger.info(f"Making API request to: {url}")
        result = net._Net__request(url, encrypted_payload)
        
        # Check if response contains encryptPayload
        if 'encryptPayload' not in result:
            error_msg = f"API response missing encryptPayload field. Response: {result}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Check if encryptPayload is empty
        if not result['encryptPayload'] or len(result['encryptPayload']) == 0:
            error_msg = f"API response encryptPayload is empty. Response: {result}"
            logger.error(error_msg)
            raise Exception(error_msg)

        # Decrypt the response
        logger.info("Decrypting response payload...")
        decrypted_response = encrypt.decryptParam(result['encryptPayload'])
        
        # Print the full document list information
        print("Full Document List Response:")
        print("-" * 60)
        print(json.dumps(decrypted_response, indent=2, ensure_ascii=False))
        print("-" * 60)
        
        # Extract and print key information
        if 'policyDocumentList' in decrypted_response:
            policy_docs = decrypted_response['policyDocumentList']
            print(f"\nNumber of policy document entries: {len(policy_docs)}")
            
            total_documents = 0
            for idx, policy_doc in enumerate(policy_docs):
                if 'documentList' in policy_doc:
                    doc_list = policy_doc['documentList']
                    print(f"\nPolicy Document Entry {idx + 1}:")
                    print(f"  Number of document types: {len(doc_list)}")
                    
                    for doc_idx, document in enumerate(doc_list):
                        doc_code = document.get('documentCode', 'N/A')
                        ref_nos = document.get('documentRefNoList', [])
                        total_documents += len(ref_nos)
                        print(f"    Document {doc_idx + 1}:")
                        print(f"      Code: {doc_code}")
                        print(f"      Reference Numbers: {len(ref_nos)}")
                        if ref_nos:
                            print(f"      First few refs: {ref_nos[:3]}")
            
            print(f"\nTotal document reference numbers: {total_documents}")
        
        # Also call the existing method to see filtered results
        print(f"\n{'='*60}")
        print("Filtered Document List (using existing getDocumentList method):")
        print(f"{'='*60}\n")
        filtered_list = net.getDocumentList(policy_no)
        print(f"\nFiltered document reference numbers ({len(filtered_list)}):")
        if filtered_list:
            print(json.dumps(filtered_list, indent=2, ensure_ascii=False))
        else:
            print("  (No documents after filtering)")
        
        return decrypted_response
        
    except Exception as e:
        logger.error(f"Error getting document list: {e}")
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
    # Policy number: 20007752
    policy_number = "20003200"
    
    # Get document list
    document_list = get_document_list(policy_number)
    
    if document_list:
        print(f"\nSuccessfully retrieved document list for {policy_number}")
    else:
        print(f"\nFailed to retrieve document list for {policy_number}")

