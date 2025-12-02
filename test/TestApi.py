print("love")

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import host_server, client_id, client_secret, provision_key, authenticated_userid, grant_type, response_type
from common.logger import logger

def get_token():
    try:
        logger.info("Fetching access token...")
        url = f'{host_server}/authorization-api/v1/oauth2/authorize'
        hdr = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        payload = {
            'client_id': client_id,
            'response_type': response_type,
            'provision_key': provision_key,
            'authenticated_userid': authenticated_userid,
        }

        # step 1 获取 redirect_uri
        response = requests.post(url, headers=hdr, json=payload)
        code = response.json()['redirect_uri'].split('=')[1]

        # step 2 获取 token
        url = f'{host_server}/authorization-api/v1/oauth2/token'
        payload = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': host_server,
            'code': code,
        }
        response = requests.post(url, headers=hdr, json=payload)
        logger.info("Access token fetched successfully.")
        return response.json()['access_token']
    except Exception as e:
        logger.error(f"Failed to fetch access token: {e}")
        raise

token = get_token()

print('token = '+token)