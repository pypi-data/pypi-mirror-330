import requests

from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from secretvalidate.session_manager import get_session
from secretvalidate.http_validator import get_headers, get_service_url
import json


# Use the shared session
session = get_session()

def validate_new_relic(service, secret, response):
    """Validate New Relic License Key."""
    payload = {'message': '[M&S AppSec Team] Found a New Relic harcoded secret in Github. Please check the AppSec wiki for remediation instructions: https://devopssec.engineering.mnscorp.net/Products/GHAS-Secret-Scanning/Prioritising-and-Fixing'}
    headers = get_headers(service, secret)

    # New Relic has two possible endpoints, a EU-based one and a global. 
    # We don't know which our developers will use, so we need to check both.
    urls = get_service_url(service)

    try:
        status_code = []
        for url in urls:
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            if res.status_code == 202:
                return get_secret_active() if response else "New Relic secret is active."
            
            elif res.status_code == 403:
                status_code.append(res.status_code)
                
            elif res.status_code >= 500:
                return f"Unexpected HTTP response status: {res.status_code}"
        if 202 not in status_code:
            return get_secret_inactive() if response else "New Relic secret is inactive."

    except requests.exceptions.RequestException as e:
        return str(e)


# curl --location --request POST 'https://log-api.newrelic.com/log/v1' \
# --header 'X-License-Key: licensekey' \
# --header 'Content-Type: application/json' \
# --data '{"message":"[M&S AppSec Team] Found a New Relic harcoded secret in Github, please rotate it"}' -vvv

# curl --location --request POST 'https://log-api.eunewrelic.com/log/v1' \
# --header 'X-License-Key: licensekey' \
# --header 'Content-Type: application/json' \
# --data '{"message":"[M&S AppSec Team] Found a New Relic harcoded secret in Github, please rotate it"}' -vvv


