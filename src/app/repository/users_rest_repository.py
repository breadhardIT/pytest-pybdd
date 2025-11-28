import requests
from fastapi import HTTPException

class UsersRestRepository:
    """
    A repository for accessing enrolled users
    Args:
        base_url(str): base url for endpoint
        timeout(str): timeout limit, default 5.0 seconds
    """
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def exists(self, user_id: str) -> bool:
        """
        Validate if user is enrolled
        Args:
            user_id(str): The user id
        Returns:
            boolean: True if user exists, false if user doesn't exist
        Raises:
            HTTPException with 500 status
        """
        url = f"{self.base_url}/users/{user_id}"
        response = requests.get(url, timeout=self.timeout)

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise HTTPException(status_code=500,detail="Internal server error")