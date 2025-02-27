import requests
from ..utility.passwords import password_encrypt_sha512


class Auth:
    def __init__(self, session, logger, base_url, workspace_instance):
        self.session = session
        self.logger = logger
        self.base_url = base_url
        self.workspace_instance = workspace_instance
        self.user_instance = None

    def login(self, email: str, password: str):
        """Authenticate a user and store their auth token."""
        try: 
            if not email or not password:
                raise ValueError("Email and Password are required to login")
            
            url = f"{self.base_url}/rest/v17/user/login"
            headers = {
                'Content-Type': 'application/json',
                'jwt': 'true',
                'businessDomain': self.workspace_instance['BUSINESS_DOMAIN'],
                'businessTagId': self.workspace_instance['BUSINESS_TAG_ID'],
            }
            sha512pwd = password_encrypt_sha512(password)
            data = {'email': email, 'password': sha512pwd}
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            resp = response.json()
            if resp.get('error') is False:
                token = resp['loginToken']
                headers = {
                    'Authorization': f"Bearer {token}",
                    'businessDomain': self.workspace_instance['BUSINESS_DOMAIN'],
                    'jwt': token,
                    'Content-type': 'application/json;charset=UTF-8',
                    "device": 'script',
                    'businessTagID': self.workspace_instance['BUSINESS_TAG_ID']
                }
                self.session.headers.update(headers)
                self.user_instance = resp
                self.logger.info(f"User {email} logged in")
            else:
                raise ValueError(resp.get('message'))
            return resp
        except requests.exceptions.RequestException as http_err:
            error_response = response.json()
            status_code = error_response.get('statusCode', response.status_code)
            error_message = error_response.get('message', str(http_err))

            error_message = f"{status_code} Error: {error_message}"
            self.logger.error(f"An error occurred: {error_message}")
            raise requests.exceptions.HTTPError(error_message)
        except Exception as e:
            self.logger.error(e)
            raise e
