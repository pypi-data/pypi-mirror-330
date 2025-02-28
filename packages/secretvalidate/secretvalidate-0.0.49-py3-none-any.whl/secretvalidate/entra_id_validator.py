import jwt

from dotenv import load_dotenv
from datetime import datetime
import time
from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from secretvalidate.http_validator import get_service_url

load_dotenv()

def validate_entra_id(service, token, response):
    """
    This funcion will check if the JWT is expired or not. This will solve 100% of current cases.
    TODO: Extend function to actual validation against Microsoft should the need arise.
    """
    metadata_url = get_service_url(service)

    current_time = time.time()
    decoded_token = jwt.decode(token, jwt.PyJWKClient(metadata_url), require=["exp"], options={"verify_signature": False}) 
    token_expiration = decoded_token.get("exp") 
    expiration_human_friendly = datetime.fromtimestamp(token_expiration) 

    if not token_expiration:
        return "JWT missing expiration claim."
    
    if token_expiration < current_time:
        return get_secret_inactive() if response else f"JWT expired on {expiration_human_friendly}"
    else:
        return get_secret_active() if response else "JWT not expired"
