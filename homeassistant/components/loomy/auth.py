# api.py
import aiohttp

from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session


class Auth0APIClient:
    def __init__(self, session: OAuth2Session):
        self.session = session

    async def async_get_access_token(self):
        """Get a valid access token."""
        await self.session.async_ensure_token_valid()
        return self.session.token["access_token"]

    async def async_make_request(self, method, url, **kwargs):
        """Make an authenticated request to your backend."""
        token = await self.async_get_access_token()

        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        async with aiohttp.ClientSession() as client:
            async with client.request(method, url, **kwargs) as response:
                return await response.json()
