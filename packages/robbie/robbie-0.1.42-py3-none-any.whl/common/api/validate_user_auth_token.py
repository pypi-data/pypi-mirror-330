import requests
from common.user_config import user_config
from common.env_config import env
from common.logging_config import logger

def is_auth_token_valid() -> bool:
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN}
    url = f'{env.API_BASE}/validate-user-auth-token'
    
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)

    logger.debug(response)
    if response.status_code == 200:
        if response.json().get('sentryDsn'):
            user_config.sentry_dsn = response.json().get('sentryDsn')
            user_config.write()
        else:
            logger.warning('No sentryDsn in response')
        return True
    else:
        return False     

if __name__ == "__main__":
    print(is_auth_token_valid())
