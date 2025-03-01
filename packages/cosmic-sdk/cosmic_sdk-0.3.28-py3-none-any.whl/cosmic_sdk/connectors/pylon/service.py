import requests
from pprint import pprint
from .models import AccountList, Account

class PylonService:
    def __init__(self, credentials: dict):
        oauth_token = credentials.get('oauth_token')
        if not oauth_token:
            raise ValueError("Missing required credential: 'oauth_token'")
        self.oauth_token = oauth_token
        self.api_url = "https://api.usepylon.com"
        self.account_slug = "accounts"
        self.issues_slug = "issues"
        self.headers = {"Authorization": f"Bearer {self.oauth_token}", "Content-Type":"application/json"}

    def _handle_error(self, response: requests.Response):
        if response.status_code >= 400:
            error_text = response.text
            print(f"Request failed with status code {response.status_code}")
            print(f"Error response: {error_text}")
        response.raise_for_status()

    def get_accounts(self) -> AccountList:
        """
        Get all accounts
        """
        response = requests.get(
            f"{self.api_url}/{self.account_slug}",
            headers=self.headers,
        )
        self._handle_error(response)
        response.raise_for_status()
        resp = response.json()
        pprint(resp)

        return AccountList(**resp)
    
    def get_account_by_id(self, account_id: str) -> Account:
        """
        Get an account by id
        """
        response = requests.get(
            f"{self.api_url}/{self.account_slug}/{account_id}",
            headers=self.headers,
        )
        self._handle_error(response)
        response.raise_for_status()
        resp = response.json()
        return Account(**resp.get("data"))

    def update_account(self, account_id: str, data: dict) -> Account:
        """
        Update an account
        """
        response = requests.patch(
            f"{self.api_url}/{self.account_slug}/{account_id}",
            headers=self.headers,
            json=data,
        )
        self._handle_error(response)
        resp = response.json()
        return Account(**resp.get("data"))
            
if __name__ == "__main__":
    service = PylonService({})
    accounts = service.get_accounts()
    print(accounts)

    account = service.get_account_by_id("")
    print(account)

    account_update = {    
        "tags": [
            f"champion: Shikhar"
        ]
    }

    account = service.update_account("", account_update)
    print(account)

    
